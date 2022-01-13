from typing import Dict, List, Optional, Set, cast
from enum import Enum
from datetime import date, timedelta
from functools import wraps
from uuid import uuid4
from flask import g, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.local import LocalProxy
from sqlalchemy import Table, Column, String, Integer, Boolean
from ._config import API_KEY_REQUIRED_STARTING_AT, RATELIMIT_STORAGE_URL
from ._common import app, request, db
from ._exceptions import MissingAPIKeyException, UnAuthenticatedException
from ._db import metadata, TABLE_OPTIONS

API_KEY_HARD_WARNING = API_KEY_REQUIRED_STARTING_AT - timedelta(days=14)
API_KEY_SOFT_WARNING = API_KEY_HARD_WARNING - timedelta(days=14)

API_KEY_WARNING_TEXT = "an api key will be required starting at {}, go to https://delphi.cmu.edu to request one".format(API_KEY_REQUIRED_STARTING_AT)

user_table = Table(
    "api_user",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("api_key", String(50), unique=True),
    Column("roles", String(255)),
    Column('tracking', Boolean(), default=True),
    Column('registered', Boolean(), default=False),
    **TABLE_OPTIONS,
)

class DBUser:
    id: int
    api_key: str
    roles: Set[str]
    tracking: bool = True
    registered: bool = False

    @property
    def roles_str(self):
        return '\n'.join(self.roles)

    @staticmethod
    def _parse(r: Dict) -> 'DBUser':
        u = DBUser()
        u.id = r['id']
        u.api_key = r['api_key']
        u.roles = set(r['roles'].split(','))
        u.tracking = r['tracking'] != False
        u.registered = r['registered'] == True
        return u

    @staticmethod
    def find(user_id: int) -> 'DBUser':
        stmt = user_table.select().where(user_table.c.id == user_id)
        return DBUser._parse(db.execution_options(stream_results=False).execute(stmt).first())

    @staticmethod
    def find_by_api_key(api_key: int) -> Optional['DBUser']:
        stmt = user_table.select().where(user_table.c.api_key == api_key)
        r = db.execution_options(stream_results=False).execute(stmt).first()
        if r is None:
            return None
        return DBUser._parse(r)

    @staticmethod
    def list() -> List['DBUser']:
        return [DBUser._parse(r) for r in db.execution_options(stream_results=False).execute(user_table.select())]

    @staticmethod
    def insert(api_key: str, roles: Set[str], tracking: bool = True, registered: bool = False):
        db.execute(user_table.insert().values(api_key=api_key, roles=','.join(roles), tracking=tracking, registered=registered))

    @staticmethod
    def register_new_key() -> str:
        api_key = str(uuid4())
        DBUser.insert(api_key, set(), True, False)
        return api_key

    def delete(self):
        db.execute(user_table.delete(user_table.c.id == self.id))

    def update(self, api_key: str, roles: Set[str], tracking: bool = True, registered: bool = False) -> 'DBUser':
        db.execute(user_table.update().where(user_table.c.id == self.id).values(api_key=api_key, roles=','.join(roles), tracking=tracking, registered=registered))
        self.api_key = api_key
        self.roles = roles
        self.tracking = tracking
        self.registered = registered
        return self



class UserRole(str, Enum):
    afhsb = "afhsb"
    cdc = "cdc"
    fluview = "fluview"
    ght = "ght"
    norostat = "norostat"
    quidel = "quidel"
    sensors = "sensors"
    sensor_twtr = "sensor_twtr"
    sensor_gft = "sensor_gft"
    sensor_ght = "sensor_ght"
    sensor_ghtj = "sensor_ghtj"
    sensor_cdc = "sensor_cdc"
    sensor_quid = "sensor_quid"
    sensor_wiki = "sensor_wiki"
    twitter = "twitter"


# begin sensor query authentication configuration
#   A multimap of sensor names to the "granular" auth tokens that can be used to access them; excludes the "global" sensor auth key that works for all sensors:
GRANULAR_SENSOR_ROLES = {
    "twtr": UserRole.sensor_twtr,
    "gft": UserRole.sensor_gft,
    "ght": UserRole.sensor_ght,
    "ghtj": UserRole.sensor_ghtj,
    "cdc": UserRole.sensor_cdc,
    "quid": UserRole.sensor_quid,
    "wiki": UserRole.sensor_wiki,
}

