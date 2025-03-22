from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login_manager
from sqlalchemy import Integer

class User(UserMixin, db.Model):#user table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    full_name = db.Column(db.String(128))
    qualification = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date)

    scores = db.relationship('Score', backref='user', lazy='dynamic')
    
    given_feedbacks = db.relationship('Feedback', foreign_keys='[Feedback.user_id]', backref='admin', lazy='dynamic')#admin ne feedback diya 
    received_feedbacks = db.relationship('Feedback', foreign_keys='[Feedback.student_id]', backref='student', lazy='dynamic')#student ne feedback receive kiya

    announcements = db.relationship('Announcement', backref='admin_user', lazy='dynamic', foreign_keys='[Announcement.admin_id]')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader  #user session manage karne ke liye
def load_user(id):
    return User.query.get(int(id))

class Subject(db.Model):#subject table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref='subject', lazy='dynamic')

class Chapter(db.Model):#chapter table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy='dynamic')

class Quiz(db.Model):#quiz table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False, default="Quiz 0")  
    date_of_quiz = db.Column(db.Date, nullable=False)
    time_duration = db.Column(Integer, nullable=False) 
    remarks = db.Column(db.Text)
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade="all, delete-orphan")
    scores = db.relationship('Score', backref='quiz', lazy='dynamic', cascade="all, delete-orphan")

class Question(db.Model):#question table
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(200), nullable=False)
    option2 = db.Column(db.String(200), nullable=False)
    option3 = db.Column(db.String(200), nullable=False)
    option4 = db.Column(db.String(200), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

class Score(db.Model):#score table
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer, nullable=False)
    feedbacks = db.relationship('Feedback', backref='score', lazy='dynamic')
    user_answer = db.relationship('Answer', backref='student_score', lazy='dynamic', cascade="all, delete-orphan"
    ) 

class Feedback(db.Model):#feedback table
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):#announcement table
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, name="admin_id")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    title = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  
    admin = db.relationship('User', foreign_keys=[admin_id])
    user = db.relationship('User', foreign_keys=[user_id])

class Answer(db.Model):#answer table
    id = db.Column(db.Integer, primary_key=True)
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.Integer, nullable=False)


