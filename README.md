# Capstone Project - Data Engineering Nanodegree Program

## Overview

The purpose of the data engineering capstone project is to combine and process big datasets using concepts and technologies learned throughout the nano degree program. We will use the Udacity provided project, containing four datasets: data on immigration to the United States, data on airport codes, U.S. city demographics and temperature data.

## Project Steps

### Scope the Project and Gather Data

#### Project scope

The main goal of the project is to develop a database holding data prepared to be anlyzed by data analysts and to answer for example questions about correlation between origin or nationality of the visitor and the demographics of the arriving city in the United States. Because we need to process millions of rows from different data sources we decided to use Amazon Redshift Data Warehouse for analysing data and Amazon S3 for long-term storing data. For the ETL pipeline we will use Apache Airflow (or Amazon Managed Workflows for Apache Airflow service in the AWS). For preprocessing the data, we will use Apache Spark and load the Date into S3 bucket in the AWS.

The Udacity provided project contains data on immigration to the United States, and supplementary datasets including data on airport codes, U.S. city demographics, and temperature data.

 - **I94 Immigration Data**:\
  This data comes from the US National Tourism and Trade Office: https://www.trade.gov/national-travel-and-tourism-office
 
 - **World Temperature Data**:\
  This dataset comes from Kaggle: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
 
 - **U.S. City Demographic Data**:\
  This data comes from OpenSoft: https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/
 
 - **Airport Code Table**:\
  This is a table of airport codes and corresponding cities: https://datahub.io/core/airport-codes#data

This project prepares only the data to answer the questions, the analysis of data is out of scope.

### Explore and Assess the Data

For more in-depth information about the data sets we refer to the _Capstone Project Template.ipynb_ Jupyter Notebook. In this file we check the data format, uniqueness and null values. So we drop columns with more than 90% null values and some id columns because they contain no useful information we needed.
In _Capstone Project SAS Labels.ipynb_ we are extracting various data from the provided I94_SAS_Labels_Descriptions.SAS file and store it in csv files.

### Define the Data Model

![ER Diagram](https://raw.githubusercontent.com/euweb/CapstoneProject/main/model.png)

We decided to use a star schema which is optimized for queries on the visitor analysis. 

In the visit table we extracted data from the immigration data set. The redundant columns _year_of_arrival_ and _month_of_arrival_ are used as partition key to unload the date to S3, so the data can be retrieved later using Amazon Athena.

To assign the right city to the port of arrival we used the date from the _airport code table_ dataset and only if information was missing we used the extracted data from SAS Label file.

### Run ETL to Model the Data

In `spark/convert_sas.py` we used Spark to preprocess SAS data for generating parquet files. It was necessary to whitelist the columns since there are additional columns for June 2016 and that's why Redshift COPY command didn't work.

![Airflow Pipeline Diagram](https://raw.githubusercontent.com/euweb/CapstoneProject/main/Airflow-Pipeline.png)

### Complete Project Write Up

After the ETL has processed the result following querry can be run against the model:

Show the count of visitors per year, month, country of citezenship and port of entry in the U.S. and additional demographics information of the port of entry.

```sql
select
    v.year_of_arrival,
    v.month_of_arrival,
    c.description as origin,
    v.visitors,
    p.city,
    p.state,
    pc.white,
    pc.american_indian_and_alaska_native,
    pc.hispanic_or_latino,
    pc.black_or_african_american,
    pc.asian
from
    (
        select
            year_of_arrival,
            month_of_arrival,
            country_of_citizenship as country,
            port_of_entry,
            count(country_of_citizenship) as visitors
        from
            visit
        group by
            year_of_arrival,
            month_of_arrival,
            country,
            port_of_entry
    ) as v
    join country_mapping c on c.id = v.country
    join port p on v.port_of_entry = p.port
    join port_city pc on pc.city = p.city
    and pc.state_code = p.state
limit
    100
```
After running the query you see this result:

![Example query result](https://raw.githubusercontent.com/euweb/CapstoneProject/main/example_query.png)


Description of how to approach the problem differently under the following scenarios:

  *  _If the data was increased by 100x._

     We are already prepared for it using partitioning for the large dataset (immigration data). For the preprocessing the data we would use AWS EMR to transform SAS data to Parquet format
  *  _If the pipelines were run on a daily basis by 7am._

     Apache Airflow allows scheduling of the DAG runs

  *  _If the database needed to be accessed by 100+ people._

     We would use AWS IAM to create users and roles to access data


## File list

| Name                              | Description                                                                        |
|-----------------------------------|------------------------------------------------------------------------------------|
| dags                              | folder containing the Apache Airflow dags                                          |
| docker/Dockerfile                 | Docker file for Apache Airflow base image                                          |
| plugins                           | folder containing all Apache Airflow plugin code                                   |
| source_data                       | folder containing data sets used in this project                                   |
| spark/convert_sas.py              | script to convert SAS files to Parquet format                                      |
| Capstone Project SAS Labels.ipynb | Jupyter notebook extracting data from the SAS labels and exporting it to csv files |
| Capstone Project Template.ipynb   | Jupyter notebook examining project data                                            |
| DataDictionary.md                 | description of the data                                                            |
| README.md                         | this documentation                                                                 |
| docker-compose.yaml               | Docker composer file to run Apache Airflow                                         |
| model.drawio                      | diagram of the data model                                                          |
| redshift_util.py                  | python script for creating and deleting redshift cluster                           |
