import sqlite3
from werkzeug.security import generate_password_hash
from database import DATABASE, init_db, migrate_db

SAMPLE_DIRECTORS = [
    {
        "full_name": "Dr. Arthur Pendelton",
        "first_name": "Arthur",
        "last_name": "Pendelton",
        "date_of_birth": "1972-04-12",
        "student_id_code": "DIR-ADMIN-01",
        "photo_url": "",
        "email": "director@philadelphia.edu",
        "password": "director2026",
        "specialty": "University Administration",
        "country": "United States",
        "bio": "Executive Campus Director & Dean of Academic Admissions at Philadelphia Campus.",
        "avatar_color": "#DC2626",
        "role": "director",
        "academic_year": "Administration",
        "class_name": "Office of the Dean",
        "living_street": "1 College Hall, University Plaza, Philadelphia, PA",
        "parents_name": "N/A (Executive Staff)",
        "parents_phone": "+1 (215) 555-0100"
    }
]

SAMPLE_TEACHERS = [
    {
        "full_name": "Prof. Robert Langdon",
        "first_name": "Robert",
        "last_name": "Langdon",
        "date_of_birth": "1980-06-25",
        "student_id_code": "FAC-CS-101",
        "photo_url": "",
        "email": "teacher.cs@philadelphia.edu",
        "password": "teacher2026",
        "specialty": "Computer Science & IT",
        "country": "United States",
        "bio": "Chair Professor of Computer Science. Specializing in Algorithms, Distributed Systems, and AI.",
        "avatar_color": "#1E3A8A",
        "role": "teacher",
        "academic_year": "Faculty",
        "class_name": "Dept. of Computer Science",
        "living_street": "3401 Walnut St, Philadelphia, PA",
        "parents_name": "Faculty Staff",
        "parents_phone": "+1 (215) 555-0142"
    },
    {
        "full_name": "Dr. Claire Fontaine",
        "first_name": "Claire",
        "last_name": "Fontaine",
        "date_of_birth": "1984-09-18",
        "student_id_code": "FAC-MED-201",
        "photo_url": "",
        "email": "teacher.med@philadelphia.edu",
        "password": "teacher2026",
        "specialty": "Medicine & Healthcare",
        "country": "France",
        "bio": "Clinical Professor of Human Anatomy and Emergency Therapeutics.",
        "avatar_color": "#B91C1C",
        "role": "teacher",
        "academic_year": "Faculty",
        "class_name": "School of Medicine",
        "living_street": "420 Curie Blvd, Philadelphia, PA",
        "parents_name": "Faculty Staff",
        "parents_phone": "+1 (215) 555-0188"
    },
    {
        "full_name": "Prof. Jonathan Hayes",
        "first_name": "Jonathan",
        "last_name": "Hayes",
        "date_of_birth": "1978-03-30",
        "student_id_code": "FAC-BUS-301",
        "photo_url": "",
        "email": "teacher.bus@philadelphia.edu",
        "password": "teacher2026",
        "specialty": "Business Administration & Management",
        "country": "United States",
        "bio": "Professor of Corporate Finance and Entrepreneurial Strategy.",
        "avatar_color": "#172554",
        "role": "teacher",
        "academic_year": "Faculty",
        "class_name": "School of Business",
        "living_street": "3620 Locust Walk, Philadelphia, PA",
        "parents_name": "Faculty Staff",
        "parents_phone": "+1 (215) 555-0199"
    },
    {
        "full_name": "Dr. Frank Miller",
        "first_name": "Frank",
        "last_name": "Miller",
        "date_of_birth": "1982-12-05",
        "student_id_code": "FAC-ENG-401",
        "photo_url": "",
        "email": "teacher.eng@philadelphia.edu",
        "password": "teacher2026",
        "specialty": "Mechanical Engineering",
        "country": "United States",
        "bio": "Senior Lecturer in Robotics, Mechatronics and Thermodynamics.",
        "avatar_color": "#2563EB",
        "role": "teacher",
        "academic_year": "Faculty",
        "class_name": "Dept. of Mechanical Engineering",
        "living_street": "220 S 33rd St, Philadelphia, PA",
        "parents_name": "Faculty Staff",
        "parents_phone": "+1 (215) 555-0155"
    },
    {
        "full_name": "Prof. Eleanor Vance",
        "first_name": "Eleanor",
        "last_name": "Vance",
        "date_of_birth": "1981-08-14",
        "student_id_code": "FAC-LAW-501",
        "photo_url": "",
        "email": "teacher.law@philadelphia.edu",
        "password": "teacher2026",
        "specialty": "Law & International Relations",
        "country": "United Kingdom",
        "bio": "Distinguished Scholar of Constitutional Jurisprudence & International Treaties.",
        "avatar_color": "#991B1B",
        "role": "teacher",
        "academic_year": "Faculty",
        "class_name": "Faculty of Law",
        "living_street": "3501 Sansom St, Philadelphia, PA",
        "parents_name": "Faculty Staff",
        "parents_phone": "+1 (215) 555-0177"
    }
]

