# career_expert_app.py
import os
import sqlite3
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

DB = "career_expert_system.db"

# --- Database Creation and Sample Data ---
if not os.path.exists(DB):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    # Users
    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        stage TEXT
    )""")
    # Careers
    cur.execute("""CREATE TABLE IF NOT EXISTS careers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career TEXT
    )""")
    # Career rules
    cur.execute("""CREATE TABLE IF NOT EXISTS career_rules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        career_id INTEGER,
        stage TEXT,
        education_level TEXT,
        subjects TEXT,
        skills TEXT,
        interests TEXT,
        min_cgpa REAL,
        FOREIGN KEY(career_id) REFERENCES careers(id)
    )""")
    # User choices
    cur.execute("""CREATE TABLE IF NOT EXISTS user_choices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        stage TEXT,
        subjects TEXT,
        subject_grades TEXT,
        skills TEXT,
        interests TEXT,
        education_level TEXT,
        cgpa REAL
    )""")
    # Sample careers
    careers = ["Software Engineer", "Graphic Designer", "Data Analyst", "Nurse", "Psychologist", "Mechanical Engineer"]
    for c in careers:
        cur.execute("INSERT INTO careers (career) VALUES (?)", (c,))
    # Sample rules
    cur.execute("SELECT id, career FROM careers")
    rows = cur.fetchall()
    for career_id, career in rows:
        if career == "Software Engineer":
            cur.execute("""INSERT INTO career_rules 
                (career_id, stage, subjects, skills, interests, education_level, min_cgpa) 
                VALUES (?, 'university', 'Maths,Physics,Computer Science', 'Python,C++,Algorithms,Data Structures', 'Technology,Software Development,Logic', 'BSc,BEng,Masters', 3.0)""", (career_id,))
        elif career == "Graphic Designer":
            cur.execute("""INSERT INTO career_rules 
                (career_id, stage, subjects, skills, interests) 
                VALUES (?, 'highschool', 'Arts,Design', 'Photoshop,Illustrator,Typography', 'Art,Storytelling,Advertising')""", (career_id,))
        elif career == "Data Analyst":
            cur.execute("""INSERT INTO career_rules 
                (career_id, stage, subjects, skills, interests, education_level, min_cgpa) 
                VALUES (?, 'university', 'Maths,Statistics,Computer Science', 'Excel,Python,Data Visualization,Analysis', 'Research,Logic,Continuous Learning', 'BSc,Masters', 3.0)""", (career_id,))
        elif career == "Nurse":
            cur.execute("""INSERT INTO career_rules 
                (career_id, stage, subjects, skills, interests) 
                VALUES (?, 'highschool', 'Biology,Chemistry', 'Patient Care,Empathy,Observation', 'Helping People,Medical Equipment,Patient Care')""", (career_id,))
        elif career == "Psychologist":
            cur.execute("""INSERT INTO career_rules 
                (career_id, stage, subjects, skills, interests, education_level, min_cgpa) 
                VALUES (?, 'university', 'Psychology,Biology', 'Counselling,Research,Empathy', 'Mental Health,Human Behavior,Philosophy', 'BSc,Masters', 3.0)""", (career_id,))
        elif career == "Mechanical Engineer":
            cur.execute("""INSERT INTO career_rules 
                (career_id, stage, subjects, skills, interests, education_level, min_cgpa) 
                VALUES (?, 'university', 'Maths,Physics', 'Problem Solving,Design,Analysis', 'Robotics,Automotive,Sustainable Energy', 'BSc,BEng,Masters', 3.0)""", (career_id,))
    conn.commit()
    conn.close()
    print("Database created with sample data.")

# --- Database helper functions ---
def fetch_rules(stage):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("""SELECT c.career, r.education_level, r.subjects, r.skills, r.interests, r.min_cgpa
                   FROM career_rules r JOIN careers c ON c.id=r.career_id WHERE r.stage=?""", (stage,))
    rows = cur.fetchall()
    conn.close()
    return rows

def save_user(username, stage, subjects, subject_grades, skills, interests, education_level=None, cgpa=None):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    subj_str = ",".join(subjects)
    grades_str = ",".join(f"{k}:{v}" for k,v in subject_grades.items())
    skills_str = ",".join(skills)
    interests_str = ",".join(interests)
    cur.execute("""INSERT INTO user_choices (username, stage, subjects, subject_grades, skills, interests, education_level, cgpa)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (username, stage, subj_str, grades_str, skills_str, interests_str, education_level, cgpa))
    conn.commit()
    conn.close()

