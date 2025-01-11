from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Author, Book, BranchBook
from django.core.cache import cache

@receiver(post_save, sender=Author)
@receiver(post_save, sender=Book)
@receiver(post_save, sender=BranchBook)
@receiver(post_delete, sender=Author)
@receiver(post_delete, sender=Book)
@receiver(post_delete, sender=BranchBook)
def invalidate_author_list_cache(sender, **kwargs):
    cache_keys = cache.keys("author_list")
    for key in cache_keys:
        cache.delete(key)

@receiver(post_save, sender=Author)
@receiver(post_save, sender=Book)
@receiver(post_save, sender=BranchBook)
@receiver(post_delete, sender=Author)
@receiver(post_delete, sender=Book)
@receiver(post_delete, sender=BranchBook)
def invalidate_author_detail_cache(sender, instance, **kwargs):
    cache_key = f"author_detail_list"
    cache.delete(cache_key)

@receiver(post_save, sender=Book)
@receiver(post_delete, sender=Book)
def invalidate_book_list_cache(sender, **kwargs):
    cache_keys = cache.keys("book_list")
    for key in cache_keys:
        cache.delete(key)
