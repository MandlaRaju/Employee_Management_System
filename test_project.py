import pytest
from unittest.mock import MagicMock, patch
from project import Employee  # adjust this import based on your file name

# Dummy email for tests
test_email = "test@example.com"

# ---------------------------------#
#  Test: Update Personal Details   #
# ---------------------------------#
@patch("builtins.input", side_effect=["1", "John Doe"])
def test_update_name(mock_input):
    cursor = MagicMock()
    connection = MagicMock()
    Employee.updatePD(cursor, connection, test_email)
    cursor.execute.assert_called_with("UPDATE employee SET name = %s WHERE email = %s", ("John Doe", test_email))
    connection.commit.assert_called_once()

@patch("builtins.input", side_effect=["2", "newemail@example.com"])
def test_update_email(mock_input):
    cursor = MagicMock()
    connection = MagicMock()
    Employee.updatePD(cursor, connection, test_email)
    cursor.execute.assert_called_with("UPDATE employee SET email = %s WHERE email = %s", ("newemail@example.com", test_email))
    connection.commit.assert_called_once()

@patch("builtins.input", side_effect=["3", "9876543210"])
def test_update_phone(mock_input):
    cursor = MagicMock()
    connection = MagicMock()
    Employee.updatePD(cursor, connection, test_email)
    cursor.execute.assert_called_with("UPDATE employee SET phone_no = %s WHERE email = %s", ("9876543210", test_email))
    connection.commit.assert_called_once()

# --------------------------
# Test: Change Password
# --------------------------
@patch("builtins.input", side_effect=["oldPassword", "Newpass@123"])
def test_change_password_valid(mock_input):
    cursor = MagicMock()
    connection = MagicMock()

    # Simulate a correct current password
    cursor.fetchone.return_value = ("test",)

    Employee.changePSWD(cursor, connection, test_email)

    cursor.execute.assert_any_call("SELECT * FROM employee WHERE email = %s AND password = %s", (test_email, "oldPassword"))
    cursor.execute.assert_any_call("UPDATE employee SET password = %s WHERE password = %s", ("Newpass@123", "oldPassword"))
    connection.commit.assert_called_once()

@patch("builtins.input", side_effect=["wrongPassword"])
def test_change_password_invalid_current(mock_input):
    cursor = MagicMock()
    connection = MagicMock()

    # Simulate wrong current password
    cursor.fetchone.return_value = None

    Employee.changePSWD(cursor, connection, test_email)
    connection.commit.assert_not_called()

# --------------------------#
#    Test: View Profile     #
# --------------------------#
@patch("builtins.input", return_value="")  # simulate key press
def test_profile_found(mock_input):
    cursor = MagicMock()
    connection = MagicMock()

    cursor.fetchall.return_value = [(1, "John", "john@example.com", "Dev", "50000", "1234567890")]

    Employee.profile(connection, cursor, test_email)

    cursor.execute.assert_called_once_with("SELECT id, name, email, role, salary, phone_no FROM employee WHERE email = %s", (test_email,))

@patch("builtins.input", return_value="")
def test_profile_not_found(mock_input):
    cursor = MagicMock()
    connection = MagicMock()

    cursor.fetchall.return_value = []

    Employee.profile(connection, cursor, test_email)
