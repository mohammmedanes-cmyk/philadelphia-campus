import unittest
from app import app
from database import get_db
from seed_data import seed_database

class TestDirectorAndTeacherFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key-2026'
        seed_database()

    def setUp(self):
        self.client = app.test_client()

    def test_01_student_card_has_student_number_and_personal_records(self):
        """Verify student ID card displays student number, class, year, street, parents, chip & barcode."""
        with app.app_context():
            db = get_db()
            student = db.execute("SELECT id, student_id_code, full_name FROM users WHERE email = 'sarah.m@student.philadelphia.edu'").fetchone()
            self.assertIsNotNone(student)
            
            res = self.client.get(f'/student-card/{student["id"]}')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            
            # Check student ID number & personal records
            self.assertIn(student['student_id_code'], html)
            self.assertIn("STUDENT ID NO.", html)
            self.assertIn("Academic Year", html)
            self.assertIn("Class / Group", html)
            self.assertIn("Residential Street", html)
            self.assertIn("Parents", html)
            
            # Check executive features
            self.assertIn("fa-microchip", html)
            self.assertIn("fa-wifi", html)
            self.assertIn("USA ACTIVE", html)
            self.assertIn("Academic Transcript Barcode", html)

    def test_02_director_private_access_and_student_update(self):
        """Verify Director can login, access dashboard, and update student personal information."""
        # 1. Unauthenticated access blocked
        res = self.client.get('/director', follow_redirects=False)
        self.assertEqual(res.status_code, 302)

        # 2. Login as Director
        login_res = self.client.post('/director/login', data={
            'email': 'director@philadelphia.edu',
            'password': 'director2026'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        self.assertIn("Director Portal", login_res.get_data(as_text=True))

        # 3. Director updates a student's personal info
        with app.app_context():
            db = get_db()
            sarah = db.execute("SELECT id FROM users WHERE email = 'sarah.m@student.philadelphia.edu'").fetchone()
            student_id = sarah['id']

        update_res = self.client.post('/director/update-student', data={
            'student_id': student_id,
            'student_id_code': 'PC-2026-99999',
            'academic_year': '3rd Year (السنة الثالثة) - Junior',
            'class_name': 'CS-Executive-A',
            'living_street': '123 Boulevard of the Arts, Philadelphia',
            'parents_name': 'Mourad & Fatima Mansouri',
            'parents_phone': '+213 550 99 88 77'
        }, follow_redirects=True)
        self.assertEqual(update_res.status_code, 200)

        # Verify update persisted in DB
        with app.app_context():
            db = get_db()
            updated = db.execute("SELECT student_id_code, class_name, living_street, parents_phone FROM users WHERE id = ?", (student_id,)).fetchone()
            self.assertEqual(updated['student_id_code'], 'PC-2026-99999')
            self.assertEqual(updated['class_name'], 'CS-Executive-A')
            self.assertEqual(updated['living_street'], '123 Boulevard of the Arts, Philadelphia')
            self.assertEqual(updated['parents_phone'], '+213 550 99 88 77')

    def test_03_teacher_private_access_and_specialty_isolation(self):
        """Verify Teacher portal enforces specialty isolation and allows inputting marks."""
        # 1. Unauthenticated access blocked
        res = self.client.get('/teacher', follow_redirects=False)
        self.assertEqual(res.status_code, 302)

        # 2. Login as CS Teacher
        login_res = self.client.post('/teacher/login', data={
            'email': 'teacher.cs@philadelphia.edu',
            'password': 'teacher2026'
        }, follow_redirects=True)
        self.assertEqual(login_res.status_code, 200)
        html = login_res.get_data(as_text=True)
        self.assertIn("Faculty Teacher Portal", html)
        self.assertIn("Computer Science", html)
        
        # CS students visible
        self.assertIn("Sarah Mansouri", html)
        
        # Non-CS students (Medicine, Law, Business) must NOT be in the teacher's grading list
        self.assertNotIn("Lucas Dubois", html)
        self.assertNotIn("Elena Weber", html)

        # 3. Teacher adds a grade for Sarah
        with app.app_context():
            db = get_db()
            sarah = db.execute("SELECT id FROM users WHERE email = 'sarah.m@student.philadelphia.edu'").fetchone()
            sarah_id = sarah['id']

        grade_res = self.client.post('/teacher/add-grade', data={
            'student_id': sarah_id,
            'subject': 'CSC 470: Artificial Intelligence & Deep Learning',
            'score': '19.5',
            'semester': 'Semester 2 - Final Exam',
            'notes': 'Outstanding neural network design'
        }, follow_redirects=True)
        self.assertEqual(grade_res.status_code, 200)
        self.assertIn("recorded successfully", grade_res.get_data(as_text=True))

        # 4. Check grade in student transcript
        trans_res = self.client.get(f'/transcript/{sarah_id}')
        self.assertEqual(trans_res.status_code, 200)
        trans_html = trans_res.get_data(as_text=True)
        self.assertIn("Artificial Intelligence", trans_html)
        self.assertIn("19.5", trans_html)

    def test_04_teacher_cannot_grade_students_outside_specialty(self):
        """Security verification: Teacher cannot grade a student from another specialty."""
        # Login as CS Teacher
        self.client.post('/teacher/login', data={
            'email': 'teacher.cs@philadelphia.edu',
            'password': 'teacher2026'
        }, follow_redirects=True)

        with app.app_context():
            db = get_db()
            lucas = db.execute("SELECT id FROM users WHERE email = 'lucas.d@student.philadelphia.edu'").fetchone() # Medicine student
            lucas_id = lucas['id']

        # Attempt to submit grade for Medicine student from CS teacher
        tamper_res = self.client.post('/teacher/add-grade', data={
            'student_id': lucas_id,
            'subject': 'Malicious Grading Attempt',
            'score': '20.0',
            'semester': 'Semester 1',
            'notes': 'Should be rejected'
        }, follow_redirects=True)
        
        tamper_html = tamper_res.get_data(as_text=True)
        self.assertIn("Security Alert", tamper_html)

if __name__ == '__main__':
    unittest.main()