def recommend_careers(stage, subjects, subject_grades, skills, interests, education_level=None, cgpa=None, top_n=2):
    rules = fetch_rules(stage)
    user_subs = set(s.lower() for s in subjects)
    user_skills = set(s.lower() for s in skills)
    user_interests = set(i.lower() for i in interests)
    scored = []
    for career, rule_edu, rule_subs, rule_skills, rule_interests, min_cgpa in rules:
        rule_subs_set = set(s.strip().lower() for s in (rule_subs or "").split(",") if s.strip())
        rule_skills_set = set(s.strip().lower() for s in (rule_skills or "").split(",") if s.strip())
        rule_interests_set = set(i.strip().lower() for i in (rule_interests or "").split(",") if i.strip())
        rule_edu_set = set(e.strip().lower() for e in (rule_edu or "").split(",") if e.strip())

        # University/Graduate checks
        if stage in ("university","graduate"):
            if rule_edu_set and education_level:
                if education_level.strip().lower() not in rule_edu_set:
                    continue
            if min_cgpa and cgpa is not None:
                if cgpa < min_cgpa:
                    continue
            skill_matches = len(user_skills & rule_skills_set)
            interest_matches = len(user_interests & rule_interests_set)
            if skill_matches < 1 or interest_matches < 1:
                continue
            score = skill_matches*2 + interest_matches + len(user_subs & rule_subs_set)
            if score > 0:
                scored.append((career, score))
        # Highschool checks
        else:
            if rule_subs_set:
                overlap = user_subs & rule_subs_set
                coverage = len(overlap)/len(rule_subs_set)
                if coverage < 0.5:
                    continue
                bad = False
                for s in overlap:
                    g = subject_grades.get(s.lower(),0)
                    if g < 50:
                        bad=True
                        break
                if bad:
                    continue
            skill_matches = len(user_skills & rule_skills_set)
            interest_matches = len(user_interests & rule_interests_set)
            if skill_matches <1 or interest_matches <1:
                continue
            score = skill_matches*2 + interest_matches + len(user_subs & rule_subs_set)
            if score>0:
                scored.append((career,score))
    scored.sort(key=lambda x:x[1], reverse=True)
    return [c for c,_ in scored[:top_n]]

# --- Master lists ---
SUBJECTS_MASTER=["Maths","Physics","Chemistry","Biology","Computer Science","IT","Engineering","Arts","Design","Media","Psychology","Statistics","Neuroscience"]
SKILLS_MASTER=["Empathy","Counselling","Therapy Techniques","Ethical Practice","Anatomy Knowledge","Patient Positioning","Radiation Safety","Motor Skills","Leadership","Surgical Techniques","Forecasting","Analysis","Budgeting","Strategic Planning","Problem Solving","Adaptability","Programming","Python","C++","R","Data Structures","Algorithms","Statistical Analysis","Data Visualization","Illustrator","Photoshop","Designing","Branding","Typography","Teaching","Communication","Rehabilitation","Patient Assessment","Excel"]
INTERESTS_MASTER=["Mental Health","Neuroscience","Physiology","Philosophy","Human Behavior","Technology","Medical Equipment","Diagnostic Imaging","Helping People","Biology","Medical Innovation","High Precision","Patient Care","Investing","Accounting","Business","Risk Assessment","Business Strategy","Networking","Market Growth","Automotive","Aerospace","Robotics","Sustainable Energy","Software Development","Logic","Continuous Learning","Art","Storytelling","Aesthetics","Advertising","Visual Communication","Education","Child Development","Learning","Research","Finance","Economics","AI","Machine Learning"]

