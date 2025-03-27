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

### Beginner Setup Guide (Windows + VS Code)
1. **Install MySQL** from [here](https://dev.mysql.com/downloads/installer/).
2. **Open MySQL Command Line Client**.
3. **Create the database**:
   ```sql
   CREATE DATABASE your_database_name;
   ```
4. **Select the database**:
   ```sql
   USE your_database_name;
   ```
5. **Import the database schema**:
   ```sql
   SOURCE C:/path/to/mark_system.sql;
   ```
   _(Example: `SOURCE C:/Users/YourName/Desktop/mark_system.sql;`)_
6. **Open the project folder in VS Code**.
7. **Open the terminal in VS Code**.
8. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
9. **Run the application**:
   ```sh
   python3 app.py
   ```

## Usage

## Screenshots
Here are some previews of the system:

![Login Page](screenshots/LOGIN PAGE.png)
![Student First Login Password Reset](screenshots/STUDENT FIRST LOGIN PASSWORD RESET.png)
![Student Dashboard](screenshots/STUDENT DASHBOARD.png)
![Teacher Dashboard](screenshots/TEACHER DASHBOARD.png)
![Student Details](screenshots/STUDENT DETAILS.png)
![Example Data - Student Details](screenshots/EXAMPLE DATA (STUDENT DETAILS).png)
![Add Subject and Marks](screenshots/ADD SUBJECT AND MARKS.png)
![Example Data - Add Subject and Marks](screenshots/EXAMPLE DATA (ADD SUBJECT AND MARKS).png)

- **Login Page**  
  ![Login Page](screenshots/LOGIN%20PAGE.png)

- **Teacher Dashboard**  
  ![Teacher Dashboard](screenshots/TEACHER%20DASHBOARD.png)

- **Student Dashboard**  
  ![Student Dashboard](screenshots/STUDENT%20DASHBOARD.png)

- **Student First Login (Password Reset)**  
  ![Student First Login](screenshots/STUDENT%20FIRST%20LOGIN%20PASSWORD%20RESET.png)

- **Student Details**  
  ![Student Details](screenshots/STUDENT%20DETAILS.png)

- **Add Subject and Marks**  
  ![Add Subject and Marks](screenshots/ADD%20SUBJECT%20AND%20MARKS.png)

- **Example Data (Add Subject and Marks)**  
  ![Example Data](screenshots/SAMPLE%20DETAILS%20(ADD%20SUBJECT%20AND%20MARKS).png)

- **Example Data (Student Details)**  
  ![Example Data](screenshots/SAMPLE%20DETAILS%20(STUDENT%20DETAILS).png)

1. **Run the Application**
   ```sh
   python app.py
   ```
2. Open `http://127.0.0.1:5000/` in your browser.

## License
This project is for educational purposes. Modify as needed!