SAMPLE_USERS = [
    {
        "full_name": "Sarah Mansouri",
        "first_name": "Sarah",
        "last_name": "Mansouri",
        "date_of_birth": "2003-09-14",
        "student_id_code": "PC-2026-04182",
        "photo_url": "",
        "email": "sarah.m@student.philadelphia.edu",
        "password": "password123",
        "specialty": "Computer Science & IT",
        "country": "Algeria",
        "bio": "Junior CS student at Philadelphia Campus. Working on artificial intelligence, distributed systems, and campus hackathons.",
        "avatar_color": "#1E3A8A",
        "role": "student",
        "academic_year": "3rd Year (السنة الثالثة)",
        "class_name": "CS-301 / Amphi B",
        "living_street": "742 Evergreen Terrace / Rue Didouche Mourad",
        "parents_name": "Kamel & Nassima Mansouri",
        "parents_phone": "+213 550 12 34 56"
    },
    {
        "full_name": "Lucas Dubois",
        "first_name": "Lucas",
        "last_name": "Dubois",
        "date_of_birth": "2002-11-20",
        "student_id_code": "PC-2026-08391",
        "photo_url": "",
        "email": "lucas.d@student.philadelphia.edu",
        "password": "password123",
        "specialty": "Medicine & Healthcare",
        "country": "France",
        "bio": "Pre-med student at Philadelphia Campus researching clinical diagnostics and human anatomy.",
        "avatar_color": "#DC2626",
        "role": "student",
        "academic_year": "2nd Year (السنة الثانية)",
        "class_name": "MED-204 / Lab 3",
        "living_street": "15 Rue de Rivoli, Paris",
        "parents_name": "Pierre & Sophie Dubois",
        "parents_phone": "+33 6 12 34 56 78"
    },
    {
        "full_name": "Amina El-Sayed",
        "first_name": "Amina",
        "last_name": "El-Sayed",
        "date_of_birth": "2003-04-05",
        "student_id_code": "PC-2026-12749",
        "photo_url": "",
        "email": "amina.e@student.philadelphia.edu",
        "password": "password123",
        "specialty": "Business Administration & Management",
        "country": "Egypt",
        "bio": "Senior business student at Philadelphia Campus. Lead coordinator at the campus entrepreneurship incubator.",
        "avatar_color": "#B91C1C",
        "role": "student",
        "academic_year": "4th Year (السنة الرابعة)",
        "class_name": "BUS-410 / Executive Room",
        "living_street": "22 Tahrir Avenue, Cairo",
        "parents_name": "Mohamed & Fatma El-Sayed",
        "parents_phone": "+20 100 234 5678"
    },
    {
        "full_name": "Marcus Vance",
        "first_name": "Marcus",
        "last_name": "Vance",
        "date_of_birth": "2002-07-28",
        "student_id_code": "PC-2026-15923",
        "photo_url": "",
        "email": "marcus.v@student.philadelphia.edu",
        "password": "password123",
        "specialty": "Mechanical Engineering",
        "country": "United States",
        "bio": "Philadelphia Campus engineering senior. President of the University Robotics & Autonomous Vehicles Society.",
        "avatar_color": "#2563EB",
        "role": "student",
        "academic_year": "3rd Year (السنة الثالثة)",
        "class_name": "ENG-302 / Towne Lab",
        "living_street": "1204 Walnut St, Philadelphia, PA",
        "parents_name": "David & Lisa Vance",
        "parents_phone": "+1 (215) 555-8392"
    },
    {
        "full_name": "Elena Weber",
        "first_name": "Elena",
        "last_name": "Weber",
        "date_of_birth": "2003-01-16",
        "student_id_code": "PC-2026-18402",
        "photo_url": "",
        "email": "elena.w@student.philadelphia.edu",
        "password": "password123",
        "specialty": "Law & International Relations",
        "country": "Germany",
        "bio": "Exchange student at Philadelphia Campus focusing on constitutional law and international trade regulation.",
        "avatar_color": "#172554",
        "role": "student",
        "academic_year": "1st Year (السنة الأولى)",
        "class_name": "LAW-101 / Moot Court A",
        "living_street": "45 Friedrichstraße, Berlin",
        "parents_name": "Hans & Brigitte Weber",
        "parents_phone": "+49 30 1234567"
    },
    {
        "full_name": "Omar Kaci",
        "first_name": "Omar",
        "last_name": "Kaci",
        "date_of_birth": "2004-03-22",
        "student_id_code": "PC-2026-21873",
        "photo_url": "",
        "email": "omar.k@student.philadelphia.edu",
        "password": "password123",
        "specialty": "Computer Science & IT",
        "country": "Algeria",
        "bio": "Sophomore CS student passionate about mobile development, algorithms, and cloud infrastructure.",
        "avatar_color": "#1D4ED8",
        "role": "student",
        "academic_year": "2nd Year (السنة الثانية)",
        "class_name": "CS-202 / Group 1",
        "living_street": "18 Boulevard Zighoud Youcef, Algiers",
        "parents_name": "Farid & Samia Kaci",
        "parents_phone": "+213 770 98 76 54"
    }
]

