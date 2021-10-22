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
    elevation_ft NUMERIC,
    continent varchar(256),
    iso_country varchar(256),
    iso_region varchar(256),
    municipality varchar(256),
    gps_code varchar(256),
    iata_code varchar(256),
    local_code varchar(256),
    coordinates varchar(256)
);