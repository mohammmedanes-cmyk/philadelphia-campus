# -*- coding: utf-8 -*-
"""
Automated Comprehensive Test Suite for Student ID Card & Transcript Features
"""
import io
import unittest
from PIL import Image

import app
import database

class StudentFeaturesTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.app.test_client()
        with app.app.app_context():
            database.migrate_db()

    def test_student_card_public_endpoint(self):
        """Test student card page for demo user (id=1)"""
        res = self.client.get('/student-card/1')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('Student ID Card', html)
        self.assertIn('PHILADELPHIA', html)
        self.assertIn('PC-', html)
        # Check barcode SVG is present
        self.assertIn('<svg', html)
        self.assertIn('Academic Transcript Barcode', html)
        # Check transcript link is present
        self.assertIn('/transcript/1', html)

    def test_transcript_endpoint(self):
        """Test academic transcript page for demo user (id=1)"""
        res = self.client.get('/transcript/1')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('Academic Grades Transcript', html)
        self.assertIn('Course Title', html)
        self.assertIn('Credit Hours', html)
        self.assertIn('Cumulative GPA', html)
        self.assertIn('Sarah Mansouri', html)

    def test_registration_form_fields(self):
        """Test registration page contains the new fields"""
        res = self.client.get('/register')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('name="first_name"', html)
        self.assertIn('name="last_name"', html)
        self.assertIn('name="date_of_birth"', html)
        self.assertIn('name="photo"', html)
        self.assertIn('enctype="multipart/form-data"', html)

    def test_registration_with_photo_and_dob_redirects_to_card(self):
        """Test registering a new student with photo and date of birth"""
        img_io = io.BytesIO()
        test_img = Image.new('RGB', (150, 180), color=(50, 100, 200))
        test_img.save(img_io, 'JPEG')
        img_io.seek(0)

        unique_email = "test.student.signup@gmail.com"
        with app.app.app_context():
            with database.get_db() as conn:
                conn.execute("DELETE FROM users WHERE email = ?", (unique_email,))
                conn.commit()

        post_data = {
            'first_name': 'Samir',
            'last_name': 'Khadri',
            'email': unique_email,
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'specialty': 'Computer Science & IT',
            'country': 'Algeria',
            'date_of_birth': '2002-05-14',
            'photo': (img_io, 'student_photo.jpg', 'image/jpeg')
        }

        res = self.client.post('/register', data=post_data, content_type='multipart/form-data', follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        self.assertIn('/student-card', res.location)

        with app.app.app_context():
            with database.get_db() as conn:
                user = conn.execute("SELECT * FROM users WHERE email = ?", (unique_email,))
                user = user.fetchone()
                self.assertIsNotNone(user)
                self.assertEqual(user['first_name'], 'Samir')
                self.assertEqual(user['last_name'], 'Khadri')
                self.assertEqual(user['full_name'], 'Samir Khadri')
                self.assertEqual(user['date_of_birth'], '2002-05-14')
                self.assertTrue(user['photo_url'].startswith('data:image/jpeg;base64,'))
                self.assertTrue(user['student_id_code'].startswith('PC-2026-'))
                new_user_id = user['id']

        # Now follow redirect as logged in user
        res_card = self.client.get(res.location)
        self.assertEqual(res_card.status_code, 200)
        card_html = res_card.data.decode('utf-8')
        self.assertIn('Samir', card_html)
        self.assertIn('Khadri', card_html)
        self.assertIn('Computer Science &amp; IT', card_html)
        self.assertIn('2002-05-14', card_html)
        self.assertIn('data:image/jpeg;base64,', card_html)

        # Check transcript for this new user
        res_trans = self.client.get(f'/transcript/{new_user_id}')
        self.assertEqual(res_trans.status_code, 200)
        trans_html = res_trans.data.decode('utf-8')
        self.assertIn('Samir Khadri', trans_html)
        self.assertIn('Computer Science &amp; IT', trans_html)

    def test_profile_has_card_and_transcript_links(self):
        """Test profile page contains links to student card and transcript when logged in"""
        # Login demo user
        res_login = self.client.post('/login', data={
            'email': 'sarah.m@student.philadelphia.edu',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(res_login.status_code, 200)

        res = self.client.get('/profile/1')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('/student-card/1', html)
        self.assertIn('/transcript/1', html)

if __name__ == '__main__':
    unittest.main()
