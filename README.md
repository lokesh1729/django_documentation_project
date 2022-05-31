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

# select_related

 https://docs.djangoproject.com/en/2.2/ref/models/querysets/#select-related

 ```python
 Book.objects.select_related('publisher').get(id=5)

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       "library_publisher"."id",
       "library_publisher"."name"
  FROM "library_book"
 INNER JOIN "library_publisher"
    ON ("library_book"."publisher_id" = "library_publisher"."id")
 WHERE "library_book"."id" = 5

 ```

## order of filter and select_related doesn't matter
```python
Book.objects.filter(name__icontains="coding").select_related('publisher')

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       "library_publisher"."id",
       "library_publisher"."name"
  FROM "library_book"
 INNER JOIN "library_publisher"
    ON ("library_book"."publisher_id" = "library_publisher"."id")
 WHERE "library_book"."name" LIKE '%coding%' ESCAPE '\'
 LIMIT 21

 ```

## follow multiple foreignkey

```python
Book.objects.select_related("publisher__city")

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate",
       "library_publisher"."id",
       "library_publisher"."name",
       "library_publisher"."city_id",
       "library_city"."id",
       "library_city"."name"
  FROM "library_book"
 INNER JOIN "library_publisher"
    ON ("library_book"."publisher_id" = "library_publisher"."id")
  LEFT OUTER JOIN "library_city"
    ON ("library_publisher"."city_id" = "library_city"."id")
 LIMIT 21
```

*multiple arguments can be passed, if nothing passed, relationships are automatically resolved*

### import note about select_related
> :warning: select_related works by creating an SQL join and including the fields of the related object in the SELECT statement. For this reason, select_related gets the related objects in the same database query

select_related is limited to single-valued relationships - foreign key and one-to-one.

## Using select_related and annotate

### inefficient query

```python
In [1]: Publisher.objects.filter(book__rating__gt=3.0).annotate(avg_rating=Avg('book__rating'))
Out[1]: SELECT "library_publisher"."id",
       "library_publisher"."name",
       "library_publisher"."city_id",
       AVG("library_book"."rating") AS "avg_rating"
  FROM "library_publisher"
 INNER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
 WHERE "library_book"."rating" > 3.0
 GROUP BY "library_publisher"."id",
          "library_publisher"."name",
          "library_publisher"."city_id"
 LIMIT 21


Execution time: 0.001944s [Database: default]

SELECT "library_city"."id",
       "library_city"."name"
  FROM "library_city"
 WHERE "library_city"."id" = 1


Execution time: 0.001033s [Database: default]

SELECT "library_city"."id",
       "library_city"."name"
  FROM "library_city"
 WHERE "library_city"."id" = 1


Execution time: 0.000071s [Database: default]

SELECT "library_city"."id",
       "library_city"."name"
  FROM "library_city"
 WHERE "library_city"."id" = 2


Execution time: 0.000061s [Database: default]

<QuerySet [<Publisher: mcgrawhill (Hyderabad)>, <Publisher: penguin (Hyderabad)>, <Publisher: pearson (Bangalore)>]>
```

### efficient query
```python
In [2]: Publisher.objects.select_related('city').filter(book__rating__gt=3.0).annotate(avg_rating=Avg('book__rating'))
Out[2]: SELECT "library_publisher"."id",
       "library_publisher"."name",
       "library_publisher"."city_id",
       AVG("library_book"."rating") AS "avg_rating",
       "library_city"."id",
       "library_city"."name"
  FROM "library_publisher"
 INNER JOIN "library_book"
    ON ("library_publisher"."id" = "library_book"."publisher_id")
  LEFT OUTER JOIN "library_city"
    ON ("library_publisher"."city_id" = "library_city"."id")
 WHERE "library_book"."rating" > 3.0
 GROUP BY "library_publisher"."id",
          "library_publisher"."name",
          "library_publisher"."city_id",
          "library_city"."id",
          "library_city"."name"
 LIMIT 21


Execution time: 0.000227s [Database: default]

<QuerySet [<Publisher: mcgrawhill (Hyderabad)>, <Publisher: pearson (Bangalore)>, <Publisher: penguin (Hyderabad)>]>
```


# prefetch_related

https://docs.djangoproject.com/en/2.2/ref/models/querysets/#prefetch-related

prefetch_related, on the other hand, does a separate lookup for each
relationship, and does the ‘joining’ in Python. This allows it to prefetch
many-to-many and many-to-one objects, which cannot be done using
select_related, in addition to the foreign key and one-to-one relationships
that are supported by select_related

## without prefetch_related

```python
books = Book.objects.all()

books[0]

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 LIMIT 1


Execution time: 0.001059s [Database: default]

Out[2]: SELECT "library_author"."id",
       "library_author"."name",
       "library_author"."age"
  FROM "library_author"
 INNER JOIN "library_book_authors"
    ON ("library_author"."id" = "library_book_authors"."author_id")
 WHERE "library_book_authors"."book_id" = 1


Execution time: 0.001554s [Database: default]

<Book: My Experiences of Coding Interview (Lokesh, Brahmareddy)>
```

