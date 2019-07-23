This repo contains Django ORM queries and SQL queries
for django documentation.

If you want to run this code. follow the instructions

```bash
cd django_documentation_project
pyenv install 3.7.2
pyenv local 3.7.2
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py shell_plus
```

#### Cheetsheet

link: https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#cheat-sheet

```python
Book.objects.aggregate(price_diff=Max('price') - Avg('price'))

SELECT CAST((CAST(MAX("library_book"."price") AS NUMERIC) - CAST(AVG("library_book"."price") AS NUMERIC)) AS NUMERIC) AS "price_diff"
  FROM "library_book";
```

```python
Book.objects.aggregate(price_diff=Max('price', output_field=FloatField()) - Avg('price', output_field=FloatField()))

SELECT (MAX("library_book"."price") - AVG("library_book"."price")) AS "price_diff"
  FROM "library_book";
```

```python
Publisher.objects.annotate(num_books=Count('book'))

SELECT "library_publisher"."id",
       "library_publisher"."name",
       COUNT("library_book"."id") AS "num_books"
  FROM "library_publisher"
  LEFT OUTER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 GROUP BY "library_publisher"."id",
          "library_publisher"."name"
 LIMIT 21
 ```

```python
below_4 = Count('book', filter=Q(book__rating__lte=4))
above_4 = Count('book', filter=Q(book__rating__gt=4))
Publisher.objects.annotate(below_4=below_4).annotate(above_4=above_4)

> SELECT "library_publisher"."id",
       "library_publisher"."name",
       COUNT(CASE WHEN "library_book"."rating" <= 4.0 THEN "library_book"."id" ELSE NULL END) AS "below_4",
       COUNT(CASE WHEN "library_book"."rating" > 4.0 THEN "library_book"."id" ELSE NULL END) AS "above_4"
  FROM "library_publisher"
  LEFT OUTER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 GROUP BY "library_publisher"."id",
          "library_publisher"."name"
 LIMIT 21;
 ```

```python
Publisher.objects.annotate(num_books=Count('book')).order_by('-num_books')[:5]

SELECT "library_publisher"."id",
       "library_publisher"."name",
       COUNT("library_book"."id") AS "num_books"
  FROM "library_publisher"
  LEFT OUTER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 GROUP BY "library_publisher"."id",
          "library_publisher"."name"
 ORDER BY "num_books" DESC
 LIMIT 5;
 ```

 ### Aggregate

 link: https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#generating-aggregates-over-a-queryset

```python
Book.objects.aggregate(avg_price=Avg('price', output_field=FloatField()))

SELECT AVG("library_book"."price") AS "avg_price"
  FROM "library_book"
```

```python
Book.objects.aggregate(Avg('price'), Max('price'), Min('price'))

SELECT CAST(AVG("library_book"."price") AS NUMERIC) AS "price__avg",
       CAST(MAX("library_book"."price") AS NUMERIC) AS "price__max",
       CAST(MIN("library_book"."price") AS NUMERIC) AS "price__min"
  FROM "library_book"
```

```python
Store.objects.aggregate(youngest_age=Min('books__authors__age'))

SELECT MIN("library_author"."age") AS "youngest_age"
  FROM "library_store"
  LEFT OUTER JOIN "library_store_books"
    ON ("library_store"."id" = "library_store_books"."store_id")
  LEFT OUTER JOIN "library_book"
    ON ("library_store_books"."book_id" = "library_book"."id")
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_book"."id" = "library_book_authors"."book_id")
  LEFT OUTER JOIN "library_author"
    ON ("library_book_authors"."author_id" = "library_author"."id")
```

### Small Difference between aggregate and annotate

```python
Store.objects.aggregate(min_price=Min('books__price'), max_price=Max('books__price'))

SELECT CAST(MIN("library_book"."price") AS NUMERIC) AS "min_price",
       CAST(MAX("library_book"."price") AS NUMERIC) AS "max_price"
  FROM "library_store"
  LEFT OUTER JOIN "library_store_books"
    ON ("library_store"."id" = "library_store_books"."store_id")
  LEFT OUTER JOIN "library_book"
    ON ("library_store_books"."book_id" = "library_book"."id")
```

```python
Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))

SELECT "library_store"."id",
       "library_store"."name",
       CAST(MIN("library_book"."price") AS NUMERIC) AS "min_price",
       CAST(MAX("library_book"."price") AS NUMERIC) AS "max_price"
  FROM "library_store"
  LEFT OUTER JOIN "library_store_books"
    ON ("library_store"."id" = "library_store_books"."store_id")
  LEFT OUTER JOIN "library_book"
    ON ("library_store_books"."book_id" = "library_book"."id")
 GROUP BY "library_store"."id",
          "library_store"."name"
 LIMIT 21
 ```

### Annotate

link: https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#generating-aggregates-for-each-item-in-a-queryset

```python
Book.objects.annotate(Count('authors'))

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       COUNT("library_book_authors"."author_id") AS "authors__count"
  FROM "library_book"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_book"."id" = "library_book_authors"."book_id")
 GROUP BY "library_book"."id",
          "library_book"."name",
          "library_book"."pages",
          "library_book"."price",
          "library_book"."rating",
          "library_book"."publisher_id",
          "library_book"."pubdate"
 LIMIT 21
 ```

### Multiple Aggregations

