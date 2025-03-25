from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User, Subject, Chapter, Quiz, Question, Score, Announcement, Feedback, Answer
from app import db
from datetime import datetime, timedelta

anirudh_bp = Blueprint('admin', __name__, url_prefix='/admin')

@anirudh_bp.route('/dashboard')
@login_required
def dashboard(): #my admin dashboard 
    if not current_user.is_admin:
        flash('This page cannot be accesible by you')
        return redirect(url_for('user.dashboard'))
    
    subjects = Subject.query.all()
    users = User.query.filter_by(is_admin=False).all()  # Get all non-admin users
    return render_template('admin/dashboard.html', subjects=subjects, users=users)


###Subjects-----
@anirudh_bp.route('/create_subject', methods=['GET', 'POST'])
@login_required
def create_subject():# my create subject page
    if not current_user.is_admin:
        flash('This page cannot be accesible by you.')
        return redirect(url_for('user.dashboard'))
    
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        flash('Great! You created a new Subject for teh students quiz.')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/create_subject.html')

@anirudh_bp.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def edit_subject(subject_id): # my edit subject page
    if not current_user.is_admin:
        flash('this page cannot be accesible by you!')
        return redirect(url_for('user.dashboard'))
    
    subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        subject.name = request.form['name']
        subject.description = request.form['description']
        db.session.commit()
        flash('YOu edited the subject')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_subject.html', subject=subject)

@anirudh_bp.route('/delete_subject/<int:subject_id>', methods=['POST'])
@login_required # MY delete subject page
def delete_subject(subject_id):
    if not current_user.is_admin:
        flash('This page is not accesible by you')
        return redirect(url_for('user.dashboard'))
    
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted')
    return redirect(url_for('admin.dashboard'))



###Chapters-----
@anirudh_bp.route('/create_chapter/<int:subject_id>', methods=['GET', 'POST'])
@login_required
def create_chapter(subject_id):# my create chapter page
    if not current_user.is_admin:
        flash('This page is not accesible by you')
        return redirect(url_for('user.dashboard'))
    
    subject = Subject.query.get_or_404(subject_id)
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('I think you forgot to enter the name of the chapter.')
            return render_template('admin/create_chapter.html', subject=subject)
        
        chapter = Chapter(
            name=name,
            description=description,
            subject_id=subject.id
        )
        try:
            db.session.add(chapter)
            db.session.commit()
            flash('chapter created')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('some error might occured try again')
            return render_template('admin/create_chapter.html', subject=subject)
    
    return render_template('admin/create_chapter.html', subject=subject)

