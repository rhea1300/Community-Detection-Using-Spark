# install spark on your machine
# pip install findspark
# pip install pyspark
# pip install py4j


# spark setup
import pyspark
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from pyspark.ml.feature import MinHashLSH, VectorAssembler
from pyspark.ml.linalg import Vectors

# libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# create spark session, set config
#todo change config settings? maybe switch over to google collab 
spark = SparkSession.builder \
  .appName("DIS_project_5") \
  .master("local[*]") \
  .config("spark.driver.memory", "2G") \
  .config("spark.driver.maxResultSize", "2g") \
  .getOrCreate()
spark


# load data (it is automatically paralized so in RDD format)
path_data = "../data/small_test2_data.csv"
df = spark.read.format("csv").option("header", "true").load(path_data)
# df.show()
# df.printSchema()


# transform data into vector columns
#todo discuss shape of communities, how to implement it in the vector assembler
assembler = VectorAssembler(inputCols=["nodeNaam1", "nodeNaam2"], outputCol="features")
vector_df = assembler.transform(df)

# show vectorized data
# vector_df.select("id", "features").show()


# initialize MinHashLSH and fit the model
minhash = MinHashLSH(inputCol="features", outputCol="hashes", numHashTables=5)
model = minhash.fit(df)

# transform data and show hashes
transformed_df = model.transform(df)
transformed_df.show()

# find N nearest neighbors, by looping through each record in the data and finding the nearest neighbors for each record and saving them
for key in df:
  # key_ = key


# pass data of community and the nearest neighbor communities to Nils function
#todo add Nils function here
communities_similarity_scores = communities_nearest_neighbours.map()