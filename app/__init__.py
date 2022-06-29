from datetime import datetime
from flask import Flask, redirect, render_template, request, Response
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv
import json
import os
from jinja2 import Environment, FileSystemLoader
from peewee import *
from pymysql import NULL

load_dotenv()
app = Flask(__name__)

if os.getenv("TESTING") == "True":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST"),
        port=3306
    )

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = mydb

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

    try:
        name = request.form['name']
        if name == "" or name == NULL:
            return Response(render_template('error.html', error="name"), 400)
    except:
        return Response(render_template('error.html', error="name"), 400)


    try:
        email = request.form['email']
        if email == "" or email == NULL or not ('@' in email and '.' in email):
            return Response(render_template('error.html', error="email"), 400)
    except:
        return Response(render_template('error.html', error="email"), 400)


    try:
        content = request.form['content']
        if content == "" or content == NULL:
            return Response(render_template('error.html', error="content"), 400)
    except:
        return Response(render_template('error.html', error="content"), 400)

    Timeline_post = TimelinePost.create(name=name, email=email, content=content)
    model_to_dict(Timeline_post)
    return redirect("/timeline", code=302)

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