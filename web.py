#!/usr/bin/env python

import codecs
from flask import Flask
from flask import render_template
from flask.ext.misaka import Misaka
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Server, Manager
from flask.ext.migrate import Migrate, MigrateCommand

md = Misaka()
app = Flask(__name__)
md.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uwcalgo.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(debug=True))


class Solution(db.Model):
    __tablename__ = 'solutions'
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), primary_key=True)
    problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'), primary_key=True)
    url = db.Column(db.String(200), nullable=True)
    problem = db.relationship('Problem')


class Member(db.Model):
    __tablename__ = 'member'
    id = db.Column(db.Integer, primary_key=True)
    github_name = db.Column(db.String(64), nullable=True, unique=True)
    first_name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=True)
    solutions = db.relationship('Solution')


class Difficulty(db.Model):
    __tablename__ = 'difficulty'
    id = db.Column(db.Integer, primary_key=True)
    level_name = db.Column(db.String(30), nullable=False)
    points = db.Column(db.Integer, nullable=False)


class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    difficulty_id = db.Column(db.Integer, db.ForeignKey('difficulty.id'))
    difficulty = db.relationship('Difficulty', backref='problems')


@app.route('/')
def index():
    with codecs.open('index.md', encoding='utf-8') as input_file:
        content = input_file.read()

    return render_template('index.html', **locals())


@app.route('/leaderboard/')
def leaderboard():
    members = db.session.query(Member).filter(Member.solutions != None).all()
    scores = []
    for member in members:
        score = sum([solution.problem.difficulty.points for solution in member.solutions])
        scores.append([member.first_name, member.github_name, score])
    return render_template('leaderboard.html', **locals())

if __name__ == '__main__':
    manager.run()