# --- GUI Screens ---
class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        box=BoxLayout(orientation='vertical',padding=12,spacing=8)
        box.add_widget(Label(text="Career Expert System — Login / Register",size_hint_y=None,height=40))
        box.add_widget(Label(text="Username",size_hint_y=None,height=24))
        self.username_in=TextInput(multiline=False,size_hint_y=None,height=40)
        box.add_widget(self.username_in)
        box.add_widget(Label(text="Password",size_hint_y=None,height=24))
        self.password_in=TextInput(password=True,multiline=False,size_hint_y=None,height=40)
        box.add_widget(self.password_in)
        box.add_widget(Label(text="Stage (highschool/university/graduate)",size_hint_y=None,height=28))
        self.stage_in=TextInput(multiline=False,size_hint_y=None,height=40)
        box.add_widget(self.stage_in)

        btn_row=BoxLayout(size_hint_y=None,height=50,spacing=8)
        reg=Button(text="Register")
        login=Button(text="Login")
        reg.bind(on_release=self.do_register)
        login.bind(on_release=self.do_login)
        btn_row.add_widget(reg)
        btn_row.add_widget(login)
        box.add_widget(btn_row)
        self.add_widget(box)

    def do_register(self,*args):
        user=self.username_in.text.strip()
        pwd=self.password_in.text.strip()
        stg=self.stage_in.text.strip().lower()
        if not user or not pwd or stg not in ("highschool","university","graduate"):
            Popup(title="Error",content=Label(text="Enter username, password and valid stage."),size_hint=(0.7,0.4)).open()
            return
        conn=sqlite3.connect(DB)
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO users (username,password,stage) VALUES (?,?,?)",(user,pwd,stg))
            conn.commit()
            Popup(title="Success",content=Label(text="Registered. Now login."),size_hint=(0.6,0.3)).open()
        except sqlite3.IntegrityError:
            Popup(title="Error",content=Label(text="Username exists."),size_hint=(0.6,0.3)).open()
        finally:
            conn.close()

    def do_login(self,*args):
        user=self.username_in.text.strip()
        pwd=self.password_in.text.strip()
        stg=self.stage_in.text.strip().lower()
        if not user or not pwd or stg not in ("highschool","university","graduate"):
            Popup(title="Error",content=Label(text="Enter username, password and valid stage."),size_hint=(0.7,0.4)).open()
            return
        conn=sqlite3.connect(DB)
        cur=conn.cursor()
        cur.execute("SELECT id FROM users WHERE username=? AND password=?",(user,pwd))
        ok=cur.fetchone() is not None
        conn.close()
        if ok:
            app=App.get_running_app()
            app.username=user
            app.stage=stg
            self.manager.current="subjects"
        else:
            Popup(title="Error",content=Label(text="Invalid credentials."),size_hint=(0.6,0.3)).open()

