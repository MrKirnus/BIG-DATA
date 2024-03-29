# -*- coding: utf-8 -*-


#Pandas
"""

import pandas as pd

"""## 1) Загрузите в колаб файлы по оценкам (ratings) и фильмам (movies) и создайте на их основе pandas-датафреймы"""

ratings = pd.read_csv("ratings.csv", sep = '\t', header = None, names= ["user_id", "item_id", "rating", "timestamp"])
ratings.head()

movies = pd.read_csv("movies.csv", sep = '|', encoding = 'ISO-8859-1', header = None, names= ["movie id", "movie title", "release date", "video release date", "IMDb URL", "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"])
movies.head()

"""## 2) Средствами Pandas, используя dataframe ratings, найдите id пользователя, поставившего больше всего оценок"""

ratings.groupby(['user_id'])['rating'].count().nlargest(1)

ratings[['user_id', 'rating']].groupby(['user_id']).count().sort_values(by='rating', ascending=False).head()

"""## 3) Оставьте в датафрейме ratings только те фильмы, который оценил данный пользователь

**Формируем новый датафрейм с пользователем, который оставил больше всего оценок**
"""

r_filtered = ratings[ratings.user_id == 405]
r_filtered.head()

"""## 4) Добавьте к датафрейму из задания 3 столбцы

**Добавляем столбец с суммарной оценкой от всех пользователей**
"""

rs = ratings.groupby(['item_id']).sum()
rs.head()

"""**Переименовываем столбец для удобства**



"""

rs.rename(columns = {'rating' : 'sum'}, inplace = True)
rs.head()

"""**Добавляем столбец с общим количеством оценок от всех пользователей**"""

rc = ratings.groupby(['item_id']).count()
rc.head()

"""**Переименовываем столбец для удобства**"""

rc.rename(columns = {'rating' : 'count'}, inplace = True)
rc.head()

"""**Добавляем к датафрейму с одним пользователем таблицы с суммой и количеством**"""

r_rs = r_filtered.merge(rs, how = 'inner', left_on ='item_id', right_on ='item_id')
r_rs.head()

r_rs_rc = r_rs.merge(rc, how = 'inner', left_on = 'item_id', right_on = 'item_id')
r_rs_rc.head()

"""**Объединяем таблицы с рейтингами и фильмами**"""

r_merge = r_rs_rc.merge(movies, how = 'inner', left_on = 'item_id', right_on = 'movie id')
r_merge.head()

"""**Удаляем лишние колонки**"""

r_df = r_merge.drop(columns = ['user_id_y', 'timestamp_y', 'user_id', 'timestamp', 'movie id', 'video release date'], axis = 1)
r_df.head()

"""**Выделяем год из даты релиза**"""

r_df['year'] = pd.DatetimeIndex(r_df['release date']).year
r_df.head()

r_df.info()

r_df.columns

"""## 5) Сформируйте X_train, X_test, y_train, y_test

**Формируем X_train, X_test, y_train, y_test**
"""

X, y = r_df[["year", "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "sum", "count"]], r_df['rating']

from sklearn.model_selection import train_test_split

"""**Разделяем наши данные на данные для обучения и тестирования**"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

X_test.head(2)

"""## 6) Возьмите модель линейной регрессии (или любую другую для задачи регрессии)  и обучите ее на фильмах"""

from sklearn.linear_model import LinearRegression

model = LinearRegression()

"""**Обучаем модель**"""

model.fit(X_train, y_train)

"""## 7) Оцените качество модели на X_test, y_test при помощи метрик для задачи регрессии"""

from sklearn.metrics import mean_squared_error

"""**Оцениваем качество модели**"""

mean_squared_error(y_test, model.predict(X_test))

mean_squared_error(y_train, model.predict(X_train))

"""#pySpark"""

!apt-get update

!apt-get install openjdk-8-jdk-headless -qq > /dev/null

!wget -q https://downloads.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop2.7.tgz

!tar -xvf spark-3.2.1-bin-hadoop2.7.tgz

!pip install -q findspark

import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.2.1-bin-hadoop2.7"

import findspark
findspark.init()
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[*]").getOrCreate()
sc = spark.sparkContext

"""## 8) Загрузить данные в spark

Загружаем таблицу с рейтингом
"""

py_r = spark.read.csv('ratings.csv', sep = '\t', inferSchema=True, header=None)
py_r = py_r.toDF("user_id", "item_id", "rating", "timestamp")
py_r.show(5)

"""Загружаем таблицу с фильмами"""

py_m = spark.read.csv('movies.csv', sep = '|', inferSchema=True, encoding = 'ISO-8859-1', header = None)
py_m = py_m.toDF("movie_id", "movie title", "release date", "video release date", "IMDb URL", "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western")
py_m.show(5)

"""## 9) Средствами спарка вывести среднюю оценку для каждого фильма"""

py_r.groupBy("item_id").avg("rating").show()

"""## 10) Посчитайте средствами спарка среднюю оценку для каждого жанра

Объединяем таблицы с рейтингами и фильмами
"""

py_join = py_r.join(py_m, py_r.item_id == py_m.movie_id, "outer")
py_join.show(5)

from pyspark.sql.functions import col

for i in "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western":
 print([py_join.groupBy(i).avg("rating").filter(col(i) == 1).show()], end='')

"""## 11) В спарке получить 2 датафрейма с 5-ю самыми популярными и самыми непопулярными фильмами (по количеству оценок, либо по самой оценке - на Ваш выбор)

5 самых популярных фильмов по количеству оценок
"""

popular = py_join.groupBy("item_id", "movie title").count().orderBy(['count'], ascending = [False])
popular.show(5)

"""5 самых непопулярных фильмов по количеству оценок"""

popular = py_join.groupBy("item_id", "movie title").count().orderBy(['count'], ascending = [True])
popular.show(5)
