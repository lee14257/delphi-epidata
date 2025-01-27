# first party
from delphi.epidata.acquisition.covid_hosp.common.database import Database as BaseDatabase
from delphi.epidata.acquisition.covid_hosp.common.utils import Utils


class Database(BaseDatabase):

  TABLE_NAME = 'covid_hosp_facility'
  KEY_COLS = ['hospital_pk', 'collection_week']
  # These are 3-tuples of (
  #   CSV header name,
  #   SQL db column name,
  #   data type
  # ) for all the columns in the CSV file.
  # Note that the corresponding database column names may be shorter
  # due to constraints on the length of column names. See
  # /src/ddl/covid_hosp.sql for more information.
  ORDERED_CSV_COLUMNS = [
      ('hospital_pk', 'hospital_pk', str),
      ('collection_week', 'collection_week', Utils.int_from_date),
      ('address', 'address', str),
      ('all_adult_hospital_beds_7_day_avg', 'all_adult_hospital_beds_7_day_avg', float),
      ('all_adult_hospital_beds_7_day_coverage', 'all_adult_hospital_beds_7_day_coverage', int),
      ('all_adult_hospital_beds_7_day_sum', 'all_adult_hospital_beds_7_day_sum', int),
      ('all_adult_hospital_inpatient_bed_occupied_7_day_avg',
       'all_adult_hospital_inpatient_bed_occupied_7_day_avg', float),
      ('all_adult_hospital_inpatient_bed_occupied_7_day_coverage',
       'all_adult_hospital_inpatient_bed_occupied_7_day_coverage', int),
      ('all_adult_hospital_inpatient_bed_occupied_7_day_sum',
       'all_adult_hospital_inpatient_bed_occupied_7_day_sum', int),
      ('all_adult_hospital_inpatient_beds_7_day_avg', 'all_adult_hospital_inpatient_beds_7_day_avg',
       float),
      ('all_adult_hospital_inpatient_beds_7_day_coverage',
       'all_adult_hospital_inpatient_beds_7_day_coverage', int),
      ('all_adult_hospital_inpatient_beds_7_day_sum', 'all_adult_hospital_inpatient_beds_7_day_sum',
       int),
      ('ccn', 'ccn', str),
      ('city', 'city', str),
      ('fips_code', 'fips_code', str),
      ('geocoded_hospital_address', 'geocoded_hospital_address', str),
      ('hhs_ids', 'hhs_ids', str),
      ('hospital_name', 'hospital_name', str),
      ('hospital_subtype', 'hospital_subtype', str),
      ('icu_beds_used_7_day_avg', 'icu_beds_used_7_day_avg', float),
      ('icu_beds_used_7_day_coverage', 'icu_beds_used_7_day_coverage', int),
      ('icu_beds_used_7_day_sum', 'icu_beds_used_7_day_sum', int),
      ('icu_patients_confirmed_influenza_7_day_avg', 'icu_patients_confirmed_influenza_7_day_avg',
       float),
      ('icu_patients_confirmed_influenza_7_day_coverage',
       'icu_patients_confirmed_influenza_7_day_coverage', int),
      ('icu_patients_confirmed_influenza_7_day_sum', 'icu_patients_confirmed_influenza_7_day_sum',
       int),
      ('inpatient_beds_7_day_avg', 'inpatient_beds_7_day_avg', float),
      ('inpatient_beds_7_day_coverage', 'inpatient_beds_7_day_coverage', int),
      ('inpatient_beds_7_day_sum', 'inpatient_beds_7_day_sum', int),
      ('inpatient_beds_used_7_day_avg', 'inpatient_beds_used_7_day_avg', float),
      ('inpatient_beds_used_7_day_coverage', 'inpatient_beds_used_7_day_coverage', int),
      ('inpatient_beds_used_7_day_sum', 'inpatient_beds_used_7_day_sum', int),
      ('is_corrected', 'is_corrected', Utils.parse_bool),
      ('is_metro_micro', 'is_metro_micro', Utils.parse_bool),
      ('previous_day_admission_adult_covid_confirmed_18-19_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_18_19_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_20-29_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_20_29_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_30-39_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_30_39_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_40-49_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_40_49_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_50-59_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_50_59_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_60-69_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_60_69_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_70-79_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_70_79_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_7_day_coverage',
       'previous_day_admission_adult_covid_confirmed_7_day_coverage', int),
      ('previous_day_admission_adult_covid_confirmed_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_80+_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_80plus_7_day_sum', int),
      ('previous_day_admission_adult_covid_confirmed_unknown_7_day_sum',
       'previous_day_admission_adult_covid_confirmed_unknown_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_18-19_7_day_sum',
       'previous_day_admission_adult_covid_suspected_18_19_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_20-29_7_day_sum',
       'previous_day_admission_adult_covid_suspected_20_29_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_30-39_7_day_sum',
       'previous_day_admission_adult_covid_suspected_30_39_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_40-49_7_day_sum',
       'previous_day_admission_adult_covid_suspected_40_49_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_50-59_7_day_sum',
       'previous_day_admission_adult_covid_suspected_50_59_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_60-69_7_day_sum',
       'previous_day_admission_adult_covid_suspected_60_69_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_70-79_7_day_sum',
       'previous_day_admission_adult_covid_suspected_70_79_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_7_day_coverage',
       'previous_day_admission_adult_covid_suspected_7_day_coverage', int),
      ('previous_day_admission_adult_covid_suspected_7_day_sum',
       'previous_day_admission_adult_covid_suspected_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_80+_7_day_sum',
       'previous_day_admission_adult_covid_suspected_80plus_7_day_sum', int),
      ('previous_day_admission_adult_covid_suspected_unknown_7_day_sum',
       'previous_day_admission_adult_covid_suspected_unknown_7_day_sum', int),
      ('previous_day_admission_influenza_confirmed_7_day_sum',
       'previous_day_admission_influenza_confirmed_7_day_sum', int),
      ('previous_day_admission_pediatric_covid_confirmed_7_day_coverage',
       'previous_day_admission_pediatric_covid_confirmed_7_day_coverage', int),
      ('previous_day_admission_pediatric_covid_confirmed_7_day_sum',
       'previous_day_admission_pediatric_covid_confirmed_7_day_sum', int),
      ('previous_day_admission_pediatric_covid_suspected_7_day_coverage',
       'previous_day_admission_pediatric_covid_suspected_7_day_coverage', int),
      ('previous_day_admission_pediatric_covid_suspected_7_day_sum',
       'previous_day_admission_pediatric_covid_suspected_7_day_sum', int),
      ('previous_day_covid_ED_visits_7_day_sum', 'previous_day_covid_ed_visits_7_day_sum', int),
      ('previous_day_total_ED_visits_7_day_sum', 'previous_day_total_ed_visits_7_day_sum', int),
      ('previous_week_patients_covid_vaccinated_doses_all_7_day',
       'previous_week_patients_covid_vaccinated_doses_all_7_day', int),
      ('previous_week_patients_covid_vaccinated_doses_all_7_day_sum',
       'previous_week_patients_covid_vaccinated_doses_all_7_day_sum', int),
      ('previous_week_patients_covid_vaccinated_doses_one_7_day',
       'previous_week_patients_covid_vaccinated_doses_one_7_day', int),
      ('previous_week_patients_covid_vaccinated_doses_one_7_day_sum',
       'previous_week_patients_covid_vaccinated_doses_one_7_day_sum', int),
      ('previous_week_personnel_covid_vaccinated_doses_administered_7_day',
       'previous_week_personnel_covid_vaccd_doses_administered_7_day', int),
      ('previous_week_personnel_covid_vaccinated_doses_administered_7_day_sum',
       'previous_week_personnel_covid_vaccd_doses_administered_7_day_sum', int),
      ('staffed_adult_icu_bed_occupancy_7_day_avg', 'staffed_adult_icu_bed_occupancy_7_day_avg',
       float),
      ('staffed_adult_icu_bed_occupancy_7_day_coverage',
       'staffed_adult_icu_bed_occupancy_7_day_coverage', int),
      ('staffed_adult_icu_bed_occupancy_7_day_sum', 'staffed_adult_icu_bed_occupancy_7_day_sum',
       int),
      ('staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_avg',
       'staffed_icu_adult_patients_confirmed_suspected_covid_7d_avg', float),
      ('staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_coverage',
       'staffed_icu_adult_patients_confirmed_suspected_covid_7d_cov', int),
      ('staffed_icu_adult_patients_confirmed_and_suspected_covid_7_day_sum',
       'staffed_icu_adult_patients_confirmed_suspected_covid_7d_sum', int),
      ('staffed_icu_adult_patients_confirmed_covid_7_day_avg',
       'staffed_icu_adult_patients_confirmed_covid_7_day_avg', float),
      ('staffed_icu_adult_patients_confirmed_covid_7_day_coverage',
       'staffed_icu_adult_patients_confirmed_covid_7_day_coverage', int),
      ('staffed_icu_adult_patients_confirmed_covid_7_day_sum',
       'staffed_icu_adult_patients_confirmed_covid_7_day_sum', int),
      ('state', 'state', str),
      ('total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_avg',
       'total_adult_patients_hosp_confirmed_suspected_covid_7d_avg', float),
      ('total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_coverage',
       'total_adult_patients_hosp_confirmed_suspected_covid_7d_cov', int),
      ('total_adult_patients_hospitalized_confirmed_and_suspected_covid_7_day_sum',
       'total_adult_patients_hosp_confirmed_suspected_covid_7d_sum', int),
      ('total_adult_patients_hospitalized_confirmed_covid_7_day_avg',
       'total_adult_patients_hospitalized_confirmed_covid_7_day_avg', float),
      ('total_adult_patients_hospitalized_confirmed_covid_7_day_coverage',
       'total_adult_patients_hospitalized_confirmed_covid_7_day_coverage', int),
      ('total_adult_patients_hospitalized_confirmed_covid_7_day_sum',
       'total_adult_patients_hospitalized_confirmed_covid_7_day_sum', int),
      ('total_beds_7_day_avg', 'total_beds_7_day_avg', float),
      ('total_beds_7_day_coverage', 'total_beds_7_day_coverage', int),
      ('total_beds_7_day_sum', 'total_beds_7_day_sum', int),
      ('total_icu_beds_7_day_avg', 'total_icu_beds_7_day_avg', float),
      ('total_icu_beds_7_day_coverage', 'total_icu_beds_7_day_coverage', int),
      ('total_icu_beds_7_day_sum', 'total_icu_beds_7_day_sum', int),
      ('total_patients_hospitalized_confirmed_influenza_7_day_avg',
       'total_patients_hospitalized_confirmed_influenza_7_day_avg', float),
      ('total_patients_hospitalized_confirmed_influenza_7_day_coverage',
       'total_patients_hospitalized_confirmed_influenza_7_day_coverage', int),
      ('total_patients_hospitalized_confirmed_influenza_7_day_sum',
       'total_patients_hospitalized_confirmed_influenza_7_day_sum', int),
      ('total_patients_hospitalized_confirmed_influenza_and_covid_7_day_avg',
       'total_patients_hosp_confirmed_influenza_and_covid_7d_avg', float),
      ('total_patients_hospitalized_confirmed_influenza_and_covid_7_day_coverage',
       'total_patients_hosp_confirmed_influenza_and_covid_7d_cov', int),
      ('total_patients_hospitalized_confirmed_influenza_and_covid_7_day_sum',
       'total_patients_hosp_confirmed_influenza_and_covid_7d_sum', int),
      ('total_pediatric_patients_hospitalized_confirmed_and_suspected_covid_7_day_avg',
       'total_pediatric_patients_hosp_confirmed_suspected_covid_7d_avg', float),
      ('total_pediatric_patients_hospitalized_confirmed_and_suspected_covid_7_day_coverage',
       'total_pediatric_patients_hosp_confirmed_suspected_covid_7d_cov', int),
      ('total_pediatric_patients_hospitalized_confirmed_and_suspected_covid_7_day_sum',
       'total_pediatric_patients_hosp_confirmed_suspected_covid_7d_sum', int),
      ('total_pediatric_patients_hospitalized_confirmed_covid_7_day_avg',
       'total_pediatric_patients_hospitalized_confirmed_covid_7_day_avg', float),
      ('total_pediatric_patients_hospitalized_confirmed_covid_7_day_coverage',
       'total_pediatric_patients_hosp_confirmed_covid_7d_cov', int),
      ('total_pediatric_patients_hospitalized_confirmed_covid_7_day_sum',
       'total_pediatric_patients_hospitalized_confirmed_covid_7_day_sum', int),
      ('total_personnel_covid_vaccinated_doses_all_7_day',
       'total_personnel_covid_vaccinated_doses_all_7_day', int),
      ('total_personnel_covid_vaccinated_doses_all_7_day_sum',
       'total_personnel_covid_vaccinated_doses_all_7_day_sum', int),
      ('total_personnel_covid_vaccinated_doses_none_7_day',
       'total_personnel_covid_vaccinated_doses_none_7_day', int),
      ('total_personnel_covid_vaccinated_doses_none_7_day_sum',
       'total_personnel_covid_vaccinated_doses_none_7_day_sum', int),
      ('total_personnel_covid_vaccinated_doses_one_7_day',
       'total_personnel_covid_vaccinated_doses_one_7_day', int),
      ('total_personnel_covid_vaccinated_doses_one_7_day_sum',
       'total_personnel_covid_vaccinated_doses_one_7_day_sum', int),
      ('total_staffed_adult_icu_beds_7_day_avg', 'total_staffed_adult_icu_beds_7_day_avg', float),
      ('total_staffed_adult_icu_beds_7_day_coverage', 'total_staffed_adult_icu_beds_7_day_coverage',
       int),
      ('total_staffed_adult_icu_beds_7_day_sum', 'total_staffed_adult_icu_beds_7_day_sum', int),
      ('zip', 'zip', str),
  ]

  def __init__(self, *args, **kwargs):
    super().__init__(
        *args,
        **kwargs,
        table_name=Database.TABLE_NAME,
        columns_and_types=Database.ORDERED_CSV_COLUMNS)
