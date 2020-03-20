import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','IT_Group_Project.settings')
import django
django.setup()
from inspeakers.models import *
from django.contrib.auth.models import User

def populate():
    tags = [{'name':'E'},{'name':'F'},{'name':'G'},{'name':'H'}]
    speakers = [{'name':'Adam','desc': 'No desc now','rate': 0},{'name':'Ben','desc': 'No desc now','rate': 3},{'name':'Chris','desc': 'No desc now','rate': 1},{'name':'Donald','desc': 'No desc now','rate': 4}]
    for s in speakers:
        add_speakers(s['name'], s['desc'],s['rate'])

    for t in tags:
        add_tag(t['name'])

def add_tag(name, popularity=0):
    t = Tag.objects.get_or_create(name = name)[0]
    t.popularity = popularity
    t.save()
    return t

def add_speakers(name, desc, rate = 0):
    try:
        u = User.objects.create_user(name,name+'@'+name+'.com','123456')
    except:
        u = User.objects.get(email=name+'@'+name+'.com')
    u.save()
    s = SpeakerProfile.objects.get_or_create(speaker=u)[0]
    s.name = name
    s.description = desc
    s.rate = rate
    s.save()
    return s

# Start execution here!
if __name__ == '__main__':
	print('Starting Inspeakers population script...')
	populate()