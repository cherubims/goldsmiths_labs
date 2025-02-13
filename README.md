
# 🚀 Goldsmiths Labs - E-Learning Platform

Goldsmiths Labs is a clean and modern, feature-rich e-learning platform designed to facilitate seamless interaction between students and teachers. It provides a structured environment for course management, real-time communication, progress tracking, and notifications, ensuring a smooth and engaging learning experience.

----------

## 📌 Features

### 1. User Authentication & Roles

-   Custom user authentication with **Students** and **Teachers** roles.
-   Secure login and registration system.
-   Profile management with profile picture upload.

### 2. Course Management

-   Teachers can create and manage courses.
-   Students can enroll in available courses.
-   Course materials can be uploaded as PDFs, videos, or documents.
-   Course completion tracking.

### 3. Announcements & Feedback

-   Teachers can post announcements for their students.
-   Students can leave feedback on courses.
-   Teachers can view feedback left by students.

### 4. Notifications System

-   Automated notifications for teachers when students enroll.
-   Notifications for students when new materials are uploaded.
-   Teachers are notified when students complete courses.
-   Mark notifications as read functionality.

### 5. Real-Time Chat

-   In-app chat system for student-teacher communication.
-   Users can search for specific students/teachers in the chat feature.
-   Supports real-time messaging with WebSockets.

### 6. Student Progress Tracking

-   Students can track their course progress.
-   Teachers can monitor student completion rates.
-   Progress bars for visual representation.

### 7. Basic but Decent Inbuilt Search Capabilities

-   Teachers can **search for students** within the feedback section.
-   The **chat feature** also includes an inbuilt search to find users quickly.
-   Searchable announcements for teachers and students.

### 8. API with Swagger Docs

-   RESTful API endpoints for external integrations.
-   Fully documented API using Swagger.
-   Secure authentication with Token-based authentication.

### 9. Admin Panel

-   Custom **modern and elegant** admin login panel for managing users, courses, and materials.
-   Secure authentication for admin users.

##  🛠️ **Main Technologies Used**

-  **Django** - Web Framework

-  **Django REST Framework (DRF)** - API Development

-  **Django Channels** - Real-time WebSockets

-  **SQLite3** - Database

-  **Bootstrap 5** - Frontend Styling

-  **WebSockets & RabbitMQ** - Real-time Communication

----------

## 🛠 Installation & Setup

### Prerequisites

Ensure you have the following installed:

-   Python 3+
-   Django 4.2+
-   RabbitMQ (for WebSockets & Notifications)
-   SQLite3


### 🔹 Clone the Repository

```sh
git clone https://github.com/yourusername/goldsmiths-labs.git
cd goldsmiths-labs

```

### 🔹 Create a Virtual Environment

```sh
python -m venv goldsmithsenv
source goldsmithsenv/bin/activate  # macOS/Linux
# OR
goldsmithsenv\Scripts\activate  # Windows

```

### 🔹 Install Dependencies

```sh
pip install -r requirements.txt

```

### 🔹 Apply Migrations & Run Server

```sh
python manage.py migrate
python manage.py runserver

```

### 🔹 Create Superuser (for Admin Access)

```sh
python manage.py createsuperuser

```

----------

## 📈 Top 6 Future Improvements (Full list in documented report)

1.  **Advanced Search:** Implement AI-powered search with fuzzy matching.
2.  **Gamification:** Reward students with badges for course completion.
3.  **Live Video Lectures:** Integrated video conferencing for live classes.
4.  **Mobile App Support:** Develop a mobile-friendly version using React Native.
5.  **More API Integrations:** Extend API capabilities for third-party tools.
6.  **Dark Mode:** Implement a full-fledged light/dark mode toggle.

----------

##  💡 **Contributing**

Contributions are welcome! If you’d like to contribute:

1.  **Fork** the repository.

2. Create a new **branch**.

3.  **Make your changes** and **commit**.

4.  **Push** to your fork and submit a **Pull Request**.

----------

## 📜 License

This project is open-source and licensed under the MIT License.

🎉 **Happy Learning with Goldsmiths Labs!** 🚀