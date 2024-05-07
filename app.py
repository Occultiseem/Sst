from flask import Flask,render_template,request,Response,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_cors import *
from pyspark.sql.functions import col
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.types import StructType, StringType, IntegerType
from pyspark import SparkConf, SparkContext
from pyspark.sql import functions as F
import pandas as pd
import json

app = Flask(__name__)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

from pyspark.sql import SparkSession

# 创建 SparkSession 对象
spark = SparkSession.builder \
.appName("sst") \
.config("spark.driver.extraClassPath", "D:\\pycharm\\venv\\bigData\Lib\site-packages\mysql-connector-java-8.0.11.jar") \
.getOrCreate()

# pyspark连接数据库
def conn():

    # 连接本地spark
    spark = SparkSession .builder .appName("sst") .getOrCreate()
    # 初始化设置
    spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    sc = spark.sparkContext
    sc.setLogLevel("WARN")
    # 读取数据库表格，读取出来的数据类型是dataframe
    tableDF = spark.read.format("jdbc").option("url","jdbc:mysql://8.130.10.243:3306/test1").option("driver","com.mysql.cj.jdbc.Driver").option("dbtable", "sst1").option("user", "root").option("password", "Sst@0930").load()

    return tableDF


def preprocess(tableDF):
    # 数据预处理，去除重复值
    distinct_columns = ['answer_count', 'articles_count', 'gender', 'name']
    tableDF = tableDF.dropDuplicates(distinct_columns)
    return tableDF

# 发文数量统计
def get_articles(tableDF):

    table1 = tableDF.filter(tableDF['articles_count'] != 0)
    # 发文数量统计
    articles_count_result = table1.groupBy("articles_count").count().orderBy(col("articles_count"))

    # 通过pandas格式转换为list
    articles_count = articles_count_result.toPandas()
    articles_column = articles_count.columns.tolist()
    articles_value = articles_count.values.tolist()
    return articles_column, articles_value


# 性别数量统计
def get_sex(tableDF):

    # 性别数量统计
    gender_result = tableDF.groupBy("gender").count().orderBy(col("count").desc())
    gender_count = gender_result.toPandas()
    gender = gender_count.values.tolist()

    return gender


# 回答问题数量统计
def get_answer(tableDF):
    table1 = tableDF.filter(tableDF['answer_count'] != 0)
    # 回答问题数量统计
    answer_count_result = table1.groupBy("answer_count").count().orderBy(col("answer_count"))
    # 通过pandas格式转换为list
    answer_count = answer_count_result.toPandas()
    answer_column = answer_count.columns.tolist()
    answer_value = answer_count.values.tolist()

    return answer_column, answer_value

# 姓名中姓的数量统计
def get_name(tableDF):

    # 姓名中姓的词频统计
    name_result = tableDF.select(F.substring(tableDF.name, 0, 1).alias("name_first"))
    name_first_result = name_result.groupBy("name_first").count()
    name_first = name_first_result.toPandas()
    name = name_first.values.tolist()

    return name


@app.route('/')
def index():

    # 建立连接
    df = conn()
    # 数据预处理
    df = preprocess(df)
    # 发文数量统计
    articles_column, articles_value = get_articles(df)
    # 性别数量统计
    gender = get_sex(df)
    # 回答问题数量统计
    answer_column, answer_value = get_answer(df)
    # 姓名中姓的统计
    name = get_name(df)


    return render_template("index.html",
                           articles_column=articles_column, articles_value=articles_value,
                           gender=gender,
                           answer_column=answer_column, answer_value=answer_value,
                           name=name)  # 加入变量传递


if __name__ == '__main__':

    app.run(debug=True, host='127.0.0.1', port=5000)
