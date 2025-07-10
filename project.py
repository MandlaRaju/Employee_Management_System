import sys
from db_connection import Database
import textwrap
import re 

#-----------------------------------------------------------------------------#
###                              MANAGER                                    ###
#-----------------------------------------------------------------------------#

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

#Safe input with exit support
def safe_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == "exit":
        print(colored(" Exiting the program...!", "1;31"))
        print(colored("     🌟 Thank you for using EMS! 🌟", "1;33"))
        print(colored("╔══════════════════════════════════════╗", "1;33"))
        print(colored("║   👋 You have successfully exited.   ║", "1;33"))
        print(colored("║    Have a productive day ahead!      ║", "1;33"))
        print(colored("╚══════════════════════════════════════╝\n", "1;33"))
        sys.exit()
    return user_input

class Manager:

        @staticmethod
        def Login(connection, cursor, email, password):
            try:
                query = "SELECT * FROM manager WHERE email = %s AND password = %s"
                cursor.execute(query, (email, password))
                manager = cursor.fetchone()
                if manager:
                    print(colored("Login Successfull✅","1;32"))
                    return True
                else:
                    print(colored("Invalid email or password.","1;31"))
                    return False
            except Exception as e:
                print(colored(f"Error during login: {e}","1;31"))
                return False
            

        @staticmethod
        def add_manager(cursor, connection):
            manager_email = "raju587836@gmail.com"
            manager_pswd = "Xyz1432@"
            try:
                cursor.execute("SELECT * FROM manager WHERE email = %s", (manager_email,))
                if cursor.fetchone():
                    print("Manager already exists!")
                    return

                query = """
                INSERT INTO manager(email, password)
                VALUES (%s, %s)
                """
                cursor.execute(query, (manager_email, manager_pswd))
                connection.commit()
                print("Manager Added Successfully!")
            except Exception as e:
                print("Error While Adding Manager:", e)


            
        @staticmethod
        def createEmp(connection, cursor):
            print("\033[1;33m╔" + "═" * 33 + "╗\033[0m")
            print("\033[1;33m║       Creating a Employee       ║\033[0m")
            print("\033[1;33m╚" + "═" * 33 + "╝\033[0m")
            name = safe_input(colored("Enter Employee Name: ","1;32").strip())
            email = safe_input(colored("Enter Employee E-mail: ","1;32").strip())
            password = safe_input(colored("Enter Employee Password: ","1;32").strip())
            role = safe_input(colored("Enter Employee Role: ","1;32").strip())
            salary = safe_input(colored("Enter Employee Salary: ","1;32").strip())
            phoneNo = safe_input(colored("Enter Employee PhoneNo: ","1;32").strip())

            try:
                query = """
                INSERT INTO employee (name, email, password, role, salary, phone_no)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (name, email, password, role, salary, phoneNo)
                cursor.execute(query, values)
                connection.commit()
                print(colored(f" Employee {name} added successfully!✅","1;32"))

            except Exception as e:
                print(colored(f"Error while adding employee: {e}","1;31"))

        @staticmethod
        def viewEM(connection, cursor):
            try:
                emp_id = safe_input("\033[1;32mEnter Your Employee ID: \033[0m")  

                cursor.execute("SELECT * FROM employee WHERE id = %s", (emp_id,))
                employee = cursor.fetchone()

                if employee:
                    width = 50
                    # Box top
                    print("\033[1;35m╔" + "═" * width + "╗\033[0m")
                    # Title row
                    title = " Employee Details "
                    print("\033[1;36m║" + title.center(width) + "║\033[0m")
                    # Separator
                    print("\033[1;35m╠" + "═" * width + "╣\033[0m")

                    # Details rows
                    print("\033[1;35m║ {:<12}: {:<35}║\033[0m".format("ID", employee[0]))
                    print("\033[1;35m║ {:<12}: {:<35}║\033[0m".format("Name", employee[1]))
                    print("\033[1;35m║ {:<12}: {:<35}║\033[0m".format("Email", employee[2]))
                    print("\033[1;35m║ {:<12}: {:<35}║\033[0m".format("Role", employee[4]))
                    print("\033[1;35m║ {:<12}: {:<35}║\033[0m".format("Salary", employee[5]))
                    print("\033[1;35m║ {:<12}: {:<35}║\033[0m".format("PhoneNo", employee[6]))

                    # Box bottom
                    print("\033[1;35m╚" + "═" * width + "╝\033[0m")
                    input(colored("Press any key to return dashboard...","1;33"))
                else:
                    input("\033[1;31mNo employee found with the given ID.\nPress any key to return DASH BOARD...\033[0m")  # Red text

            except Exception as e:
                print("\033[1;31mError fetching employee data:\033[0m", e)  # Red text


        @staticmethod
        def setProject(cursor, connection):
            print("\033[1;33m╔" + "═" * 35 + "╗\033[0m")
            print("\033[1;33m║  Assigning A Project To Employee  ║\033[0m")
            print("\033[1;33m╚" + "═" * 35 + "╝\033[0m")
            
            employee_id = safe_input(colored("Enter Employee ID To Assign Project: ","1;32").strip())
            project_name = safe_input(colored("Enter Project Name: ","1;32").strip())
            deadline = safe_input(colored("Enter Project Deadline(YYYY-MM-DD): ","1;32").strip())
            client = safe_input(colored("Enter Client Name: ","1;32").strip())

            try:
                query = """
                INSERT INTO project(employee_id, project_name, deadline,client_name)
                VALUES(%s, %s, %s, %s)
                """
                values = (employee_id, project_name, deadline, client)
                cursor.execute(query, values)
                connection.commit()
                print(colored("Project and Deadline assigned successfully✅","1;32"))

            except Exception as e:
                print(colored(f"Error while assigning Project: {e}","1;31"))



        @staticmethod
        def req(connection, cursor):
            try:
                print("\033[1;35m╔" + "═" * 45 + "╗\033[0m")
                print("\033[1;36m║{:^45}║\033[0m".format("Pending Requests"))
                print("\033[1;35m╠" + "═" * 45 + "╣\033[0m")
                
                # Fetch pending requests
                cursor.execute("""
                    SELECT r.request_id, e.name, r.request_type, r.description, r.status 
                    FROM request r 
                    JOIN employee e ON r.employee_id = e.id 
                    WHERE r.status = 'Pending'
                """)
                requests = cursor.fetchall()

                # Check if there are no pending requests
                if not requests:
                    print(colored("║           No pending requests found.        ║", "1;31"))
                    print("\033[1;35m╚" + "═" * 45 + "╝\033[0m")
                    input(colored("Press any key to return dash board...", "1;33"))
                    return

                # Display pending requests

                for req in requests:
                    print("\033[1;35m║ Request ID   : {:<28} ║\033[0m".format(req[0]))
                    print("\033[1;35m║ Employee Name: {:<28} ║\033[0m".format(req[1]))
                    print("\033[1;35m║ Request Type : {:<28} ║\033[0m".format(req[2]))

                    # Break description into multiple lines if it's too long
                    description = req[3]
                    wrapped_lines = textwrap.wrap(description, width=28)

                    if len(wrapped_lines) > 0:
                        # Print the first line with the label
                        print("\033[1;35m║ Description  : {:<28} ║\033[0m".format(wrapped_lines[0]))

                        # Print remaining lines with spaces instead of label
                        for line in wrapped_lines[1:]:
                            print("\033[1;35m║                {:<28} ║\033[0m".format(line))
                    else:
                        # If no description, leave it blank
                        print("\033[1;35m║ Description  : {:<28} ║\033[0m".format(""))

                    print("\033[1;35m║ Status       : {:<28} ║\033[0m".format(req[4]))
                    print("\033[1;35m╚" + "═" * 45 + "╝\033[0m")


                # Approve/Reject Requests
                while True:
                    choice = safe_input(colored("\nEnter request ID to Approve/Reject (or 0 to go back): ", "1;32"))
                    if not choice.isdigit():
                        print(colored("Please enter a valid number.", "1;31"))
                        continue

                    choice = int(choice)
                    if choice == 0:
                        return

                    # Check if the request exists and is still pending
                    cursor.execute(
                        "SELECT * FROM request WHERE request_id = %s AND status = 'Pending'",
                        (choice,)
                    )
                    request = cursor.fetchone()

                    # If the request exists, approve or reject it
                    if not request:
                        print(colored("Invalid or already processed request ID.", "1;31"))
                        input(colored("[ Press any key to return to the Dashboard...]", "1;32"))
                        break  # Break out to return to dashboard or menu

                    # If request exists, ask for action
                    action = safe_input(colored("Enter 'A' to Approve or 'R' to Reject: ", "1;32")).strip().upper()

                    if action == 'A':
                        cursor.execute(
                            "UPDATE request SET status = 'Approved' WHERE request_id = %s",
                            (choice,)
                        )
                        connection.commit()
                        print(colored("Request Approved ✅", "1;32"))
                        break

                    elif action == 'R':
                        cursor.execute(
                            "UPDATE request SET status = 'Rejected' WHERE request_id = %s",
                            (choice,)
                        )
                        connection.commit()
                        print(colored("Request Rejected ❌", "1;31"))
                        break

                    else:
                        print(colored("Invalid action. Try again!", "1;31"))

            except Exception as e:
                print(colored(f"Error handling requests: {str(e)}", "1;31"))



        @staticmethod
        def deleteEmp(connection, cursor):
            print(colored("╔════════════════════════════════════════╗", "1;32"))
            print(colored("║         🗑️  Deleting an Employee!       ║", "1;36"))
            print(colored("╚════════════════════════════════════════╝", "1;32"))

            employee_id = safe_input(colored("Enter Employee ID To Delete: ","1;32").strip())

            try:
                confirm = safe_input(colored(f"Are you sure you want to delete employee ID {employee_id}? (y/n): ","1;33").strip())
                if confirm.lower() != 'y':
                    print(colored("Deletion cancelled.","1;31"))
                    return
                query = "DELETE FROM employee WHERE id = %s" 
                cursor.execute(query, (employee_id,))
                connection.commit()

                if cursor.rowcount > 0:
                    print(colored("Employee Deleted Successfully!✅","1;32"))
                else:
                    input(colored("No Employee Found With This ID! Press any key to return DASH BOARD...","1;31"))

            except Exception as e:
                print(colored(f"Error While Deleting Employee: {e}", "1;31"))


        @staticmethod
        def allEmp(connection, cursor):
            try:
                query = """
                SELECT e.id, e.name, e.role, e.salary, e.phone_no, p.project_name
                FROM employee e
                LEFT JOIN project p ON e.id = p.employee_id
                """
                cursor.execute(query)
                employees = cursor.fetchall()

                # Dictionary to track employees and their projects
                if not employees:
                    input(colored("No Employees Found! Press any key to return DASH BOARD...", "1;31"))
                    return

                print("\033[1;35m╔════════════════════════════════════════════════════════════════╗\033[0m")
                print("\033[1;36m║                  👥  All Employees List                        ║\033[0m")
                print("\033[1;35m╠════════════════════════════════════════════════════════════════╣\033[0m")

                for emp in employees:
                    print("\033[1;35m║ {:<15}: {:<46}║\033[0m".format("Employee ID", emp[0]))
                    print("\033[1;35m║ {:<15}: {:<46}║\033[0m".format("Name", emp[1]))
                    print("\033[1;35m║ {:<15}: {:<46}║\033[0m".format("Role", emp[2]))
                    print("\033[1;35m║ {:<15}: {:<46}║\033[0m".format("Salary", f"{int(emp[3]):,}"))
                    print("\033[1;35m║ {:<15}: {:<46}║\033[0m".format("Phone No", emp[4]))
                    print("\033[1;35m║ {:<15}: {:<46}║\033[0m".format("Project", emp[5] if emp[5] else "None"))
                    print("\033[1;35m╚════════════════════════════════════════════════════════════════╝\033[0m")

                input(colored("Press any key to return to dashboard...", "1;33"))


            except Exception as e:
                print(colored("Error while fetching employees:", "1;31"), e)


        @staticmethod
        def editEM(connection, cursor):
            try:
                emp_id = input(colored("Enter Employee ID to edit (or type 'exit' to go back): ", "1;32")).strip()
                if emp_id.lower() == 'exit':
                    return

                # Fetch employee details including phone_no
                cursor.execute("SELECT id, name, email, role, salary, phone_no FROM employee WHERE id = %s", (emp_id,))
                employee = cursor.fetchone()

                if not employee:
                    print(colored("Employee not found!", "1;31"))
                    return

                # Display current details
                print(colored("\n╔" + "═" * 96 + "╗", "1;35"))
                print(colored("║{:^95}║".format("📋 Employee Current Details"), "1;36"))
                print(colored("╠" + "═" * 4 + "╦" + "═" * 17 + "╦" + "═" * 27 + "╦" + "═" * 16 + "╦" + "═" * 13 + "╦" + "═" * 14 + "╣", "1;35"))
                print(colored("║ {:<2} ║ {:<15} ║ {:<25} ║ {:<14} ║ {:>11} ║ {:<12} ║".format("ID", "Name", "Email", "Role", "Salary", "Phone No"), "1;30"))
                print(colored("╠" + "═" * 4 + "╬" + "═" * 17 + "╬" + "═" * 27 + "╬" + "═" * 16 + "╬" + "═" * 13 + "╬" + "═" * 14 + "╣", "1;35"))
                print(colored("║ {:<2} ║ {:<15} ║ {:<25} ║ {:<14} ║ ₹{:>10,.2f} ║ {:<12} ║".format(employee[0], employee[1], employee[2], employee[3], employee[4], employee[5] if employee[5] else "N/A"), "1;35"))
                print(colored("╚" + "═" * 4 + "╩" + "═" * 17 + "╩" + "═" * 27 + "╩" + "═" * 16 + "╩" + "═" * 13 + "╩" + "═" * 14 + "╝", "1;35"))
                input(colored("Press any key to start editing", "1;33"))

                # Edit options
                print(colored("╔" + "═" * 34 + "╗", "1;35"))
                print(colored("║{:^35}║".format("✏️  What do you want to edit?"), "1;36"))
                print(colored("╠" + "═" * 34 + "╣", "1;35"))
                print(colored("║ 1. Name                          ║", "1;35"))
                print(colored("║ 2. Email                         ║", "1;35"))
                print(colored("║ 3. Role                          ║", "1;35"))
                print(colored("║ 4. Salary                        ║", "1;35"))
                print(colored("║ 5. Phone Number                  ║", "1;35"))
                print(colored("║ 6. Cancel                        ║", "1;31"))
                print(colored("╚" + "═" * 34 + "╝", "1;35"))

                choice = safe_input(colored("Enter your choice (1–6): ", "1;32")).strip()

                if choice == '1':
                    new_name = safe_input(colored("Enter new name: ", "1;32")).strip()
                    cursor.execute("UPDATE employee SET name = %s WHERE id = %s", (new_name, emp_id))

                elif choice == '2':
                    new_email = safe_input(colored("Enter new email: ", "1;32")).strip()
                    cursor.execute("UPDATE employee SET email = %s WHERE id = %s", (new_email, emp_id))

                elif choice == '3':
                    new_role = safe_input(colored("Enter new role: ", "1;32")).strip()
                    cursor.execute("UPDATE employee SET role = %s WHERE id = %s", (new_role, emp_id))

                elif choice == '4':
                    try:
                        new_salary = float(safe_input(colored("Enter new salary: ", "1;32")))
                        cursor.execute("UPDATE employee SET salary = %s WHERE id = %s", (new_salary, emp_id))
                    except ValueError:
                        print(colored("Invalid salary input! Must be a number.", "1;31"))
                        return

                elif choice == '5':
                    new_phone = safe_input(colored("Enter new phone number: ", "1;32")).strip()
                    cursor.execute("UPDATE employee SET phone_no = %s WHERE id = %s", (new_phone, emp_id))

                elif choice == '6':
                    print(colored("Edit cancelled.", "1;31"))
                    return

                else:
                    print(colored("Invalid choice. Try again.", "1;31"))
                    return

                connection.commit()
                print(colored("Employee details updated successfully ✅", "1;32"))

            except Exception as e:
                print(colored(f"Error editing employee: {e}", "1;31"))


        @staticmethod
        def changePswd(cursor, connection):
            print(colored("╔" + "═" * 39 + "╗", "1;35"))
            print(colored("║{:^38}║".format("🔐 Changing Manager Password!"), "1;36"))
            print(colored("╚" + "═" * 39 + "╝", "1;35"))
            
            current_pswd = safe_input(colored("Enter Current Password: ","1;32").strip())
            new_pswd = safe_input(colored("The Password Should Be 8 Characters and In Between [0-9],[A-Z],[a-z] and [_@$]: ","1;32").strip())
            if not re.match(r'^[A-Za-z0-9_@$]{8,}$', new_pswd):
                print(colored("Invalid Password Format! Must be 8+ characters using A-Z, a-z, 0-9, and _@$","1;31"))
                return
            try:
                cursor.execute("SELECT * FROM manager WHERE password = %s", (current_pswd,))
                manager = cursor.fetchone()

                if manager:
                    cursor.execute("UPDATE manager SET password = %s WHERE password = %s", (new_pswd, current_pswd))
                    connection.commit()
                    print(colored("Password Changed Successfully!✅","1;32"))
                else:
                    print(colored("Current Password Is Incorrect!","1;31"))
            except Exception as e:
                print(colored("Error While Changing Password: ","1;31", e))

        @staticmethod
        def logout():
            print(colored("Manager Logged Out Successfully!","1;32"))
            return True


#-----------------------------------------------------------------------------#
###                             EMPLOYEE                                    ###
#-----------------------------------------------------------------------------#

def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

def safe_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == "exit":
        print(colored("Exiting The Program!!","1;31"))
        sys.exit()
    return user_input

class Employee:

        @staticmethod
        def EMlogin(connection, cursor, email, password):
            try:
                cursor.execute("SELECT * FROM employee WHERE email = %s AND password = %s",(email, password))
                employee = cursor.fetchone()

                if employee:
                    print(colored("Login Successfull✅","1;32"))
                    return True
                else:
                    print(colored("Invalid Credentials❌","1;31"))
                    return False
                
            except Exception as e:
                print(colored("Error during login: ","1;31",e))
                return False
            

        @staticmethod
        def reqM(connection, cursor, emp_email):
            print(colored("╔" + "═" * 39 + "╗", "1;35"))
            print(colored("║{:^38}║".format("📨 Request to Manager Menu"), "1;36"))
            print(colored("╠" + "═" * 39 + "╣", "1;35"))
            print(colored("║ 1️⃣  Send a new request                 ║", "1;35"))
            print(colored("║ 2️⃣  View my previous requests          ║", "1;35"))
            print(colored("║ 3️⃣  Cancel my previous requests        ║", "1;35"))
            print(colored("║ 4️⃣  Exit                               ║", "1;31"))
            print(colored("╚" + "═" * 39 + "╝", "1;35"))

            choice = safe_input(colored("Enter your choice: ", "1;32"))

            cursor.execute("SELECT id FROM employee WHERE email = %s", (emp_email,))
            result = cursor.fetchone()
            if not result:
                print(colored("Employee not found!", "1;31"))
                return
            emp_id = result[0]

            if choice == '1':
                subject = safe_input(colored("Enter request subject: ", "1;32"))
                message = safe_input(colored("Enter request message: ", "1;32"))

                try:
                    cursor.execute(
                        "INSERT INTO request (employee_id, request_type, description, status) VALUES (%s, %s, %s, %s)",
                        (emp_id, subject, message, 'Pending')
                    )
                    connection.commit()
                    print(colored("Request sent successfully ✅", "1;32"))
                    input(colored("Press any key to return to dashboard...", "1;33"))
                except Exception as e:
                    print(colored(f"Error while sending request: {e}", "1;31"))

            elif choice == '2':
                try:
                    cursor.execute(
                        "SELECT request_type, description, status FROM request WHERE employee_id = %s",
                        (emp_id,)
                    )
                    rows = cursor.fetchall()
                    if rows:
                        box_width = 37
                        inner_width = box_width - 11  # adjust for '║ Message : '

                        print(colored("╔" + "═" * box_width + "╗", "1;35"))
                        print(colored("║{:^36}║".format("📋 Your Requests"), "1;34"))
                        print(colored("╠" + "═" * box_width + "╣", "1;35"))
                        for i, row in enumerate(rows, start=1):
                            wrapped_msg = textwrap.wrap(row[1], width=inner_width)

                            print(colored("║ Request #{}{:>26}║".format(i, ""), "1;36"))
                            print(colored("║ Subject : {:<26}║".format(row[0]), "1;36"))
                            print(colored("║ Message : {:<26}║".format(wrapped_msg[0]), "1;36"))

                            for line in wrapped_msg[1:]:
                                print(colored("║           {:<26}║".format(line), "1;36"))

                            print(colored("║ Status  : {:<26}║".format(row[2]), "1;36"))

                            if i != len(rows):
                                print(colored("╠" + "═" * box_width + "╣", "1;35"))

                        print(colored("╚" + "═" * box_width + "╝", "1;35"))
                        input(colored("Press any key to return to dashboard...", "1;33"))
                    else:
                        print(colored("      No previous requests found.", "1;31"))
                        input(colored("Press any key to return dashboard...", "1;33"))

                except Exception as e:
                    print(colored(f"Error while fetching requests: {e}", "1;31"))

            elif choice == '3':
                try:
                    cursor.execute("SELECT request_id, request_type, description FROM request WHERE employee_id = %s AND status = 'Pending'", (emp_id,))
                    rows = cursor.fetchall()

                    if not rows:
                        print(colored("No pending requests found to cancel.", "1;33"))
                        input(colored("Press any key to return to dashboard...", "1;33"))
                        return

                    print(colored("╔═════════════════════════════════════╗", "1;35"))
                    print(colored("║       📋 Your Pending Requests      ║", "1;36"))
                    print(colored("╠═════════════════════════════════════╣", "1;35"))

                    for i, row in enumerate(rows, start=1):
                        print(colored(f"║ Request #{i:<27}║", "1;36"))
                        print(colored(f"║ Request ID : {row[0]:<23}║", "1;36"))
                        print(colored(f"║ Subject    : {row[1]:<23}║", "1;36"))
                        message_lines = textwrap.wrap(row[2], width=20)

                        if message_lines:
                            print(f"\033[1;36m║ Description  : {message_lines[0]:<21} ║\033[0m")

                            for line in message_lines[1:]:
                                print(f"\033[1;36m║               {line:<21} ║\033[0m")
                        else:
                            print(colored(f"║ Description    : {row[2]:<21}║", "1;36"))

                        if i != len(rows):
                            print(colored("╠═════════════════════════════════════╣", "1;35"))

                    print(colored("╚═════════════════════════════════════╝", "1;35"))

                    req_id = safe_input(colored("Enter the Request ID you want to cancel: ", "1;32"))
                    cursor.execute("DELETE FROM request WHERE request_id = %s AND employee_id = %s AND status = 'Pending'", (req_id, emp_id))
                    connection.commit()

                    if cursor.rowcount > 0:
                        print(colored("Request canceled successfully ✅", "1;32"))
                    else:
                        print(colored("Invalid Request ID or request already processed!", "1;31"))
                    input(colored("Press any key to return to dashboard...", "1;33"))

                except Exception as e:
                    print(colored(f"Error while canceling request: {e}", "1;31"))

            elif choice == '4':
                print(colored("Exiting Request Menu.", "1;31"))
                return

            else:
                print(colored("Invalid choice. Try again!", "1;31"))




        @staticmethod
        def viewProjectDetails(connection, cursor):
            try:
                emp_id = input(colored("Enter your employee ID view assigned project: ", "1;32"))
                cursor.execute("SELECT id, project_name, deadline, client_name FROM project WHERE employee_id = %s",(emp_id,))
                rows = cursor.fetchall()

                if not rows:
                    print(colored("No project records found.", "1;33"))
                else:
                    print(colored("╔════════════════════════════════════╗", "1;35"))
                    print(colored("║       📁 Project Details Menu      ║", "1;36"))
                    print(colored("╠════════════════════════════════════╣", "1;35"))
                
                    for i, row in enumerate(rows, start = 1): 
                        print(colored(f"║ Project #{i:<26}║", "1;36"))
                        print(colored(f"║ Project ID   : {str(row[0]):<20}║", "1;36"))
                        print(colored(f"║ Project Name : {str(row[1]):<20}║", "1;36"))
                        print(colored(f"║ Deadline     : {str(row[2]):<20}║", "1;36"))
                        print(colored(f"║ Client Name  : {str(row[3]):<20}║", "1;36"))
                        if i != len(rows):
                            print(colored("╠════════════════════════════════════╣", "1;35"))

                    print(colored("╚════════════════════════════════════╝", "1;35"))

                input(colored("Press any key to return to dashboard...", "1;33"))

            except Exception as e:
                print(colored(f"Error while fetching project details: {e}", "1;31"))



        @staticmethod
        def updatePD(cursor, connection, email):
            print(colored("╔═══════════════════════════════════╗", "1;35"))
            print(colored("║     Updating Personal Details     ║", "1;36"))
            print(colored("╠═══════════════════════════════════╣", "1;35"))
            print(colored("║ 1. Name                           ║", "1;35"))
            print(colored("║ 2. Email                          ║", "1;35"))
            print(colored("║ 3. Phone Number                   ║", "1;35"))
            print(colored("║ 4. Cancel                         ║", "1;31"))
            print(colored("╚═══════════════════════════════════╝", "1;35"))

            print()
            choice = safe_input(colored("Enter your choice: ", "1;32"))
            
            if choice == '1':
                new_name = safe_input(colored("Enter full name: ","1;32"))
                cursor.execute("UPDATE employee SET name = %s WHERE email = %s", (new_name,email))
                connection.commit()
                print(colored("Name changed successfully✅", "1;32"))

            elif choice == '2':
                new_mail = safe_input(colored("Enter new email: ", "1;32"))
                cursor.execute("UPDATE employee SET email = %s WHERE email = %s", (new_mail, email))
                connection.commit()
                print(colored("Email updated successfully✅", "1;32"))

            elif choice == '3':
                new_phone = safe_input(colored("Enter new number: ", "1;32"))
                cursor.execute("UPDATE employee SET phone_no = %s WHERE email = %s", (new_phone,email))
                connection.commit()
                print(colored("Phone number updated successfully✅", "1;32"))

            elif choice == '4':
                print(colored("Canceled❌", "1;31"))
                return
            
            else:
                print(colored("Inavlid choice. Try again!", "1;31"))



        @staticmethod
        def changePSWD(cursor, connection, email):
            print(colored("╔═════════════════════════════════════════╗", "1;35"))
            print(colored("║      Changing Employee Password!        ║", "1;36"))
            print(colored("╚═════════════════════════════════════════╝", "1;35"))

            current_pswd = safe_input(colored("Enter current password: ", "1;32"))
            cursor.execute("SELECT * FROM employee WHERE email = %s AND password = %s", (email,current_pswd))
            employee = cursor.fetchone()


            if not employee:
                print(colored("Current password is incorrect. Try again!", "1;31"))
                return
            print(colored("New Password Should Be 8 Characters and In Between [0-9],[A-Z],[a-z] and [_@$]: ", "1;32"))
            new_pswd = safe_input(colored("Enter new password: ", "1;32"))

            def strongpswd(pswd):
                return(
                    len(pswd) >= 8 and
                    re.search(r"[A-Z]",pswd) and
                    re.search(r"[a-z]",pswd) and
                    re.search(r"[0-9]",pswd) and
                    re.search(r"[_@$]",pswd) 
                )

            if not strongpswd(new_pswd):
                print(colored("Invalid password format! Must be 8+ characters including A-Z, a-z, 0-9, and special character (_@$).", "1;31"))
                return
            try:
                cursor.execute("UPDATE employee SET password = %s WHERE password = %s", (new_pswd, current_pswd))
                connection.commit()
                print(colored("Password changed successfully!✅", "1;32"))

            except Exception as e:
                print(colored(f"Error while changing password: {e}", "1;31"))

        @staticmethod
        def profile(connection, cursor,email):
            try:
                print(colored("╔══════════════════════════════════════════╗", "1;35"))
                print(colored("║              Employee Profile            ║", "1;36"))
                print(colored("╠══════════════════════════════════════════╣", "1;35"))

                cursor.execute("SELECT id, name, email, role, salary, phone_no FROM employee WHERE email = %s",(email,))
                rows = cursor.fetchall()

                if not rows:
                    print(colored("Employee Details not found.", "1;31"))
                    
                else:
                    for row in rows:
                        print(colored(f"║ Employee ID   : {str(row[0]):<25}║", "1;36"))
                        print(colored(f"║ Name          : {str(row[1]):<25}║", "1;36"))
                        print(colored(f"║ Email         : {str(row[2]):<25}║", "1;36"))
                        print(colored(f"║ Role          : {str(row[3]):<25}║", "1;36"))
                        print(colored(f"║ Salary        : {str(row[4]):<25}║", "1;36"))
                        print(colored(f"║ Phone         : {str(row[5]):<25}║", "1;36"))
                    print(colored("╚" + "═" * 42 + "╝", "1;35")) 
                    
                input(colored("Press any key to return dashboard...", "1;33"))

            except Exception as e:
                print(colored(f"Error While fetching employee details: {e}", "1;31"))   


        @staticmethod
        def logout():
            print(colored("Employee logged out successfully!","1;32"))
            return True
# Connect to database
db = Database()
connection, cursor = db.connect()

# Define color codes
def colored(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"

# Safe input with exit support
def safe_input(prompt):
    user_input = input(prompt).strip()
    if user_input.lower() == "exit":
        print(colored(" Exiting the program...!", "1;31"))
        print(colored("\n     🌟 Thank you for using EMS! 🌟", "1;33"))
        print(colored("╔══════════════════════════════════════╗", "1;33"))
        print(colored("║   👋 You have successfully exited.   ║", "1;33"))
        print(colored("║    Have a productive day ahead!      ║", "1;33"))
        print(colored("╚══════════════════════════════════════╝\n", "1;33"))
        sys.exit()
    return user_input

#-----------------------------------------------------------------------------#
###                               MAIN MENU                                 ###
#-----------------------------------------------------------------------------#

def main():
    while True:
        print(colored("╔══════════════════════════════════════════════╗", "1;35"))
        print(colored("║     👨‍💼 Employee Management System (EMS)    ║", "1;36"))
        print(colored("╠══════════════════════════════════════════════╣", "1;35"))
        print(colored("║ 1️⃣  Manager Login                             ║", "1;35"))
        print(colored("║ 2️⃣  Employee Login                            ║", "1;35"))
        print(colored("║ 3️⃣  Exit                                      ║", "1;31"))
        print(colored("╚══════════════════════════════════════════════╝", "1;35"))

        choice = safe_input(colored(" Enter Your Choice (1/2/3): ", "1;32"))

        if choice == '1':
            while True:
                email = safe_input(colored("📧 Enter Manager Email: ", "1;32"))
                password = safe_input(colored("🔒 Enter Password: ", "1;32"))

                if Manager.Login(connection, cursor, email, password):
                    while True:
                        print(colored("╔══════════════════════════════════════╗", "1;35"))
                        print(colored("║         🛠 Manager Dashboard          ║", "1;36"))
                        print(colored("╠══════════════════════════════════════╣", "1;35"))
                        print(colored("║ 1. ➕ Create New Employee            ║", "1;35"))
                        print(colored("║ 2. 🔍 View Employee                  ║", "1;35"))
                        print(colored("║ 3. 📅 Set Project & Deadline         ║", "1;35"))
                        print(colored("║ 4. ❌ Delete Employee                ║", "1;35"))
                        print(colored("║ 5. 📋 View All Employees             ║", "1;35"))
                        print(colored("║ 6. 🔐 Change Manager Password        ║", "1;35"))
                        print(colored("║ 7. ✏️ Edit Employee Details           ║", "1;35"))
                        print(colored("║ 8. 📨 View Employee Requests         ║", "1;35"))
                        print(colored("║ 9. 🚪 Logout                         ║", "1;31"))
                        print(colored("╚══════════════════════════════════════╝", "1;35"))

                        choice1 = safe_input(colored("🔎 Select an option (1-9): ", "1;32"))

                        if choice1 == '1':
                            Manager.createEmp(connection, cursor)
                        elif choice1 == '2':
                            Manager.viewEM(connection, cursor)
                        elif choice1 == '3':
                            Manager.setProject(cursor, connection)
                        elif choice1 == '4':
                            Manager.deleteEmp(connection, cursor)
                        elif choice1 == '5':
                            Manager.allEmp(connection, cursor)
                        elif choice1 == '6':
                            Manager.changePswd(cursor, connection)
                        elif choice1 == '7':
                            Manager.editEM(connection, cursor)
                        elif choice1 == '8':
                            Manager.req(connection, cursor)
                        elif choice1 == '9':
                            Manager.logout()
                            break
                        else:
                            print(colored("⚠️ Invalid option! Please select between 1 and 9.", "1;31"))
                    break
                else:
                    print(colored("❌ Incorrect Manager Credentials! Please try again.", "1;31"))

        elif choice == '2':
            while True:
                email = safe_input(colored("📧 Enter Employee Email: ", "1;32"))
                password = safe_input(colored("🔒 Enter Password: ", "1;32"))

                if Employee.EMlogin(connection, cursor, email, password):

                    while True:
                        print(colored("╔══════════════════════════════════════╗", "1;35"))
                        print(colored("║         👨‍💻 Employee Dashboard      ║", "1;36"))
                        print(colored("╠══════════════════════════════════════╣", "1;35"))
                        print(colored("║ 1. 📨 Requests to Manager            ║", "1;35"))
                        print(colored("║ 2. 📁 View Project Details           ║", "1;35"))
                        print(colored("║ 3. 📝 Update Personal Details        ║", "1;35"))
                        print(colored("║ 4. 🔐 Change Password                ║", "1;35"))
                        print(colored("║ 5. 🧾 Profile                        ║", "1;35"))
                        print(colored("║ 6. 🚪 Logout                         ║", "1;31"))
                        print(colored("╚══════════════════════════════════════╝", "1;35"))

                        choice2 = safe_input(colored("🔎 Select an option (1-6): ", "1;32"))

                        if choice2 == '1':
                            Employee.reqM(connection, cursor, email)
                        elif choice2 == '2':
                            Employee.viewProjectDetails(connection, cursor) 
                        elif choice2 == '3':
                            Employee.updatePD(cursor, connection, email)
                        elif choice2 == '4':
                            Employee.changePSWD(cursor, connection, email)
                        elif choice2 == '5':
                            Employee.profile(connection, cursor, email)
                        elif choice2 == '6':
                            Employee.logout()
                            break
                        else:
                            print(colored("⚠️ Invalid option! Please choose between 1 and 6.", "1;31"))
                    break
                else:
                    print(colored("❌ Incorrect Employee Credentials! Try again.", "1;31"))

        elif choice == '3':
            print()
            print(colored("     🌟 Thank you for using EMS! 🌟", "1;33"))
            print(colored("╔══════════════════════════════════════╗", "1;33"))
            print(colored("║   👋 You have successfully exited.   ║", "1;33"))
            print(colored("║    Have a productive day ahead!      ║", "1;33"))
            print(colored("╚══════════════════════════════════════╝\n", "1;33"))
            sys.exit()

        else:
            print(colored("\n🚫 Invalid input detected!", "1;33"))
            print(colored("💡 Tip: Please enter 1, 2, or 3 as shown in the menu.\n", "1;31"))



if __name__ == "__main__":
    main()


