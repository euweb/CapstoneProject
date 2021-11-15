--- Staging tables

CREATE TABLE IF NOT EXISTS public.i94imm_staging (
  i94yr DOUBLE PRECISION,
  i94mon DOUBLE PRECISION,
  i94cit DOUBLE PRECISION,
  i94res DOUBLE PRECISION,
  i94port varchar(256),
  arrdate DOUBLE PRECISION,
  i94mode DOUBLE PRECISION,
  i94addr varchar(256),
  depdate DOUBLE PRECISION,
  i94bir DOUBLE PRECISION,
  i94visa DOUBLE PRECISION,
  dtadfile varchar(256),
  visapost varchar(256),
  occup varchar(256),
  entdepa varchar(256),
  entdepd varchar(256),
  entdepu varchar(256),
  matflag varchar(256),
  biryear DOUBLE PRECISION,
  dtaddto varchar(256),
  gender varchar(256),
  insnum varchar(256),
  airline varchar(256),
  fltno varchar(256),
  visatype varchar(256)
);

CREATE TABLE IF NOT EXISTS public.temperature_staging (
  dt varchar(256),
  AverageTemperature numeric(18,0),
  AverageTemperatureUncertainty numeric(18,0),
  City varchar(256),
  Country varchar(256),
  Latitude varchar(256),
  Longitude varchar(256)
);

CREATE TABLE IF NOT EXISTS public.us_cities_demographics_staging (
    city varchar(256),
    state varchar(256),
    median_age numeric(18,0),
    male_population INTEGER,
    female_population INTEGER,
    total_population INTEGER,
    number_of_veterans INTEGER,
    foreign_born INTEGER,
    average_household_size numeric(18,0),
    state_code varchar(256),
    race varchar(256),
    race_count INTEGER
);

CREATE TABLE IF NOT EXISTS public.airport_codes_staging (
    ident varchar(256),
    type varchar(256),
    name varchar(256),
    elevation_ft DOUBLE PRECISION,
    continent varchar(256),
    iso_country varchar(256),
    iso_region varchar(256),
    municipality varchar(256),
    gps_code varchar(256),
    iata_code varchar(256),
    local_code varchar(256),
    coordinates varchar(256)
);


-- model tables
CREATE TABLE IF NOT EXISTS public.visit (
  year_of_arrival SMALLINT,
  month_of_arrival SMALLINT,
  country_of_citizenship INTEGER,
  country_of_residence INTEGER,
  port_of_entry varchar(256),
  arrival_date DATE,
  arrivid_by INTEGER,
  state_of_arrival varchar(256),
  departure_date DATE,
  age SMALLINT,
  visa SMALLINT,
  birth_year SMALLINT,
  gender varchar(256),
  visatype varchar(256)
);

CREATE TABLE IF NOT EXISTS public.i94_cit_res_mapping (
  id INTEGER,
  description varchar(256)
);

CREATE TABLE IF NOT EXISTS public.i94port_mapping (
  id varchar(256),
  description varchar(256)
);

CREATE TABLE IF NOT EXISTS public.i94mode_mapping (
  id INTEGER,
  description varchar(256)
);

CREATE TABLE IF NOT EXISTS public.i94addr_mapping (
  id varchar(256),
  description varchar(256)
);

CREATE TABLE IF NOT EXISTS public.i94visa_mapping (
  id INTEGER,
  description varchar(256)
);

CREATE TABLE IF NOT EXISTS public.date (
  date DATE,
  day SMALLINT,
  week SMALLINT,
  month SMALLINT,
  year SMALLINT,
  weekday SMALLINT
);

CREATE TABLE IF NOT EXISTS public.port (
  port varchar(256),
  state varchar(256),
  city varchar(256)
);

CREATE TABLE IF NOT EXISTS public.temperature (
  dt varchar(256),
  AverageTemperature numeric(18,0),
  AverageTemperatureUncertainty numeric(18,0),
  City varchar(256),
  Country varchar(256),
  Latitude varchar(256),
  Longitude varchar(256)
);

CREATE TABLE IF NOT EXISTS public.port_city (
  city varchar(256),
  state varchar(256),
  median_age numeric(18,0),
  male_population INTEGER,
  female_population INTEGER,
  total_population INTEGER,
  number_of_veterans INTEGER,
  foreign_born INTEGER,
  average_household_size numeric(18,0),
  state_code varchar(256),
  white INTEGER,
  american_indian_and_alaska_native INTEGER,
  hispanic_or_latino INTEGER,
  black_or_african_american INTEGER,
  asian INTEGER
)
-- CREATE TABLE IF NOT EXISTS public.visapost ();

-- CREATE TABLE IF NOT EXISTS public.visatype ();

