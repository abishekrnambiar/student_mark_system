# Student Mark System

A web-based mark adding system for teachers and a mark viewing system for students using Flask and MySQL.

## Features
- Teachers can add student marks.
- Students can view their marks.
- Teachers can create new student logins.
- A student's **first name** will be their **username**.
- Default password is set by the system.
- On first login, students must reset their password.
- After resetting, they are instantly logged out to ensure security.
- MySQL database integration.
- Flask-based web interface.

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.x
- MySQL Server
- pip (Python package manager)

### Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/abishekrnambiar/student_mark_system.git
   cd student_mark_system
   ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up the Database**
   - Import `mark_system.sql` into MySQL:
     ```sh
     mysql -u root -p < mark_system.sql
     ```
   - **Modify Database Credentials:**
     - Open `app.py` and update the database name and password:
       ```python
       database="your_database_name"
       password="your_password"
       ```
     - Replace `your_database_name` and `your_password` with your actual MySQL credentials.

## Usage
1. **Run the Application**
   ```sh
   python app.py
   ```
2. Open `http://127.0.0.1:5000/` in your browser.

## License
This project is for educational purposes. Modify as needed!

