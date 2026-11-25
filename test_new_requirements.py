# -*- coding: utf-8 -*-
import unittest
import io
from PIL import Image
import app
import database

class NewRequirementsTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.app.test_client()

    def test_reject_applicant_younger_than_2012(self):
        """Applicants born after 2012 (e.g. 2013) must be rejected"""
        img_io = io.BytesIO()
        Image.new('RGB', (100, 100), color=(10, 50, 100)).save(img_io, 'JPEG')
        img_io.seek(0)

        res = self.client.post('/register', data={
            'first_name': 'Young',
            'last_name': 'Student',
            'email': 'young.kid.2015@gmail.com',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'specialty': 'Computer Science & IT',
            'country': 'United States',
            'date_of_birth': '2015-06-20',  # Younger than 2012!
            'photo': (img_io, 'photo.jpg', 'image/jpeg')
        }, follow_redirects=False)

        # Must not redirect to card (must re-render with error status 200)
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('2012', html)
        self.assertIn('Registration is not accepted for applicants younger than 2012', html)

    def test_accept_applicant_born_in_2012(self):
        """Applicants born in 2012 (e.g. 2012-09-10) must be accepted"""
        img_io = io.BytesIO()
        Image.new('RGB', (100, 100), color=(10, 50, 100)).save(img_io, 'JPEG')
        img_io.seek(0)

        test_email = 'student.born.2012@gmail.com'
        # Clean if exists
        with app.app.app_context():
            with database.get_db() as conn:
                conn.execute("DELETE FROM users WHERE email = ?", (test_email,))
                conn.commit()

        res = self.client.post('/register', data={
            'first_name': 'Alex',
            'last_name': 'Carter',
            'email': test_email,
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'specialty': 'Software Engineering',
            'country': 'United States',
            'date_of_birth': '2012-09-10',  # Exactly 2012!
            'photo': (img_io, 'photo.jpg', 'image/jpeg')
        }, follow_redirects=False)

        self.assertEqual(res.status_code, 302)
        self.assertIn('/student-card', res.location)

        # Follow redirect and check card renders
        res_card = self.client.get(res.location)
        self.assertEqual(res_card.status_code, 200)
        card_html = res_card.data.decode('utf-8')
        self.assertIn('Alex', card_html)
        self.assertIn('Carter', card_html)
        self.assertIn('2012-09-10', card_html)

    def test_deep_navy_blue_card_styling_and_american_touch(self):
        """Card must have Deep Navy Blue styling (#030d22, #091f4d) and American touch"""
        res = self.client.get('/student-card/1')
        self.assertEqual(res.status_code, 200)
        card_html = res.data.decode('utf-8')
        
        # Check Deep Navy Blue theme
        self.assertIn('#030d22', card_html)
        self.assertIn('#091f4d', card_html)

        # Check American collegiate touch elements
        self.assertIn('USA ACTIVE', card_html)
        self.assertIn('American Collegiate Pass', card_html)
        self.assertIn('from-red-600 via-white to-blue-600', card_html)
        self.assertIn('PHILADELPHIA <span class="text-red-500">CAMPUS</span>', card_html)
        self.assertIn('EST. 1776', card_html)
        self.assertIn('Official Matricule', card_html)

    def test_registration_form_max_attribute_is_2012(self):
        """Register form input must have max='2012-12-31'"""
        res = self.client.get('/register')
        self.assertEqual(res.status_code, 200)
        html = res.data.decode('utf-8')
        self.assertIn('max="2012-12-31"', html)

if __name__ == '__main__':
    unittest.main()
