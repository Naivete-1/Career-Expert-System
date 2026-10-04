# 🤖 Rule-Based Career Expert System
A Python-based rule-driven expert system that provides personalized career guidance by evaluating a user's interests, skills, and academic background against a structured career knowledge base.

**Completed:** 2024
**Project Type:** Academic / Computer Engineering
**Primary Language:** Python

## 📌 Overview

The Career Expert System is a **rule-based expert system** designed to provide personalized career guidance.

Instead of relying on large datasets or machine-learning models, the system uses **knowledge representation and IF-THEN rules** developed from career counselling concepts, job descriptions, and academic programme requirements.

The user completes a structured questionnaire covering areas such as:

* Interests
* Skills
* Academic background

The system evaluates the responses against its rule base and infers suitable career paths and areas of specialization.

## 🎯 Problem

Choosing an appropriate career path can be difficult when students and other users have limited access to personalized career guidance.

The project addresses this by providing an **automated, accessible and consistent** form of career guidance through a software-based expert system.

## 💡 Solution

The system models relationships between user characteristics and potential careers.

For example:

```text
Interests
    +
Skills
    +
Academic Background
        ↓
 IF-THEN Rules
        ↓
Inference Engine
        ↓
Career Recommendations
```

Possible characteristics include:

**Interests**

* Analytical
* Artistic
* Social

**Skills**

* Programming
* Communication
* Problem-solving

**Academic Background**

* Sciences
* Engineering
* Humanities

These characteristics can be evaluated against career paths such as:

* Software Engineer
* Nurse
* Teacher
* Graphic Designer
## 🧠 Expert-System Architecture

The system is divided into three main modules.

### 1. User Interaction Module

Provides the interface through which users interact with the system.

It is responsible for:

* Displaying questions
* Collecting user responses
* Validating input
* Presenting career recommendations

### 2. Inference Engine

The inference engine performs the **rule-based reasoning**.

It compares the user's responses against the system's IF-THEN rules and identifies career recommendations when the required conditions are satisfied.

The system can also consider the number of conditions satisfied when determining suitable recommendations.

### 3. Knowledge Base Management

The knowledge base stores the career-related rules and information used by the inference engine.

It includes:

* Career category definitions
* Relationships between academic backgrounds and careers
* Relationships between interests, skills and professions
* Career descriptions and supporting information

## 🛠️ Technologies Used

### Python

Python was used as the primary development language because of its suitability for application development, AI-related projects and implementation of rule-based logic.

### Kivy

Kivy was used to develop the graphical user interface and provide an interactive application through which users complete the questionnaire and receive recommendations.

### SQLite

SQLite provides lightweight, persistent data storage without requiring an external database server.

## 🗄️ Database

The project uses an SQLite database to store the career-related information used by the application.

The database development process includes:

1. Creating the database structure
2. Creating the required tables
3. Inserting career information
4. Retrieving data during system operation

### Database Scripts

* **`Career Database creation.py`** — creates the database and its structure.
* **`Career Database insertion.py`** — populates the database with career-related information.

## 🔄 System Workflow

```text
User
 ↓
Questionnaire
 ↓
Input Validation
 ↓
User Characteristics
 ↓
Inference Engine
 ↓
IF-THEN Rule Evaluation
 ↓
Knowledge Base
 ↓
Career Recommendation
```

The system processes the user's answers and evaluates them against the available rules before producing appropriate career recommendations.

## 📂 Project Structure

```text
Career-Expert-System/
│
├── README.md
├── Career_Expert_System.py
├── Career Database creation.py
├── Career Database insertion.py
├── career_expert_system.db
├── Career_Expert_System_APP
└── Report.pdf
```

| File                           | Description                      |
| ------------------------------ | -------------------------------- |
| `Career_Expert_System.py`      | Main Python source code          |
| `Career Database creation.py`  | Database creation and structure  |
| `Career Database insertion.py` | Career data insertion            |
| `career_expert_system.db`      | SQLite database                  |
| `Career_Expert_System_APP`     | Application/build                |
| `Report.pdf`                   | Complete technical documentation |
| `README.md`                    | Project documentation            |

## 🧩 Key Technical Concepts

This project demonstrates practical application of:

* Rule-based artificial intelligence
* Expert systems
* Knowledge representation
* IF-THEN reasoning
* Inference engines
* Python programming
* GUI development
* Kivy
* SQLite databases
* Database integration
* User input processing
* Career knowledge modelling
* 
## 📄 Documentation

The complete project report is available in **`Rule%20Based%20Expert%20System%20for%20career%20guidance%20project.pdf`**.

The report provides additional information about the system requirements, architecture, modules, implementation and development process.

## 🚀 Potential Future Improvements

* Expand the career knowledge base
* Add more career categories and rules
* Improve recommendation ranking
* Provide explanations for each recommendation
* Add user profiles and recommendation history
* Develop a web-based version
* Add more sophisticated reasoning mechanisms
* Extend the system to support additional educational and career pathways

