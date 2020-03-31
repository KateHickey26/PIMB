import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','IT_Group_Project.settings')
import django
django.setup()
from inspeakers.models import *
from django.contrib.auth.models import User

def populate():
    tags = [{'name':'Corporate Events'},{'name':'Wellness Retreats'},{'name':'Job Fairs'},{'name':'Hotel Conference Room Fillers'},{'name':'Lonely Hearts Conventions'}]
    speakers = [{'name':'Adam Scott','desc': 'Are you looking for someone to bring some flair to your next corporate event? Look no further!','rate': 3, 'Tags':['Corporate Events'], 'email':'lucy@munroesmotivators.com','phone':'0563 456 66','company':'Munroes Motivators','hourlyrate':'£500','twitter':'https://twitter.com/home'},
    {'name':'Ben Halpert','desc': 'I specialise in convincing unemployed people to stop looking for a job, and start giving me money (taken bi-monthly) to help them acheive their dreams!!','rate': 4,'Tags':['','Job Fairs'], 'email':'hnelson@nelsontalent.com','phone':'0173 466 56','company':'Nelson Talent','hourlyrate':'£250','twitter':'https://twitter.com/home'},
    {'name':'Emma-Jane Andrews','desc': 'One day I dreamt about all the people in the world who have been unlucky in love. I realised that there are millions of lonely people in the world who have never found that special someone. Then an apiphany hit me: I could charge all those people to learn how to be ready to accept love in to their hearts, which could equate to millions of dollars in ticket sales! Its simple dollars and cents!'
    ,'rate': 5, 'Tags':['Wellness Retreats','Hotel Conference Room Fillers','Lonely Hearts Conventions'], 'email':'grahem@ghmanagement.com','phone':'0123 456 56','company':'GH Management','hourlyrate':'£300','twitter':'https://twitter.com/home'},
    {'name':'Donald Sax','desc': 'Self Care is very important to me. This is why my life goals is to charge other a fair, nominal fee for a weekend retreat where you can learn to meditate, to channel good vibes, and to sit cross-legged on the ground.','rate': 1,'Tags':['Wellness Retreats'], 'email':'alice@allstarspeakers.com','phone':'0123 567 56','company':'All Star Speakers','hourlyrate':'£90','twitter':'https://twitter.com/home'}]
    for s in speakers:
        add_speakers(s['name'], s['desc'],s['Tags'],s['email'],s['phone'],s['company'],s['hourlyrate'],s['twitter'])


def add_tag(name, popularity=0):
    t = Tag.objects.get_or_create(name = name)[0]
    t.popularity = popularity
    t.save()
    return t

def add_speakers(name, desc, tags , email, phone, company, hourlyrate, twitter):
    try:
        u = User.objects.create_user(username = name, email = name+'@'+name+'.com')
    except:
        u = User.objects.get(username = name)
    u.set_password('123456')
    u.save()
    a = UserProfile.objects.get_or_create(user=u)
    s = SpeakerProfile.objects.get_or_create(speaker=u)[0]
    for t in tags:
        to =  Tag.objects.get_or_create(name = t)[0]
        s.tags.add(to)
    s.name = name
    s.description = desc
    s.email = email
    s.phone = phone
    s.company = company
    s.hourlyrate = hourlyrate
    s.twitter = twitter
    s.save()
    return s

# Start execution here!

if __name__ == '__main__':
	print('Starting Inspeakers population script...')
	populate()
