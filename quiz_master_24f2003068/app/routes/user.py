from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import User, Subject, Chapter, Quiz, Question, Score, Feedback, Announcement,Answer
from app import db
from datetime import datetime, timedelta

anirudh_bp = Blueprint('user', __name__)#user blueprint

@anirudh_bp.route('/dashboard')
@login_required
def dashboard():#my user dashboard
    subjects = Subject.query.all()
    scores = Score.query.filter_by(user_id=current_user.id).all()
    quiz_labels = [score.quiz.title for score in scores]
    quiz_scores = [score.total_scored for score in scores]
    return render_template('user/dashboard.html', subjects=subjects, quiz_labels=quiz_labels, quiz_scores=quiz_scores)

@anirudh_bp.route('/subject/<int:subject_id>')
@login_required#my subject page
def view_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    chapters = Chapter.query.filter_by(subject_id=subject.id).all()
    return render_template('user/view_subject.html', subject=subject, chapters=chapters)

@anirudh_bp.route('/chapter/<int:chapter_id>')
@login_required
def view_chapter(chapter_id):#my chapter page
    chapter = Chapter.query.get_or_404(chapter_id)
    quizzes = Quiz.query.filter_by(chapter_id=chapter.id).all()
    return render_template('user/view_chapter.html', chapter=chapter, quizzes=quizzes)

@anirudh_bp.route('/take_quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def take_quiz(quiz_id):#my take quiz page
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    if request.method == 'POST':
        total_score = 0
        ist_time = datetime.utcnow() + timedelta(hours=5, minutes=30)#indian standard time
        new_score = Score(
            quiz_id=quiz.id,
            user_id=current_user.id,
            time_stamp_of_attempt=ist_time,
            total_scored=0 
        )
        db.session.add(new_score)
        db.session.commit() 
        for question in questions:
            user_answer = request.form.get(f'question_{question.id}')
            if user_answer is not None:
                try:
                    user_answer = int(user_answer)
                    is_correct = user_answer == question.correct_option
                    if is_correct:
                        total_score += 1
                    answer = Answer(
                        score_id=new_score.id,
                        question_id=question.id,
                        selected_option=user_answer
                    )
                    db.session.add(answer)
                except ValueError:
                    flash(f"Invalid answer for question {question.id}.", "fail")
        new_score.total_scored = total_score
        db.session.commit()
        flash(f'hurray!, quiz completed. Your score: {total_score}/{len(questions)}', 'success')
        return redirect(url_for('user.view_results', quiz_id=quiz.id))
    return render_template('user/take_quiz.html', quiz=quiz, questions=questions)

@anirudh_bp.route('/view_results/<int:quiz_id>')
@login_required
def view_results(quiz_id):#my results page
    quiz = Quiz.query.get_or_404(quiz_id)
    score = Score.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).first()
    feedback = Feedback.query.filter_by(quiz_id=quiz.id, user_id=current_user.id).order_by(Feedback.timestamp.desc()).first()
    if not score:
        flash("No score available. Please take the quiz first.")
        return redirect(url_for('user.take_quiz', quiz_id=quiz.id))
    return render_template('user/view_results.html', quiz=quiz, score=score, feedback=feedback)

@anirudh_bp.route('/my_scores')
@login_required
def my_scores():#my scores page
    scores = Score.query.filter_by(user_id=current_user.id).order_by(Score.time_stamp_of_attempt.desc()).all()
    return render_template('user/my_scores.html', scores=scores)

@anirudh_bp.route('/api/student_scores', methods=['GET'])
@login_required
def get_student_scores():#my student scores page
    if current_user.is_admin:
        scores = db.session.query(User.full_name, Quiz.title, Score.total_scored, Quiz.id) \
            .join(Score, User.id == Score.user_id) \
            .join(Quiz, Score.quiz_id == Quiz.id).all()#joins the tables
        data = {}
        for name, quiz_name, score, quiz_id in scores:
            question_count = Question.query.filter_by(quiz_id=quiz_id).count()
            percentage_score = (score / question_count) * 100 if question_count > 0 else 0 #percentage score calculation
            data.setdefault(name, []).append({"quiz": quiz_name, "score": percentage_score})
    else:
        scores = Score.query.filter_by(user_id=current_user.id).all()
        data = {
            "student": current_user.full_name,
            "scores": [{"quiz": score.quiz.name, "score": (score.total_scored / score.quiz.questions.count()) * 100} for score in scores]
        }
    return jsonify(data)

@anirudh_bp.route('/announcements')
@login_required
def view_announcements():#my announcements page
    announcements = Announcement.query.order_by(Announcement.timestamp.desc()).all()
    return render_template('user/announcements.html', announcements=announcements)

@anirudh_bp.route('/my_feedback')
@login_required
def my_feedback():#my feedback page
    feedbacks = Feedback.query.filter_by(student_id=current_user.id).order_by(Feedback.timestamp.desc()).all()
    return render_template('user/feedback.html', feedbacks=feedbacks)