#   A set of sensors that do not require an auth key to access:
OPEN_SENSORS = [
    "sar3",
    "epic",
    "arch",
]


class User:
    api_key: str
    roles: Set[UserRole]
    authenticated: bool
    tracking: bool = True
    registered: bool = True

    def __init__(self, api_key: str, authenticated: bool, roles: Set[UserRole], tracking: bool = True, registered: bool = False) -> None:
        self.api_key = api_key
        self.authenticated = authenticated
        self.roles = roles
        self.tracking = tracking
        self.registered = registered

    def has_role(self, role: UserRole) -> bool:
        return role in self.roles

    def log_info(self, msg: str, *args, **kwargs) -> None:
        if self.authenticated and self.tracking:
            app.logger.info(f"apikey: {self.api_key}, {msg}", *args, **kwargs)
        else:
            app.logger.info(msg, *args, **kwargs)

    def is_rate_limited(self) -> bool:
        return not self.registered


ANONYMOUS_USER = User("anonymous", False, set())


def _find_user(api_key: Optional[str]) -> User:
    if not api_key:
        return ANONYMOUS_USER
    stmt = user_table.select().where(user_table.c.api_key == api_key)
    user = db.execution_options(stream_results=False).execute(stmt).first()
    if user is None:
        return ANONYMOUS_USER
    else:
        return User(user.api_key, True, set(user.roles.split(",")), user.tracking, user.registered)

def resolve_auth_token() -> Optional[str]:
    # auth request param
    for name in ('auth', 'api_key', 'token'):
        if name in request.values:
            return request.values[name]
    # user name password
    if request.authorization and request.authorization.username == "epidata":
        return request.authorization.password
    # bearer token authentication
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[len("Bearer ") :]
    return None


def _get_current_user() -> User:
    if "user" not in g:
        api_key = resolve_auth_token()
        user = _find_user(api_key)
        if not user.authenticated and require_api_key():
            raise MissingAPIKeyException()
        user.log_info(request.full_path)
        g.user = user
    return g.user


current_user: User = cast(User, LocalProxy(_get_current_user))


def require_api_key() -> bool:
    n = date.today()
    return n >= API_KEY_REQUIRED_STARTING_AT and not app.config.get('TESTING', False)


def show_soft_api_key_warning() -> bool:
    n = date.today()
    return not current_user.authenticated and not app.config.get('TESTING', False) and n > API_KEY_SOFT_WARNING and n < API_KEY_HARD_WARNING


def show_hard_api_key_warning() -> bool:
    n = date.today()
    return not current_user.authenticated and not app.config.get('TESTING', False) and n > API_KEY_HARD_WARNING


def _is_public_route() -> bool:
    return request.path.startswith("/lib") or request.path.startswith('/admin') or request.path.startswith('/version')

@app.before_request
def resolve_user():
    if _is_public_route():
        return
    # try to get the db
    try:
        _get_current_user()
    except MissingAPIKeyException as e:
        raise e
    except UnAuthenticatedException as e:
        raise e
    except:
        app.logger.error("user connection error", exc_info=True)
        if require_api_key():
            raise MissingAPIKeyException()
        else:
            g.user = ANONYMOUS_USER


def require_role(required_role: Optional[UserRole]):
    def decorator_wrapper(f):
        if not required_role:
            return f

        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user or not current_user.has_role(required_role):
                raise UnAuthenticatedException()
            return f(*args, **kwargs)

        return decorated_function

    return decorator_wrapper

def _resolve_tracking_key() -> str:
    token = resolve_auth_token()
    return token or get_remote_address()

def deduct_on_success(response: Response) -> bool:
    if response.status_code != 200:
        return False
    # check if we have the classic format
    if not response.is_streamed and response.is_json:
        out = response.json
        if out and isinstance(out, dict) and out.get('result') == -1:
            return False
    return True

limiter = Limiter(app, key_func=_resolve_tracking_key, storage_uri=RATELIMIT_STORAGE_URL)

@limiter.request_filter
def _no_rate_limit() -> bool:
    if app.config.get('TESTING', False) or _is_public_route():
        return False
    # no rate limit if the user is registered
    user = _get_current_user()
    return user is not None and not user.is_rate_limited()