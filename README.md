# MAD-1

## Description of the Project
Quiz_master is a multi-user application designed to help students prepare for examinations through interactive quizzes. Users can practice subject-specific quizzes and receive personalized feedback from instructors (admins) based on their quiz performance.

## Features

### Users:
1. **Subject Selection:** Users can log in and choose any subject from the available list.
2. **Quiz Participation:** Users can browse chapters under a subject, select quizzes, and practice related questions.
3. **Announcements:** Users can view announcements from the quiz master for important updates or clarifications.
4. **Score Tracking & Feedback:** Users can review past quiz scores and check for feedback issued by the admin.
5. **Quiz Retake:** Users have the option to retake quizzes to improve their scores.

### Admin:
1. **Subject Management:** Admins can add, delete, or edit subjects in the database.
2. **Chapter & Quiz Management:** Admins can manage chapters within subjects and add, delete, or edit chapters, quizzes or related questions.
3. **Announcements:** Admins can send announcements to all students.
4. **Student Progress Tracking:** Admins can browse student lists, track individual progress, and view student details.
5. **Feedback System:** Admins can provide personalized feedback on students' quiz attempts.

## Installation & Setup
1. Clone the repository:
   ```sh
   git clone https://yourusername/MAD-1.git
   cd quiz_master_24f2003068
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the database:
   ```sh
   python init_db.py
   ```
4. Create an Admin User
   ```sh
   python create_admin.py
   ```
5. Run the application:
   ```sh
   python run.py
   ```
6. Open the browser and access the app at:
   ```
   http://localhost:5000
   ```

## Technologies Used
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, CSS, Bootstrap
- **Authentication:** Flask-Login

## Future Enhancements
- Implementing a leaderboard for quiz rankings.
- Adding a discussion forum for student interactions.
- Introducing timed quizzes for better exam simulation.

## Contributing
Contributions are welcome! If you'd like to improve the project, feel free to fork the repository and submit a pull request.

---
# Contact

**For questions or suggestions, please contact:**

Name: Anirudh Phophalia

Email: aphophalia_be24@thapar.edu

