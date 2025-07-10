# Employee Management System (EMS)
#### Video Demo:  <https://youtu.be/Y6OfmuNx1nQ?si=ENllqTS7IPly_4BS>
#### Description:

The **Employee Management System (EMS)** is a comprehensive, menu-driven Python application integrated with a MySQL database, designed to manage various operations within an organization for both employees and managers. This system supports core functionalities such as secure login, profile management, password changes, project assignments, and request handling between employees and managers. The goal of EMS is to simulate a real-world human resource management system that enhances employee–manager communication and task coordination in a secure and organized way.

---

### 📁 Project Structure:

- **EMS.py**  
  The main driver file of the project. It connects to the MySQL database and launches the EMS menu with options for manager and employee login. Once authenticated, users are directed to role-specific menus. All feature integration (CRUD operations, viewing profiles, updating details, etc.) is done through this script.

- **Database.py**  
  Handles MySQL database connection logic using the `mysql.connector` module. It provides a reusable function `connectDB()` that returns both the connection and the cursor object used throughout the program.

- **Employee.py**  
  Contains the `Employee` class which manages:
    - Employee login and authentication
    - Viewing and editing employee profile
    - Changing passwords
    - Viewing assigned projects
    - Sending requests to the manager

- **Manager.py**  
  Contains the `Manager` class which manages:
    - Manager login and authentication
    - Performing CRUD operations on employees (Add, View, Update, Delete)
    - Viewing employee details
    - Assigning projects to employees
    - Viewing and responding to employee requests

- **test_project.py**  
  Contains unit tests for core functionality using `pytest`. Ensures that login, data integrity, and input validation mechanisms work as expected. Helps in maintaining system reliability.

---

### ⚙️ Technologies Used:

- **Python 3.13+**
- **MySQL** (for data storage and manipulation)
- **MySQL Connector/Python**
- **pytest** (for testing)
- **termcolor** (for colored console outputs)
- **os** and **getpass** for OS-level functionalities and secure input handling

---

### ✅ Key Features:

- **Role-Based Login System**: Separate logins for employees and managers with validation.
- **Secure Password Input**: Passwords are handled securely using `getpass` to prevent on-screen echoing.
- **CRUD Operations for Managers**: Managers can manage employees, assign projects, and monitor employee information and requests.
- **Profile Management for Employees**: Employees can view their own profile, update personal details, and see project assignments.
- **Request Management**: Employees can raise requests (e.g., leave requests, updates) that managers can review and respond to.
- **Persistent Data Storage**: All data is stored and managed in a MySQL relational database, ensuring consistency across sessions.

---

### 🎯 Design Decisions:

- **Modular Structure**: The system is designed in a modular fashion (separate Python files for each role and for DB) to improve readability and maintainability.
- **Database Security**: Input values are properly sanitized, and parameterized queries are used to avoid SQL injection vulnerabilities.
- **User Experience**: A clean, color-coded terminal interface with emoji markers is used to enhance the user experience.
- **Main Guard (`if __name__ == "__main__"`)**: Ensures that the main menu doesn’t auto-run during test execution or imports, preventing unwanted prompts during testing.
- **Testing Strategy**: `pytest` is used for unit testing, and the project is designed to be testable by abstracting inputs where needed.

---

### 📌 How to Run the Project:

1. Ensure MySQL is installed and running.
2. Create and configure the database with required tables (`employees`, `managers`, `projects`, `requests`).
3. Install the required Python packages:
   ```bash
   pip install mysql-connector-python termcolor pytest
