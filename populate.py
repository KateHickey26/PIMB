import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','IT_Group_Project.settings')
import django
django.setup()
from inspeakers.models import *
from django.contrib.auth.models import User

def populate():
    tags = [{'name':'E'},{'name':'F'},{'name':'G'},{'name':'H'}]
    speakers = [{'name':'Adam','desc': 'No desc now','rate': 0, 'Tags':['A','C']},{'name':'Ben','desc': 'No desc now','rate': 3,'Tags':['','C']},{'name':'Chris','desc': 'No desc now','rate': 1, 'Tags':['A','B','C']},{'name':'Donald','desc': 'No desc now','rate': 4,'Tags':['D']}]
    for s in speakers:
        add_speakers(s['name'], s['desc'],s['Tags'],s['rate'])

    for t in tags:
        add_tag(t['name'])

def add_tag(name, popularity=0):
    t = Tag.objects.get_or_create(name = name)[0]
    t.popularity = popularity
    t.save()
    return t

def add_speakers(name, desc, tags , rate = 0):
    try:
        u = User.objects.create_user(name,name+'@'+name+'.com','123456')
    except:
        u = User.objects.get(username = name)
    u.save()
    s = SpeakerProfile.objects.get_or_create(speaker=u)[0]
    for t in tags:
        to =  Tag.objects.get_or_create(name = t)[0]
        s.tags.add(to)
    s.name = name
    s.description = desc
    s.rate = rate
    s.save()
    return s

# Start execution here!
if __name__ == '__main__':
	print('Starting Inspeakers population script...')
	populate()