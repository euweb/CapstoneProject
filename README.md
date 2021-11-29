# Capstone Project - Data Engineering Nanodegree Program

## Overview

The purpose of the data engineering capstone project is to combine and process big datasets using concepts and technologies learned throughout the nano degree program. We will use the Udacity provided project, containing four datasets: data on immigration to the United States, data on airport codes, U.S. city demographics and temperature data.

## Project Steps

### Scope the Project and Gather Data

#### Project scope

The main goal of the project is to develop a database holding data prepared to be anlysed by data analysts and to answer for example questions about corelation between origin or nationality of the vistior and the demographics of the arriving city in the United States. Because we need to process millions of rows from diffirent data sources we decided to use Amazon Redshift Data Warehouse. For the ETL pipeline we will use Apache Airflow.

We decided us to use the Udacity provided project containing data on immigration to the United States, and supplementary datasets including data on airport codes, U.S. city demographics, and temperature data.

 - **I94 Immigration Data**:\
  This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. This is where the data comes from. There's a sample file so you can take a look at the data in csv format before reading it all in. You do not have to use the entire dataset, just use what you need to accomplish the goal you set at the beginning of the project.
 
 - **World Temperature Data**:\
  This dataset came from Kaggle: https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data
 
 - **U.S. City Demographic Data**:\
  This data comes from OpenSoft: https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/
 
 - **Airport Code Table**:\
  This is a simple table of airport codes and corresponding cities: https://datahub.io/core/airport-codes#data

This project prepares only the data for possible analysis of it. The analysis itself is out of scope.

### Explore and Assess the Data

For more in-depth information about the data sets we refer to the _Capstone Project Template.ipynb_ Jupyter Notebook. In this file we check the data format, uniqueness and null values. So we drop columns with more than 90% null values and some id columns because they contain no usefull information we needed.
In _Capstone Project SAS Labels.ipynb_ we extracting various data from the provided I94_SAS_Labels_Descriptions.SAS file and store it to csv files.

### Define the Data Model

![ER Diagram](https://raw.githubusercontent.com/euweb/CapstoneProject/main/model.png)

We decided to use a star schema which is optimized for queries on the visitor analysis. 

In the visit table we extracted data from the immigration data set. The redundand columns _year_of_arrival_ and _month_of_arrival_ are used as partition key to unload the date to S3, so the data can be retrieved later using Amazon Athena.

To assign the right city to the port of arrival we used the date from the _airport code tabele_ dataset and only if information was missing we used the extracted data from SAS Label file.

### Run ETL to Model the Data

In `spark/convert_sas.py` we used Spark to preprocess SAS data for generating parquet files. It was nessesary to whitelist the columns since there are additional columns for june 2016 and that's why Redshift COPY command didn't work.

![Airflow Pipeline Diagram](https://raw.githubusercontent.com/euweb/CapstoneProject/main/Airflow-Pipeline.png)

### Complete Project Write Up

Description of how to approach the problem differently under the following scenarios:

  *  _If the data was increased by 100x._

     We are already prepared for it using partitioning for the large dataset (immigration data). For the preprocessing the data we would use AWS EMR to transform SAS data to Parquet format
  *  _If the pipelines were run on a daily basis by 7am._

     Apache Airflow allowes scheduling of the DAG runs

  *  _If the database needed to be accessed by 100+ people._

     We would using AWS IAM to create users and roles to acccess data


## File list

