from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to="author_images", blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        "core.Category", on_delete=models.CASCADE, related_name="books_category"
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField()
    image = models.ImageField(upload_to="book_images", blank=True)

    def __str__(self):
        return self.title


class BranchBook(models.Model):
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="book_branches"
    )
    branch = models.ForeignKey(
        "libraries.Branch", on_delete=models.CASCADE, related_name="branch_books"
    )
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.book.title + " - " + self.branch.library.name + " - "


class BorrowedBook(models.Model):
    TYPES = (("borrowed", "Borrowed"), ("returned", "Returned"))
    user = models.ForeignKey(
        "core.User", on_delete=models.CASCADE, related_name="borrowed_user"
    )
    book = models.ForeignKey(
        BranchBook, on_delete=models.CASCADE, related_name="borrowed_book"
    )
    status = models.CharField(max_length=10, choices=TYPES, default="borrowed")
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)
    overdue_days_penalty = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.book.book.title + " - " + self.user.email + " - " + self.status