SAMPLE_POSTS = [
    {
        "user_email": "sarah.m@student.philadelphia.edu",
        "title": "Philadelphia Campus Midterm Revision: Algorithm Analysis & Dynamic Programming study group",
        "content": "Hey everyone! For the upcoming CS 317 exam next Thursday, we have booked study room 304 in Van Pelt Library on Wednesday from 4 PM to 7 PM. We'll be reviewing graph traversal algorithms, Bellman-Ford, and dynamic programming memoization. All Philadelphia Campus CS students are welcome to drop by!",
        "specialty": "Computer Science & IT"
    },
    {
        "user_email": "omar.k@student.philadelphia.edu",
        "title": "Best IDE setup and debugging tools for Operating Systems (CS 421)",
        "content": "Hello fellow CS classmates! What debugger or Linux environment are you using for the multi-threading and semaphore assignment? Looking for recommendations between VS Code Remote SSH and CLion.",
        "specialty": "Computer Science & IT"
    },
    {
        "user_email": "lucas.d@student.philadelphia.edu",
        "title": "Clinical Anatomy flashcards and clinical case discussions for Term 2",
        "content": "Hi fellow pre-med and healthcare students! We've compiled high-yield visual notes for cardiovascular pathology and organ systems. If anyone wants to cross-verify answers for Dr. Miller's weekly lab assignment, let's share notes here.",
        "specialty": "Medicine & Healthcare"
    },
    {
        "user_email": "amina.e@student.philadelphia.edu",
        "title": "Philadelphia Campus Venture Challenge 2026 - Looking for team members!",
        "content": "The annual Philadelphia Campus Venture Challenge submissions open in 3 weeks. Our team is developing an intelligent student notes sharing and peer tutoring app. We are looking for business and marketing students to collaborate on the pitch deck.",
        "specialty": "Business Administration & Management"
    },
    {
        "user_email": "marcus.v@student.philadelphia.edu",
        "title": "3D Printers access in the Engineering Innovation Lab over the weekend",
        "content": "Quick reminder for mechanical engineering students: the makerspace in Towne Hall will have extended open hours this Saturday from 10 AM to 6 PM for capstone project prototyping. Make sure to bring your STL files pre-sliced.",
        "specialty": "Mechanical Engineering"
    },
    {
        "user_email": "elena.w@student.philadelphia.edu",
        "title": "Constitutional Law & International Moot Court competition prep",
        "content": "For our constitutional and international law seminar, we are staging a mock appellate hearing next month. Law students who want to practice oral arguments and treaty citations, let's form a practice bench!",
        "specialty": "Law & International Relations"
    }
]

