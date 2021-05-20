import operator
from celery import shared_task
from contextlib import closing
from django.db.models import Q
from functools import reduce

from .models import Entry, ForbiddenWord


@shared_task
def delete_harmful_entries():
    words = list(ForbiddenWord.objects.values_list('word', flat=True))
    Entry.objects.filter(reduce(operator.or_, (Q(text__contains=x) for x in words))).delete()
