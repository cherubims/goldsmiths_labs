from courses_app.models import Course
from auth_app.models import CustomUser

# Get the teacher user
teacher = CustomUser.objects.filter(is_teacher=True).first()

# Create sample courses
uol_courses = [
    {"name": "Mobile Development", "description": "Learn to build mobile apps with React Native and Flutter."},
    {"name": "Advanced Web Development", "description": "Master web development with Django, React, and modern web technologies."},
    {"name": "Artificial Intelligence", "description": "Explore foundational concepts of AI, including search algorithms and game theory."},
    {"name": "Machine Learning", "description": "Learn supervised and unsupervised machine learning techniques with Python."},
    {"name": "Natural Language Processing", "description": "Understand text processing, sentiment analysis, and machine translation."},
    {"name": "Fundamentals of Computer Science", "description": "Core principles of computer science, including data structures and algorithms."},
    {"name": "Programming with Data", "description": "Analyze and visualize data using Python and libraries like Pandas and Matplotlib."},
    {"name": "Object-Oriented Programming", "description": "Deep dive into OOP concepts and design patterns using Java or Python."},
    {"name": "Discrete Mathematics", "description": "Learn set theory, graph theory, and combinatorics for computer science."},
    {"name": "Software Engineering", "description": "Explore software development lifecycle models, agile practices, and testing."},
    {"name": "Cybersecurity", "description": "Understand security principles, cryptography, and penetration testing."},
    {"name": "Human-Computer Interaction", "description": "Study user interface design, usability testing, and accessibility principles."},
    {"name": "Virtual Reality and Augmented Reality", "description": "Learn to create VR and AR experiences with Unity or Unreal Engine."},
    {"name": "Game Development", "description": "Design and develop games using game engines and programming principles."},
    {"name": "Data Science", "description": "Explore statistical techniques and data manipulation for insights and predictions."},
]

for course in uol_courses:
    Course.objects.create(name=course["name"], description=course["description"], teacher=teacher)

print("UoL courses added successfully!")
