import findspark
import os
from pyspark.sql import SparkSession

findspark.init()

host="127.0.0.1"

spark = SparkSession.builder\
    .master("local[*]")\
    .config("spark.jars.packages","saurfang:spark-sas7bdat:3.0.0-s_2.12")\
    .config("spark.driver.bindAddress",host)\
    .config("spark.driver.host",host)\
    .config("spark.sql.debug.maxToStringFields", 1000)\
    .enableHiveSupport().getOrCreate()

root_dir = "data/input/18-83510-I94-Data-2016/"

columns = [
  "i94yr",
  "i94mon",
  "i94cit",
  "i94res",
  "i94port",
  "arrdate",
  "i94mode",
  "i94addr",
  "depdate",
  "i94bir",
  "i94visa",
  "dtadfile",
  "visapost",
  "occup",
  "entdepa",
  "entdepd",
  "entdepu",
  "matflag",
  "biryear",
  "dtaddto",
  "gender",
  "insnum",
  "airline",
  "fltno",
  "visatype"
]

for root, subdirs, files in os.walk(root_dir):
    for name in files:
      file_name = os.path.join(root, name)
      print(file_name)
      df_spark =spark.read.format('com.github.saurfang.sas.spark').load(file_name)
      # df_spark.write.mode("append").partitionBy("i94yr","i94mon").parquet("data3/parquet")
      df_spark.select(*columns).write.mode("append").parquet("data/parquet")