@anirudh_bp.route('/delete_chapter/<int:chapter_id>', methods=['POST'])
@login_required # MY delete chapter page
def delete_chapter(chapter_id):
    if not current_user.is_admin:
        flash('This page is not accesible by you')
        return redirect(url_for('user.dashboard'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted')
    return redirect(url_for('admin.dashboard'))

@anirudh_bp.route('/edit_chapter/<int:chapter_id>', methods=['GET', 'POST'])
@login_required # my edit chapter page
def edit_chapter(chapter_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        chapter.name = request.form['name']
        chapter.description = request.form['description']
        db.session.commit()
        flash('Chapter edited')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_chapter.html', chapter=chapter,back_url=request.referrer)

@anirudh_bp.route('/view_chapter/<int:chapter_id>')
@login_required # my view chapter page
def view_chapter(chapter_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = chapter.quizzes.all()
    return render_template('admin/view_chapter.html', chapter=chapter, quizzes=quizzes)



###Quizzes-----
@anirudh_bp.route('/create_quiz/<int:chapter_id>', methods=['GET', 'POST'])
@login_required # my create quiz page
def create_quiz(chapter_id):#my create quiz page
    if not current_user.is_admin:
        flash('This page is not accesible by you')
        return redirect(url_for('user.dashboard'))
    
    chapter = Chapter.query.get_or_404(chapter_id)
    if request.method == 'POST':
        name = request.form['name']
        date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        time_duration = timedelta(minutes=int(request.form['time_duration']))
        remarks = request.form['remarks']
        quiz = Quiz(
            name=name, 
            chapter_id=chapter.id,
            date_of_quiz=date_of_quiz,
            time_duration=time_duration.total_seconds() // 60, #minutes mein conversion
            remarks=remarks
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created')
        return redirect(url_for('admin.create_question', quiz_id=quiz.id))
    
    return render_template('admin/create_quiz.html', chapter=chapter)

@anirudh_bp.route('/delete_quiz/<int:quiz_id>', methods=['POST'])
@login_required # my delete quiz page
def delete_quiz(quiz_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    Feedback.query.filter_by(quiz_id=quiz_id).delete()
    Score.query.filter_by(quiz_id=quiz_id).delete()
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted')
    return redirect(url_for('admin.dashboard'))

@anirudh_bp.route('/view_quiz/<int:quiz_id>')
@login_required # my view quiz page
def view_quiz(quiz_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions.all()
    chapter_id = quiz.chapter_id  # Assuming Quiz has a foreign key `chapter_id`
    return render_template('admin/view_quiz.html', quiz=quiz, questions=questions, chapter_id=chapter_id)

@anirudh_bp.route('/edit_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required # my edit quiz page
def edit_quiz(quiz_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        quiz.name = request.form['name']
        quiz.date_of_quiz = datetime.strptime(request.form['date_of_quiz'], '%Y-%m-%d')
        quiz.time_duration = timedelta(minutes=int(request.form['time_duration'])).total_seconds() // 60
        quiz.remarks = request.form['remarks']
        db.session.commit()
        flash('Quiz edited')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_quiz.html', quiz=quiz,back_url=request.referrer)



###Questions-----
@anirudh_bp.route('/create_question/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def create_question(quiz_id): # my create questions page
    if not current_user.is_admin:
        flash('This page is not accesible by you.')
        return redirect(url_for('user.dashboard'))
    
    quiz = Quiz.query.get_or_404(quiz_id)
    if request.method == 'POST':
        question = Question(
            quiz_id=quiz.id,
            question_statement=request.form['question_statement'],
            option1=request.form['option1'],
            option2=request.form['option2'],
            option3=request.form['option3'],
            option4=request.form['option4'],
            correct_option=int(request.form['correct_option'])
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added')
        if 'add_another' in request.form:
            return redirect(url_for('admin.create_question', quiz_id=quiz.id))
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/create_question.html', quiz=quiz)

@anirudh_bp.route('/delete_question/<int:question_id>', methods=['POST'])
@login_required # my delete question page
def delete_question(question_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted')
    return redirect(url_for('admin.dashboard'))

@anirudh_bp.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
@login_required # my edit question page
def edit_question(question_id):
    if not current_user.is_admin:
        flash('This page is not accessible by you.')
        return redirect(url_for('user.dashboard'))
    
    question = Question.query.get_or_404(question_id)
    if request.method == 'POST':
        question.question_statement = request.form['question_statement']
        question.option1 = request.form['option1']
        question.option2 = request.form['option2']
        question.option3 = request.form['option3']
        question.option4 = request.form['option4']
        question.correct_option = int(request.form['correct_option'])
        db.session.commit()
        flash('Question edited')
        return redirect(url_for('admin.dashboard'))
    
    return render_template('admin/edit_question.html', question=question, back_url=request.referrer)



@anirudh_bp.route('/view_student_answers/<int:score_id>')
@login_required
def view_student_answers(score_id):# my view student answers page
    if not current_user.is_admin:
        flash('This page is not be accesible by you.')
        return redirect(url_for('user.dashboard'))
    
    score = Score.query.get_or_404(score_id)
    quiz = score.quiz
    questions = Question.query.filter_by(quiz_id=quiz.id).all()

    user_answers = Answer.query.filter_by(score_id=score_id).all()
    
    # questionid and selected option ko match karne ke liye dictionary
    user_answer_dict = {answer.question_id: answer.selected_option for answer in user_answers}

    return render_template('admin/view_student_answers.html', score=score, questions=questions, user_answers=user_answer_dict)

@anirudh_bp.route('/send_announcement', methods=['GET', 'POST'])
@login_required
def send_announcement():# my send announcement page
    if not current_user.is_admin:
        flash('This page is not accesible by you.')
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        announcement = Announcement(title=title, message=message, date_posted=datetime.utcnow())
        try:
            db.session.add(announcement)
            db.session.commit()
            flash('You sent announcement to the users.')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('some error occured try again')
    
    return render_template('admin/send_announcement.html')

@anirudh_bp.route('/send_feedback/<int:score_id>', methods=['GET', 'POST'])
@login_required
def send_feedback(score_id):# my send feedback page
    if not current_user.is_admin:
        flash('This page is not accesible by you')
        return redirect(url_for('user.dashboard'))

    score = Score.query.get_or_404(score_id)
    student = User.query.get(score.user_id)

    if not student:
        flash('Student not found!')
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        feedback_text = request.form['feedback']

        feedback = Feedback(
            user_id=current_user.id,  # yeh admin id hai
            quiz_id=score.quiz_id,  
            student_id=student.id, #yeh student id hai
            score_id=score.id,  
            feedback=feedback_text,  
            timestamp=datetime.utcnow()
        )

        db.session.add(feedback)
        db.session.commit()
        flash('Feedback sent')
        return redirect(url_for('admin.view_student_answers', score_id=score.id))

    return render_template('admin/send_feedback.html', score=score)

@anirudh_bp.route('/student/<int:student_id>')
@login_required
def student_details(student_id):#student details page
    if not current_user.is_admin:
        flash('This page cannot be accesible by you')
        return redirect(url_for('user.dashboard'))
    
    student = User.query.get_or_404(student_id)
    return render_template('admin/student_details.html', student=student)