# --- Subjects Screen ---
class SubjectsScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        layout=BoxLayout(orientation='vertical',spacing=8,padding=8)
        layout.add_widget(Label(text="Step 1 — Select Subjects & enter grades (mandatory for highschool)",size_hint_y=None,height=36))
        scroll=ScrollView(size_hint=(1,0.78))
        grid=GridLayout(cols=3,spacing=8,size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.controls=[]
        for subj in SUBJECTS_MASTER:
            lbl=Label(text=subj,size_hint_y=None,height=32)
            cb=CheckBox(size_hint=(None,None),size=(30,30))
            grade=TextInput(text="",multiline=False,size_hint_y=None,height=32,input_filter='float')
            grid.add_widget(lbl)
            grid.add_widget(cb)
            grid.add_widget(grade)
            self.controls.append((subj,cb,grade))
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        nav=BoxLayout(size_hint=(1,0.12),spacing=8)
        back=Button(text="Back")
        next_btn=Button(text="Next: Skills")
        back.bind(on_release=self.go_back)
        next_btn.bind(on_release=self.collect_subjects)
        nav.add_widget(back)
        nav.add_widget(next_btn)
        layout.add_widget(nav)
        self.add_widget(layout)

    def go_back(self,*args):
        self.manager.current="login"

    def collect_subjects(self,*args):
        app=App.get_running_app()
        selected=[]
        grades={}
        for name,cb,grade in self.controls:
            if cb.active:
                selected.append(name.lower())
                try:
                    g=float(grade.text.strip()) if grade.text.strip() else 0.0
                except:
                    g=0.0
                grades[name.lower()]=g
        app.selected_subjects=selected
        app.subject_grades=grades
        self.manager.current="skills"

# --- Skills Screen ---
class SkillsScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        layout=BoxLayout(orientation='vertical',spacing=8,padding=8)
        layout.add_widget(Label(text="Step 2 — Select Skills",size_hint_y=None,height=36))
        scroll=ScrollView(size_hint=(1,0.78))
        grid=GridLayout(cols=2,spacing=8,size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.skill_boxes=[]
        for s in SKILLS_MASTER:
            lbl=Label(text=s,size_hint_y=None,height=30)
            cb=CheckBox(size_hint=(None,None),size=(30,30))
            grid.add_widget(lbl)
            grid.add_widget(cb)
            self.skill_boxes.append((s,cb))
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        nav=BoxLayout(size_hint=(1,0.12),spacing=8)
        back=Button(text="Back")
        next_btn=Button(text="Next: Interests")
        back.bind(on_release=self.go_back)
        next_btn.bind(on_release=self.collect_skills)
        nav.add_widget(back)
        nav.add_widget(next_btn)
        layout.add_widget(nav)
        self.add_widget(layout)

    def go_back(self,*args):
        self.manager.current="subjects"

    def collect_skills(self,*args):
        app=App.get_running_app()
        app.selected_skills=[name.lower() for name,cb in self.skill_boxes if cb.active]
        self.manager.current="interests"

# --- Interests Screen ---
class InterestsScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        layout=BoxLayout(orientation='vertical',spacing=8,padding=8)
        layout.add_widget(Label(text="Step 3 — Select Interests",size_hint_y=None,height=36))
        scroll=ScrollView(size_hint=(1,0.7))
        grid=GridLayout(cols=2,spacing=8,size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        self.interest_boxes=[]
        for i in INTERESTS_MASTER:
            lbl=Label(text=i,size_hint_y=None,height=30)
            cb=CheckBox(size_hint=(None,None),size=(30,30))
            grid.add_widget(lbl)
            grid.add_widget(cb)
            self.interest_boxes.append((i,cb))
        scroll.add_widget(grid)
        layout.add_widget(scroll)
        nav=BoxLayout(size_hint=(1,0.18),spacing=8)
        back=Button(text="Back")
        back.bind(on_release=self.go_back)
        proceed=Button(text="Get Recommendations")
        proceed.bind(on_release=self.prepare_recommend)
        nav.add_widget(back)
        nav.add_widget(proceed)
        layout.add_widget(nav)
        self.add_widget(layout)

    def go_back(self,*args):
        self.manager.current="skills"

    def prepare_recommend(self,*args):
        app=App.get_running_app()
        app.selected_interests=[name.lower() for name,cb in self.interest_boxes if cb.active]

        if getattr(app,"stage","highschool") in ("university","graduate"):
            content=BoxLayout(orientation='vertical',spacing=8,padding=8)
            content.add_widget(Label(text="Enter education level (BSc, Masters, etc)"))
            edu_in=TextInput(multiline=False)
            content.add_widget(edu_in)
            content.add_widget(Label(text="Enter CGPA (e.g. 3.2)"))
            cgpa_in=TextInput(multiline=False,input_filter='float')
            content.add_widget(cgpa_in)
            btn=Button(text="Continue",size_hint=(1,0.2))
            content.add_widget(btn)
            popup=Popup(title="Education & CGPA",content=content,size_hint=(0.8,0.6))
            def on_continue(*a):
                app.education_level=edu_in.text.strip()
                try:
                    app.cgpa=float(cgpa_in.text.strip())
                except:
                    app.cgpa=None
                popup.dismiss()
                self.manager.current="results"
            btn.bind(on_release=on_continue)
            popup.open()
        else:
            self.manager.current="results"

# --- Results Screen ---
class ResultsScreen(Screen):
    def __init__(self,**kw):
        super().__init__(**kw)
        self.layout=BoxLayout(orientation='vertical',padding=8,spacing=8)
        self.layout.add_widget(Label(text="Step 4 — Recommended Careers",size_hint_y=None,height=36))
        self.results_box=BoxLayout(orientation='vertical',spacing=4)
        self.layout.add_widget(self.results_box)
        nav=BoxLayout(size_hint=(1,0.12))
        restart=Button(text="Start Over")
        restart.bind(on_release=self.start_over)
        nav.add_widget(restart)
        self.layout.add_widget(nav)
        self.add_widget(self.layout)

    def on_enter(self,*args):
        app=App.get_running_app()
        recs=recommend_careers(
            stage=getattr(app,"stage","highschool"),
            subjects=getattr(app,"selected_subjects",[]),
            subject_grades=getattr(app,"subject_grades",{}),
            skills=getattr(app,"selected_skills",[]),
            interests=getattr(app,"selected_interests",[]),
            education_level=getattr(app,"education_level",None),
            cgpa=getattr(app,"cgpa",None),
            top_n=5
        )
        self.results_box.clear_widgets()
        if not recs:
            self.results_box.add_widget(Label(text="No careers match your inputs."))
        else:
            for c in recs:
                self.results_box.add_widget(Label(text=f"- {c}"))

    def start_over(self,*args):
        self.manager.current="login"

# --- Main App ---
class CareerApp(App):
    def build(self):
        self.username=""
        self.stage=""
        self.selected_subjects=[]
        self.subject_grades={}
        self.selected_skills=[]
        self.selected_interests=[]
        self.education_level=None
        self.cgpa=None
        sm=ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SubjectsScreen(name="subjects"))
        sm.add_widget(SkillsScreen(name="skills"))
        sm.add_widget(InterestsScreen(name="interests"))
        sm.add_widget(ResultsScreen(name="results"))
        return sm

if __name__=="__main__":
    CareerApp().run()
