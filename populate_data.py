import datetime
import os

import django

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_documentation_project.settings")
    django.setup()
    from library.models import Author, Book, Publisher, Store, City
    from weblog.models import BlogAuthor, Blog, Entry
except django.core.exceptions.ImproperlyConfigured as exc:
    raise exc


def populate_data():
    # Cities
    city = City.objects.create(name="Hyderabad")
    city2 = City.objects.create(name="Bangalore")

    # Authors
    author = Author.objects.create(name="Lokesh", age=25)
    author2 = Author.objects.create(name="Brahmareddy", age=26)
    author3 = Author.objects.create(name="Siddarth", age=28)
    author4 = Author.objects.create(name="Ganesh", age=29)
    author5 = Author.objects.create(name="Suresh", age=39)
    author6 = Author.objects.create(name="Aneesh", age=29)
    author7 = Author.objects.create(name="Ramakrishna", age=30)
    author8 = Author.objects.create(name="Mahesh", age=32)
    
    # Publishers
    publisher = Publisher.objects.create(name="mcgrawhill", city=city)
    publisher2 = Publisher.objects.create(name="pearson", city=city2)
    publisher3 = Publisher.objects.create(name="penguin", city=city2)
    publisher4 = Publisher.objects.create(name="macmillan", city=city)
    publisher5 = Publisher.objects.create(name="cambridge", city=city2)

    # Books
    book = Book.objects.create(name="My Experiences of Coding Interview", pages=250, price=254.56, rating=4.5, publisher=publisher, pubdate=datetime.date(2019, 3, 23))
    book.authors.add(author, author2)

    book1 = Book.objects.create(name="Cracking Coding Interview", pages=350, price=354.56, rating=3.5, publisher=publisher2, pubdate=datetime.date(2019, 2, 12))
    book1.authors.add(author8, author4, author6)

    book2 = Book.objects.create(name="My Experiences of Coding Interview2", pages=1250, price=1254.56, rating=3.0, publisher=publisher3, pubdate=datetime.date(2019, 4, 25))
    book2.authors.add(author2, author7, author5, author2)

    book3 = Book.objects.create(name="My Experiences of Coding Interview3", pages=824, price=828.56, rating=3.4, publisher=publisher3, pubdate=datetime.date(2018, 12, 22))
    book3.authors.add(author, author8, author4, author6)

    book4 = Book.objects.create(name="My Experiences of Coding Interview4", pages=852, price=248.56, rating=2.5, publisher=publisher2, pubdate=datetime.date(2017, 11, 21))
    book4.authors.add(author3, author4, author5)

    book5 = Book.objects.create(name="My Experiences of Coding Interview5", pages=248, price=353.56, rating=4.0, publisher=publisher3, pubdate=datetime.date(2018, 10, 12))
    book5.authors.add(author, author3, author6, author7)

    book6 = Book.objects.create(name="My Experiences of Coding Interview6", pages=476, price=854.56, rating=4.2, publisher=publisher, pubdate=datetime.date(2019,1,23))
    book6.authors.add(author, author2, author3, author5)

    book7 = Book.objects.create(name="My Experiences of Coding Interview7", pages=850, price=854.56, rating=3.8, publisher=publisher2, pubdate=datetime.date(2018, 7, 28))
    book7.authors.add(author3, author4, author7)

    book8 = Book.objects.create(name="My Experiences of Coding Interview8", pages=283, price=248.234, rating=4.5, publisher=publisher3, pubdate=datetime.date(2016, 2, 22))
    book8.authors.add(author2, author6, author8)

    book9 = Book.objects.create(name="My Experiences of Coding Interview9", pages=384, price=254.56, rating=3.2, publisher=publisher, pubdate=datetime.date(2018, 12, 18))
    book9.authors.add(author7, author8)

    book10 = Book.objects.create(name="My Experiences of Coding Interview10", pages=923, price=914.56, rating=3.7, publisher=publisher2, pubdate=datetime.date(2018, 11, 12))
    book10.authors.add(author8)

    # stores

    store = Store.objects.create(name="store1")
    store.books.add(book, book2, book4, book7, book9)

    store1 = Store.objects.create(name="store2")
    store1.books.add(book3, book4, book5, book7, book8)

    store3 = Store.objects.create(name="store3")
    store3.books.add(book2, book6, book9, book10)

    store4 = Store.objects.create(name="store4")
    store4.books.add(book, book2, book3, book5, book6)

    store5 = Store.objects.create(name="store5")
    store5.books.add(book3, book2, book5, book6, book10)

    store6 = Store.objects.create(name="store6")
    store6.books.add(book, book2, book3, book5, book9)

    store7 = Store.objects.create(name="store7")
    store7.books.add(book, book2, book4)

    store8 = Store.objects.create(name="store8")
    store8.books.add(book3, book2, book8, book9)

    store9 = Store.objects.create(name="store9")
    store9.books.add(book, book2, book8, book5, book6)

    store10 = Store.objects.create(name="store10")
    store10.books.add(book, book4, book6, book8)

    store11 = Store.objects.create(name="store11")
    store11.books.add(book, book9)

    store12 = Store.objects.create(name="store12")
    store12.books.add(book, book2, book8, book10)

    store13 = Store.objects.create(name="store13")
    store13.books.add(book, book2, book9)

    store14 = Store.objects.create(name="store14")
    store14.books.add(book, book2)

    store15 = Store.objects.create(name="store15")
    store15.books.add(book9)

    store16 = Store.objects.create(name="store16")
    store16.books.add(book10)


if __name__ == "__main__":
    print("populating data...")
    populate_data()
    print("populated data into models")
