# insert_data.py
import sqlite3
DB = "career_expert_system.db"

def insert():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    # Careers and descriptions
    careers = [
        ("Psychologist", "Counselling, therapy and research in human behaviour"),
        ("Radiographer", "Diagnostic imaging and radiography"),
        ("Occupational Therapist", "Help patients regain daily living skills"),
        ("Surgeon", "Surgical procedures and patient care"),
        ("Financial Analyst", "Financial forecasting, analysis and planning"),
        ("Entrepreneur", "Founding and running businesses"),
        ("Mechanical Engineer", "Design and analysis of mechanical systems"),
        ("Data Scientist", "Statistical analysis, machine learning and data pipelines"),
        ("Software Engineer", "Design and development of software systems"),
        ("Creative Designer", "Branding, graphic design and visual storytelling"),
        ("Digital Designer", "UI/UX, front-end and digital product design"),
        ("Teacher", "Classroom teaching and pedagogy"),
        ("Accountant", "Financial records, auditing and accounting"),
    ]
    cur.executemany("INSERT INTO careers (career, description) VALUES (?, ?)", careers)
    conn.commit()

    # Helper to get career id quickly
    def cid(name):
        cur.execute("SELECT id FROM careers WHERE career=?", (name,))
        return cur.fetchone()[0]

    # Rules list: (career_id, stage, education_level, subjects, skills, interests, min_cgpa)
    rules = [
        # Psychologist
        (cid("Psychologist"), "highschool", None,
         "psychology,statistics,neuroscience,counselling,research methods",
         "empathy,counselling,therapy techniques,ethical practice",
         "mental health,neuroscience,physiology,philosophy,human behavior", None),
        (cid("Psychologist"), "university", "BSc,BA,Masters,PhD",
         "psychology",
         "empathy,counselling,therapy techniques,ethical practice,research",
         "mental health,neuroscience,physiology,human behavior", 3.0),

        # Radiographer
        (cid("Radiographer"), "highschool", None,
         "physics,biology,anatomy",
         "anatomy knowledge,patient positioning,radiation safety",
         "technology,medical equipment,anatomy,diagnostic imaging", None),
        (cid("Radiographer"), "university", "BSc,HND",
         "anatomy,physics",
         "anatomy knowledge,patient positioning,radiation safety,attention to detail",
         "technology,medical equipment,anatomy,diagnostic imaging", 2.5),

        # Occupational Therapist
        (cid("Occupational Therapist"), "highschool", None,
         "health sciences,biology",
         "empathy,patient assessment,rehabilitation",
         "helping people,psychology,anatomy,practical problem solving", None),
        (cid("Occupational Therapist"), "university", "BSc,Masters",
         "psychology,anatomy,kinesiology",
         "empathy,patient assessment,rehabilitation",
         "helping people,psychology,anatomy,practical problem solving", 3.0),

        # Surgeon
        (cid("Surgeon"), "highschool", None,
         "biology,chemistry,physics",
         "motor skills,anatomy,leadership,surgical techniques",
         "biology,medical innovation,high precision,patient care", None),
        (cid("Surgeon"), "university", "MBBS,MBChB,MD",
         "biology,anatomy,physiology",
         "motor skills,anatomy,leadership,surgical techniques",
         "biology,medical innovation,high precision,patient care", 3.5),

        # Financial Analyst
        (cid("Financial Analyst"), "highschool", None,
         "mathematics,economics,accounting",
         "forecasting,analysis,budgeting,strategic planning,excel",
         "investing,accounting,business,risk assessment", None),
        (cid("Financial Analyst"), "university", "BSc,BA,Masters",
         "finance,accounting,economics,applied mathematics",
         "forecasting,analysis,budgeting,strategic planning,excel",
         "investing,accounting,business,risk assessment", 3.0),

        # Accountant
        (cid("Accountant"), "highschool", None,
         "mathematics,accounting,economics",
         "financial reporting,excel,attention to detail",
         "accounting,finance,compliance", None),
        (cid("Accountant"), "university", "BCom,BSc,ACCA",
         "accounting,finance,economics",
         "financial reporting,auditing,excel,attention to detail",
         "accounting,finance,compliance", 3.0),

        # Entrepreneur
        (cid("Entrepreneur"), "highschool", None,
         "business,economics",
         "negotiation,leadership,problem solving,adaptability",
         "business strategy,networking,market growth", None),
        (cid("Entrepreneur"), "university", "BSc,BA,Masters",
         "business,entrepreneurship,marketing,finance",
         "negotiation,leadership,problem solving,adaptability,risk management",
         "business strategy,networking,market growth", 2.5),

        # Mechanical Engineer
        (cid("Mechanical Engineer"), "highschool", None,
         "physics,mathematics,design technology",
         "thermodynamics,kinematics,physics,system design",
         "automotive,aerospace,robotics,sustainable energy", None),
        (cid("Mechanical Engineer"), "university", "BEng,BSc,Masters",
         "physics,applied mathematics,material science,computer science",
         "thermodynamics,kinematics,system design,simulation",
         "automotive,aerospace,robotics,sustainable energy", 3.0),

        # Data Scientist
        (cid("Data Scientist"), "university", "BSc,Masters,PhD",
         "statistics,computer science,mathematics",
         "python,r,c++,statistical analysis,data visualization,machine learning",
         "problem solving,economics,ai,robotics,data analysis", 3.2),

        # Software Engineer
        (cid("Software Engineer"), "highschool", None,
         "mathematics,computer science",
         "programming,python,c++,java,data structures,algorithms",
         "problem solving,software development,logic,continuous learning", None),
        (cid("Software Engineer"), "university", "BSc,BEng,Masters",
         "computer science,engineering,data structures,algorithms",
         "programming,python,c++,java,data structures,algorithms",
         "problem solving,software development,logic,continuous learning", 3.0),

        # Creative Designer
        (cid("Creative Designer"), "highschool", None,
         "art,media studies,design",
         "illustrator,photoshop,designing,branding,typography",
         "art,storytelling,aesthetics,advertising,visual communication", None),
        (cid("Creative Designer"), "university", "BA,BDes,Masters",
         "graphic design,fine arts,marketing,communication,media studies",
         "illustrator,photoshop,designing,branding,typography",
         "art,storytelling,aesthetics,advertising,visual communication", 2.8),

        # Digital Designer
        (cid("Digital Designer"), "highschool", None,
         "art,computer science,media studies",
         "graphics,visual design,mobile standards",
         "front-end development,web design,digital art", None),
        (cid("Digital Designer"), "university", "BSc,BA,BDes",
         "digital design,ux,ui,web development",
         "graphics,visual design,mobile standards,ui ux",
         "front-end development,web design,digital art", 3.0),

        # Teacher
        (cid("Teacher"), "highschool", None,
         "mathematics,language,science,history",
         "communication,patience,teaching,lesson planning",
         "education,helping others,mentoring", None),
        (cid("Teacher"), "university", "BEd,BSc,PGCE,Masters",
         "education,subject specialization",
         "communication,patience,lesson planning,assessment",
         "education,helping others,learning", 2.5),
    ]

    cur.executemany("""
    INSERT INTO career_rules (
        career_id, stage, education_level, subjects, skills, interests, min_cgpa
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rules)

    conn.commit()
    conn.close()
    print("Inserted careers and rules into", DB)

if __name__ == "__main__":
    insert()