```python
In [4]: books = Book.objects.prefetch_related('authors').all()

In [5]: books
Out[5]: SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 LIMIT 21


Execution time: 0.000184s [Database: default]

SELECT ("library_book_authors"."book_id") AS "_prefetch_related_val_book_id",
       "library_author"."id",
       "library_author"."name",
       "library_author"."age"
  FROM "library_author"
 INNER JOIN "library_book_authors"
    ON ("library_author"."id" = "library_book_authors"."author_id")
 WHERE "library_book_authors"."book_id" IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)


Execution time: 0.000329s [Database: default]

<QuerySet [<Book: My Experiences of Coding Interview (Lokesh, Brahmareddy)>, <Book: Cracking Coding Interview (Ganesh, Aneesh, Mahesh)>, <Book: My Experiences of Coding Interview2 (Brahmareddy, Suresh, Ramakrishna)>, <Book: My Experiences of Coding Interview3 (Lokesh, Ganesh, Aneesh, Mahesh)>, <Book: My Experiences of Coding Interview4 (Siddarth, Ganesh, Suresh)>, <Book: My Experiences of Coding Interview5 (Lokesh, Siddarth, Aneesh, Ramakrishna)>, <Book: My Experiences of Coding Interview6 (Lokesh, Brahmareddy, Siddarth, Suresh)>, <Book: My Experiences of Coding Interview7 (Siddarth, Ganesh, Ramakrishna)>, <Book: My Experiences of Coding Interview8 (Brahmareddy, Aneesh, Mahesh)>, <Book: My Experiences of Coding Interview9 (Ramakrishna, Mahesh)>, <Book: My Experiences of Coding Interview10 (Mahesh)>]>
```

## following multiple relations

```python
In [7]: stores = Store.objects.prefetch_related('books__authors')

In [8]: stores
Out[8]: SELECT "library_store"."id",
       "library_store"."name"
  FROM "library_store"
 LIMIT 21


Execution time: 0.000251s [Database: default]

SELECT ("library_store_books"."store_id") AS "_prefetch_related_val_store_id",
       "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 INNER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 WHERE "library_store_books"."store_id" IN (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)


Execution time: 0.000238s [Database: default]

SELECT ("library_book_authors"."book_id") AS "_prefetch_related_val_book_id",
       "library_author"."id",
       "library_author"."name",
       "library_author"."age"
  FROM "library_author"
 INNER JOIN "library_book_authors"
    ON ("library_author"."id" = "library_book_authors"."author_id")
 WHERE "library_book_authors"."book_id" IN (1, 3, 5, 8, 10, 4, 6, 9, 7, 11)


Execution time: 0.000307s [Database: default]
```

# prefetch vs without prefetch

## without prefetch

without prefetch_related, for each store it makes JOIN with `library_store_books`

 ```python
 In [18]: Store.objects.annotate(min_price=Min('books__price'), max_price=Max('books__price'))
Out[18]: SELECT "library_store"."id",
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


Execution time: 0.000205s [Database: default]

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 INNER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 WHERE "library_store_books"."store_id" = 1


Execution time: 0.000229s [Database: default]

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 INNER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 WHERE "library_store_books"."store_id" = 2


Execution time: 0.000089s [Database: default]

SELECT "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 INNER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 WHERE "library_store_books"."store_id" = 3


Execution time: 0.000080s [Database: default]

Execution time: 0.000088s [Database: default]

<QuerySet [<Store: store1 (My Experiences of Coding Interview, My Experiences of Coding Interview2, My Experiences of Coding Interview4, My Experiences of Coding Interview7, My Experiences of Coding Interview9)>, <Store: store2 (My Experiences of Coding Interview3, My Experiences of Coding Interview4, My Experiences of Coding Interview5, My Experiences of Coding Interview7, My Experiences of Coding Interview8)>, <Store: store3 (My Experiences of Coding Interview2, My Experiences of Coding Interview6, My Experiences of Coding Interview9, My Experiences of Coding Interview10)>]>
 ```
 
 ## with prefetch

 ```python
 In [19]: Store.objects.prefetch_related('books').annotate(min_price=Min('books__price'), max_price=Max('books__price'))
Out[19]: SELECT "library_store"."id",
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


Execution time: 0.000107s [Database: default]

SELECT ("library_store_books"."store_id") AS "_prefetch_related_val_store_id",
       "library_book"."id",
       "library_book"."name",
       "library_book"."pages",
       "library_book"."price",
       "library_book"."rating",
       "library_book"."publisher_id",
       "library_book"."pubdate"
  FROM "library_book"
 INNER JOIN "library_store_books"
    ON ("library_book"."id" = "library_store_books"."book_id")
 WHERE "library_store_books"."store_id" IN (1, 2, 3, 4, 5)


Execution time: 0.000353s [Database: default]

<QuerySet [<Store: store1 (My Experiences of Coding Interview, My Experiences of Coding Interview2, My Experiences of Coding Interview4, My Experiences of Coding Interview7, My Experiences of Coding Interview9)>, <Store: store2 (My Experiences of Coding Interview3, My Experiences of Coding Interview4, My Experiences of Coding Interview5, My Experiences of Coding Interview7, My Experiences of Coding Interview8)>, <Store: store3 (My Experiences of Coding Interview2, My Experiences of Coding Interview6, My Experiences of Coding Interview9, My Experiences of Coding Interview10)>, <Store: store4 (My Experiences of Coding Interview, My Experiences of Coding Interview2, My Experiences of Coding Interview3, My Experiences of Coding Interview5, My Experiences of Coding Interview6)>, <Store: store5 (My Experiences of Coding Interview2, My Experiences of Coding Interview3, My Experiences of Coding Interview5, My Experiences of Coding Interview6, My Experiences of Coding Interview10)>]>
```