SAMPLE_COMMENTS = [
    {
        "post_index": 0,
        "author_email": "omar.k@student.philadelphia.edu",
        "content": "I'll definitely be there Sarah! I have some practice problems on Dijkstra and Bellman-Ford that we can solve together."
    },
    {
        "post_index": 0,
        "author_email": "sarah.m@student.philadelphia.edu",
        "content": "Awesome Omar! Bring those along, that will be super helpful for everyone in our CS class."
    },
    {
        "post_index": 1,
        "author_email": "sarah.m@student.philadelphia.edu",
        "content": "I recommend VS Code Remote SSH with the GDB debugging extension. Works smoothly with campus lab servers!"
    }
]

def seed_database():
    print("Initializing Philadelphia Campus database...")
    init_db()
    migrate_db()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # 1. Seed Students
    print("Seeding Student Accounts with Personal Records...")
    student_id_map = {}
    for u in SAMPLE_USERS:
        cursor.execute("SELECT id FROM users WHERE email = ?", (u["email"],))
        existing = cursor.fetchone()
        if existing:
            student_id_map[u["email"]] = existing[0]
            # Update their admin fields if empty
            cursor.execute("""
                UPDATE users SET 
                    academic_year = COALESCE(NULLIF(academic_year, ''), ?),
                    class_name = COALESCE(NULLIF(class_name, ''), ?),
                    living_street = COALESCE(NULLIF(living_street, ''), ?),
                    parents_name = COALESCE(NULLIF(parents_name, ''), ?),
                    parents_phone = COALESCE(NULLIF(parents_phone, ''), ?),
                    role = COALESCE(NULLIF(role, ''), 'student')
                WHERE id = ?
            """, (u["academic_year"], u["class_name"], u["living_street"], u["parents_name"], u["parents_phone"], existing[0]))
        else:
            pwd_hash = generate_password_hash(u["password"])
            cursor.execute(
                """INSERT INTO users (full_name, first_name, last_name, date_of_birth, student_id_code, photo_url, email, password_hash, specialty, country, bio, avatar_color, role, academic_year, class_name, living_street, parents_name, parents_phone)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (u["full_name"], u["first_name"], u["last_name"], u["date_of_birth"], u["student_id_code"], u["photo_url"], u["email"], pwd_hash, u["specialty"], u["country"], u["bio"], u["avatar_color"], u["role"], u["academic_year"], u["class_name"], u["living_street"], u["parents_name"], u["parents_phone"])
            )
            student_id_map[u["email"]] = cursor.lastrowid

    # 2. Seed Director Account
    print("Seeding Director Account...")
    for d in SAMPLE_DIRECTORS:
        cursor.execute("SELECT id FROM users WHERE email = ?", (d["email"],))
        existing = cursor.fetchone()
        if not existing:
            pwd_hash = generate_password_hash(d["password"])
            cursor.execute(
                """INSERT INTO users (full_name, first_name, last_name, date_of_birth, student_id_code, photo_url, email, password_hash, specialty, country, bio, avatar_color, role, academic_year, class_name, living_street, parents_name, parents_phone)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (d["full_name"], d["first_name"], d["last_name"], d["date_of_birth"], d["student_id_code"], d["photo_url"], d["email"], pwd_hash, d["specialty"], d["country"], d["bio"], d["avatar_color"], d["role"], d["academic_year"], d["class_name"], d["living_street"], d["parents_name"], d["parents_phone"])
            )

    # 3. Seed Teachers
    print("Seeding Teacher Accounts...")
    teacher_id_map = {}
    for t in SAMPLE_TEACHERS:
        cursor.execute("SELECT id FROM users WHERE email = ?", (t["email"],))
        existing = cursor.fetchone()
        if existing:
            teacher_id_map[t["specialty"]] = existing[0]
        else:
            pwd_hash = generate_password_hash(t["password"])
            cursor.execute(
                """INSERT INTO users (full_name, first_name, last_name, date_of_birth, student_id_code, photo_url, email, password_hash, specialty, country, bio, avatar_color, role, academic_year, class_name, living_street, parents_name, parents_phone)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (t["full_name"], t["first_name"], t["last_name"], t["date_of_birth"], t["student_id_code"], t["photo_url"], t["email"], pwd_hash, t["specialty"], t["country"], t["bio"], t["avatar_color"], t["role"], t["academic_year"], t["class_name"], t["living_street"], t["parents_name"], t["parents_phone"])
            )
            teacher_id_map[t["specialty"]] = cursor.lastrowid

    # 4. Seed Teacher-Entered Student Grades
    print("Seeding Initial Academic Grades...")
    cs_teacher_id = teacher_id_map.get("Computer Science & IT")
    sarah_id = student_id_map.get("sarah.m@student.philadelphia.edu")
    omar_id = student_id_map.get("omar.k@student.philadelphia.edu")

    sample_grades = []
    if sarah_id:
        sample_grades.extend([
            (sarah_id, cs_teacher_id, "CSC 101: Introduction to Python & Algorithms", 18.5, 20.0, "A+", "Semester 1", "Exemplary algorithmic thinking and recursion mastery"),
            (sarah_id, cs_teacher_id, "CSC 210: Data Structures in C++", 17.5, 20.0, "A", "Semester 1", "Excellent implementation of balanced search trees and graphs"),
            (sarah_id, cs_teacher_id, "CSC 340: Database Management Systems & SQL", 19.0, 20.0, "A+", "Semester 2", "Perfect relational database design and indexing optimization")
        ])
    if omar_id:
        sample_grades.extend([
            (omar_id, cs_teacher_id, "CSC 101: Introduction to Python & Algorithms", 16.0, 20.0, "A-", "Semester 1", "Solid code logic and timely lab submissions"),
            (omar_id, cs_teacher_id, "CSC 210: Data Structures in C++", 15.5, 20.0, "B+", "Semester 1", "Good understanding of linked lists and sorting algorithms")
        ])

    for sg in sample_grades:
        cursor.execute("SELECT id FROM grades WHERE student_id = ? AND subject = ?", (sg[0], sg[2]))
        if not cursor.fetchone():
            cursor.execute("""
                INSERT INTO grades (student_id, teacher_id, subject, score, max_score, grade_letter, semester, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, sg)

    # 5. Seed Discussions
    post_ids = []
    for post in SAMPLE_POSTS:
        author_id = student_id_map.get(post["user_email"])
        if author_id:
            cursor.execute("SELECT id FROM posts WHERE user_id = ? AND title = ?", (author_id, post["title"]))
            existing_post = cursor.fetchone()
            if existing_post:
                post_ids.append(existing_post[0])
            else:
                cursor.execute(
                    """INSERT INTO posts (user_id, title, content, specialty)
                       VALUES (?, ?, ?, ?)""",
                    (author_id, post["title"], post["content"], post["specialty"])
                )
                post_ids.append(cursor.lastrowid)

    # 6. Seed Comments
    for comment in SAMPLE_COMMENTS:
        if comment["post_index"] < len(post_ids):
            pid = post_ids[comment["post_index"]]
            author_id = student_id_map.get(comment["author_email"])
            if author_id and pid:
                cursor.execute("SELECT id FROM comments WHERE post_id = ? AND user_id = ? AND content = ?", (pid, author_id, comment["content"]))
                if not cursor.fetchone():
                    cursor.execute(
                        """INSERT INTO comments (post_id, user_id, content)
                           VALUES (?, ?, ?)""",
                        (pid, author_id, comment["content"])
                    )

    conn.commit()
    conn.close()
    print("Philadelphia Campus database seeded successfully with Director, Teachers, and Personal Student Records!")

if __name__ == '__main__':
    seed_database()
