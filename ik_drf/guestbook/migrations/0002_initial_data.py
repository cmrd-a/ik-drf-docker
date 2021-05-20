# Generated by Django 3.2.3 on 2021-05-18 23:03

from django.db import migrations


def forwards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Entry = apps.get_model('guestbook', 'Entry')
    Like = apps.get_model('guestbook', 'Like')
    ForbiddenWord = apps.get_model('guestbook', 'ForbiddenWord')

    admin = User.objects.create_superuser(username='admin', password='admin')
    just_user = User.objects.create(username='user', password='user')

    texts = ['a', 'b', 'c', 'f-word', 'n-word']
    entries = [Entry(user=admin, text=text) for text in texts]
    Entry.objects.bulk_create(entries)

    created_entries = Entry.objects.all()

    likes = [Like(user=admin, entry=entry) for entry in created_entries]
    Like.objects.bulk_create(likes)

    Like.objects.create(user=just_user, entry=created_entries[0])

    ForbiddenWord.objects.bulk_create([ForbiddenWord(word=word) for word in ['f-word', 'n-word']])


def backwards(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Entry = apps.get_model('guestbook', 'Entry')
    Like = apps.get_model('guestbook', 'Like')
    ForbiddenWord = apps.get_model('guestbook', 'ForbiddenWord')

    Like.objects.all().delete()
    Entry.objects.all().delete()
    User.objects.all().delete()
    ForbiddenWord.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('guestbook', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
