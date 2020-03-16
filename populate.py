import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','IT_Group_Project.settings')
import django
django.setup()
from inspeakers.models import Tag

def populate():
    tags = [{'name':'E'},{'name':'F'},{'name':'G'},{'name':'H'}]

    for t in tags:
        add_tag(t['name'])

def add_tag(name, popularity=0):
    t = Tag.objects.get_or_create(name = name)[0]
    t.popularity = popularity
    t.save()
    return t

# Start execution here!
if __name__ == '__main__':
	print('Starting Inspeakers population script...')
	populate()