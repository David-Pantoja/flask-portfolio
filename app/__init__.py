from datetime import datetime
from flask import Flask, render_template, request
from playhouse.shortcuts import model_to_dict
import json
import os
from jinja2 import Environment, FileSystemLoader
from peewee import *

app = Flask(__name__)
#mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
mydb = MySQLDatabase("myportfoliodb",
    user="myportfolio",
    password="mypassword",
    host="localhost",
    port=3306
)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

print(mydb)

mydb.connect()
mydb.create_tables([TimelinePost])

a = open('app/data/work.json')
work_data = json.load(a)
a.close()
work_d = work_data.copy()

b = open('app/data/hobbies.json')
hobby_data = json.load(b)
b.close()
hobbies_d = hobby_data.copy()

c = open('app/data/education.json')
education_data = json.load(c)
c.close()
education_d = education_data.copy()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/aboutme')
def aboutme():
    return render_template('aboutme.html')

@app.route('/work')
def work():
    return render_template('work.html', work = work_d)

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', hobbies = hobbies_d)

@app.route('/education')
def education():
    return render_template('education.html', education = education_d)

@app.route('/travel')
def travel():
    return render_template('travel.html')

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    Timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(Timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }


@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline", timelineuploads=get_time_line_post()["timeline_posts"])