link: https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#combining-multiple-aggregations

 ```python
 Book.objects.annotate(Count('authors'), Count('store'))

 SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       COUNT("library_book_authors"."author_id") AS "authors__count",
       COUNT("library_store_books"."store_id") AS "store__count"
  FROM "library_book"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_book"."id" = "library_book_authors"."book_id")
  LEFT OUTER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 GROUP BY "library_book"."id",
          "library_book"."name",
          "library_book"."pages",
          "library_book"."price",
          "library_book"."rating",
          "library_book"."publisher_id",
          "library_book"."pubdate"
 LIMIT 21
 ```

 ```python
 Book.objects.annotate(Count('authors', distinct=True), Count('store', distinct=True))

 SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       COUNT(DISTINCT "library_book_authors"."author_id") AS "authors__count",
       COUNT(DISTINCT "library_store_books"."store_id") AS "store__count"
  FROM "library_book"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_book"."id" = "library_book_authors"."book_id")
  LEFT OUTER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 GROUP BY "library_book"."id",
          "library_book"."name",
          "library_book"."pages",
          "library_book"."price",
          "library_book"."rating",
          "library_book"."publisher_id",
          "library_book"."pubdate"
 LIMIT 21
 ```

### Traversing Relationship Backwards

 https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#following-relationships-backwards

```python
Author.objects.annotate(total_pages=Sum('book__pages'))

SELECT "library_author"."id",
       "library_author"."name",
       "library_author"."age",
       SUM("library_book"."pages") AS "total_pages"
  FROM "library_author"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_author"."id" = "library_book_authors"."author_id")
  LEFT OUTER JOIN "library_book"
    ON ("library_book_authors"."book_id" = "library_book"."id")
 GROUP BY "library_author"."id",
          "library_author"."name",
          "library_author"."age"
 LIMIT 21
```
### filter and exclude

https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#filter-and-exclude

```python
Book.objects.filter(name__startswith="Django").annotate(num_authors=Count('authors'))

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       COUNT("library_book_authors"."author_id") AS "num_authors"
  FROM "library_book"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_book"."id" = "library_book_authors"."book_id")
 WHERE "library_book"."name" LIKE 'Django%' ESCAPE '\'
 GROUP BY "library_book"."id",
          "library_book"."name",
          "library_book"."pages",
          "library_book"."price",
          "library_book"."rating",
          "library_book"."publisher_id",
          "library_book"."pubdate"
 LIMIT 21
```

```python
Book.objects.filter(name__icontains="interview").aggregate(Avg('price'))

SELECT CAST(AVG("library_book"."price") AS NUMERIC) AS "price__avg"
  FROM "library_book"
 WHERE "library_book"."name" LIKE '%interview%' ESCAPE '\'
 ```

```python
Book.objects.annotate(num_authors=Count('authors')).filter(num_authors__gt=1)

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       COUNT("library_book_authors"."author_id") AS "num_authors"
  FROM "library_book"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_book"."id" = "library_book_authors"."book_id")
 GROUP BY "library_book"."id",
          "library_book"."name",
          "library_book"."pages",
          "library_book"."price",
          "library_book"."rating",
          "library_book"."publisher_id",
          "library_book"."pubdate"
HAVING COUNT("library_book_authors"."author_id") > 1
 LIMIT 21
```

### Order of filter and exclude

https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#order-of-annotate-and-filter-clauses

```python
Publisher.objects.annotate(num_books=Count('book', distinct=True)).filter(book__rating__gt=3.0)

SELECT "library_publisher"."id",
       "library_publisher"."name",
       COUNT(DISTINCT "library_book"."id") AS "num_books"
  FROM "library_publisher"
  LEFT OUTER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 INNER JOIN "library_book" T3
    ON ("library_publisher"."id" = T3."publisher_id")
 WHERE T3."rating" > 3.0
 GROUP BY "library_publisher"."id",
          "library_publisher"."name"
 LIMIT 21
 ```

 ```python
 Publisher.objects.filter(book__rating__gt=3.0).annotate(num_books=Count('book'))

 SELECT "library_publisher"."id",
       "library_publisher"."name",
       COUNT("library_book"."id") AS "num_books"
  FROM "library_publisher"
 INNER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 WHERE "library_book"."rating" > 3.0
 GROUP BY "library_publisher"."id",
          "library_publisher"."name"
 LIMIT 21
 ```

 ```python
 Publisher.objects.filter(book__rating__gt=3.0).annotate(avg_rating=Avg('book__rating'))

SELECT "library_publisher"."id",
       "library_publisher"."name",
       AVG("library_book"."rating") AS "avg_rating"
  FROM "library_publisher"
 INNER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 WHERE "library_book"."rating" > 3.0
 GROUP BY "library_publisher"."id",
          "library_publisher"."name"
 LIMIT 21
 ```

### using values() with filter

https://docs.djangoproject.com/en/2.2/topics/db/aggregation/#values

 ```python
 Author.objects.values('name').annotate(average_rating=Avg('book__rating'))

 SELECT "library_author"."name",
       AVG("library_book"."rating") AS "average_rating"
  FROM "library_author"
  LEFT OUTER JOIN "library_book_authors"
    ON ("library_author"."id" = "library_book_authors"."author_id")
  LEFT OUTER JOIN "library_book"
    ON ("library_book_authors"."book_id" = "library_book"."id")
 GROUP BY "library_author"."name"
 LIMIT 21
 ```