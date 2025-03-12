import os
from flask import Flask, render_template, abort

app = Flask(__name__)

# Define subjects for each branch and semester (same as before)
subjects_data = {
    'Basic Engineering': {
        '1st Year': {  # Changed from 2nd Year to 1st Year
            'SEM 1': ['Mathematics I', 'Physics I', 'Chemistry I', 'Engineering Drawing'],
            'SEM 2': ['Mathematics II', 'Physics II', 'Chemistry II', 'Basic Electrical Engineering']
        },
        # Keep the other years as they were
        '3rd Year': {
            'SEM 1': ['Data Structures', 'Database Management Systems', 'Computer Networks'],
            'SEM 2': ['Operating Systems', 'Software Engineering', 'Web Technologies']
        },
        '4th Year': {
            'SEM 1': ['Compiler Design', 'Artificial Intelligence'],
            'SEM 2': ['Machine Learning', 'Cloud Computing']
        }
    },
    'Computer': {
        '2nd Year': {
            'SEM 1': ['Data Structures', 'Digital Logic', 'Computer Organization'],
            'SEM 2': ['Algorithms', 'Object-Oriented Programming', 'Database Systems']
        },
        '3rd Year': {
            'SEM 1': ['Operating Systems', 'Computer Networks', 'Web Development'],
            'SEM 2': ['Software Engineering', 'Artificial Intelligence', 'Mobile App Development']
        },
        '4th Year': {
            'SEM 1': ['Cloud Computing', 'Machine Learning', 'Information Security'],
            'SEM 2': ['Big Data Analytics', 'Internet of Things', 'Project Management']
        }
    },
    'AI-DS': {
        '2nd Year': {
            'SEM 1': ['Python Programming', 'Statistics for Data Science', 'Linear Algebra'],
            'SEM 2': ['Data Structures', 'Probability Theory', 'Database Systems']
        },
        '3rd Year': {
            'SEM 1': ['Machine Learning Fundamentals', 'Data Visualization', 'Big Data Technologies'],
            'SEM 2': ['Deep Learning', 'Natural Language Processing', 'Computer Vision']
        },
        '4th Year': {
            'SEM 1': ['Reinforcement Learning', 'AI Ethics', 'Advanced Data Analytics'],
            'SEM 2': ['AI Project', 'Research Methods', 'Industry Applications of AI']
        }
    }
}

# Directory where the HTML notes are stored
NOTES_DIR = 'notes_html/'

# Manually map subjects to filenames to avoid transformation issues
subject_to_filename = {
    'Mathematics I': 'maths1.html',
    'Physics I': 'physics1.html',
    'Mathematics II': 'maths2.html',
    'Data Structures': 'datastructures.html',
    'Database Management Systems': 'dbms.html',
    'Computer Networks': 'computernetworks.html',
    'Operating Systems': 'operatingsystems.html',
    'Software Engineering': 'softwareengineering.html',
    'Web Technologies': 'webtechnologies.html',
    'Compiler Design': 'compilerdesign.html',
    'Artificial Intelligence': 'ai.html',
    'Machine Learning': 'machinelearning.html',
    'Cloud Computing': 'cloudcomputing.html',
    # Add more subjects and corresponding filenames here
}

# Function to load HTML notes file using the mapping
def load_html_notes(subject):
    filename = subject_to_filename.get(subject)
    
    if not filename:
        return f"<p>Notes for {subject} not found. No mapping for this subject.</p>"
    
    notes_file = os.path.join(NOTES_DIR, filename)
    
    print(f"Looking for file: {notes_file}")  # Debugging line
    
    if os.path.exists(notes_file):
        with open(notes_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # Extract just the body content to avoid conflicts with the main template
            import re
            body_content = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
            if body_content:
                return body_content.group(1)
            return content
    else:
        return f"<p>Notes for {subject} not found. Tried to load: {notes_file}</p>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/branch/<branch_name>')
def branch(branch_name):
    # Special case for Basic Engineering - go directly to semester selection
    if branch_name == 'Basic Engineering':
        return render_template('year.html', branch=branch_name, year='1st Year')
    # For other branches, show the year selection page
    return render_template('branch.html', branch=branch_name)

@app.route('/year/<branch_name>/<year>')
def year(branch_name, year):
    return render_template('year.html', branch=branch_name, year=year)

@app.route('/subjects/<branch_name>/<year>/<semester>')
def subjects(branch_name, year, semester):
    # Get the subjects based on branch, year, and semester
    subjects = subjects_data[branch_name][year][semester]
    return render_template('subjects.html', branch=branch_name, year=year, semester=semester, subjects=subjects)

@app.route('/notes/<branch_name>/<year>/<semester>/<subject>')
def notes(branch_name, year, semester, subject):
    print(f"Fetching notes for subject: {subject}")  # Debugging line
    notes = load_html_notes(subject)
    return render_template('notes.html', branch=branch_name, year=year, semester=semester, subject=subject, notes=notes)

if __name__ == '__main__':
    print(f"Absolute path to notes directory: {os.path.abspath(NOTES_DIR)}")  # Debugging line
    app.run(debug=True)
