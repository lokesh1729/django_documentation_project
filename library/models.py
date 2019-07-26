from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return "%s (%s)" % (self.name, self.age)

class Publisher(models.Model):
    name = models.CharField(max_length=300)
    city = models.ForeignKey(City, related_name="publishers", related_query_name="publisher", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.city.name)

class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name="books", related_query_name="book")
    pubdate = models.DateField()

    def __str__(self):
        return "%s (%s)" % (self.name, ", ".join(author.name for author in self.authors.all()))

class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return "%s (%s)" % (self.name, ", ".join(book.name for book in self.books.all()))
