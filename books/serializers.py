from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Author, Book, BorrowedBook
from core.serializers import CategorySerializer
from django.utils import timezone
from .tasks import send_email
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class AuthorSerializer(serializers.ModelSerializer):
    book_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "book_count", "image", "bio"]


class BookSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Book
        exclude = ["author", "category"]


class BookListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = ["title", "image", "category"]


class AuthorDetailSerializer(serializers.ModelSerializer):
    books = BookListSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books", "image", "bio"]


class BorrowedBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = BorrowedBook
        fields = [
            "id",
            "book_id",
            "status",
            "borrowed_date",
            "returned_date",
            "overdue_days_penalty",
            "user_id",
        ]
        read_only_fields = [
            "user_id",
            "id",
            "status",
            "borrowed_date",
            "overdue_days_penalty",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        if BorrowedBook.objects.filter(user=user, status="borrowed").count() == 3:
            raise serializers.ValidationError(
                {
                    "message": _(
                        "You cannot borrow more than 3 books or return one to borrow another"
                    )
                }
            )
        if BorrowedBook.objects.filter(
            book=validated_data.get("book"), status="borrowed"
        ).exists():
            raise serializers.ValidationError(
                {"message": _("You cannot borrow the same book twice")}
            )

        if BorrowedBook.objects.filter(
            book=validated_data.get("book"), book__quantity=0
        ).exists():
            raise serializers.ValidationError(
                {"message": _("This book is out of stock")}
            )
        return_date = validated_data.get("returned_date")
        if return_date and return_date < timezone.now():
            raise serializers.ValidationError(
                {"returned_date": _("Return date cannot be before borrowed date")}
            )

        if return_date and (
            return_date > timezone.now()
            and return_date > timezone.now() + timezone.timedelta(days=30)
        ):
            raise serializers.ValidationError(
                {"returned_date": _("Return date cannot be after 30 days")}
            )

        user = self.context["request"].user
        branch_book = BorrowedBook.objects.create(**validated_data)
        branch_book.book.quantity -= 1
        send_email(user.id, _("borrowing"))
        return branch_book

    def update(self, instance, validated_data):
        instance.status = _("returned")
        if instance.returned_date < timezone.now():
            instance.overdue_days_penalty = (
                (timezone.now() - instance.returned_date).days
            ) * 10
        instance.save()
        instance.book.quantity += 1
        instance.book.save()
        send_email(instance.user.id, _("returning"))
        send_notification_to_user(
            instance.user.id, _("You have successfully returned a book")
        )
        return instance


def send_notification_to_user(user_id, message):
    channel_layer = get_channel_layer()
    group_name = f"user_{user_id}"

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_notification",
            "message": message,
        },
    )
