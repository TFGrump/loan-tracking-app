import mysql.connector


class AlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SQLConnection:
    def __init__(self):
        self.cnx = mysql.connector.connect()
        self.cursor = self.cnx.cursor()

    # HELPERS
    def __dict_to_strs__(self, dictionary: dict) -> (str, str):
        # Used to format the COLUMNS and the VALUES for INSERT queries
        keys = ""
        values = ""
        for (key, value) in dictionary.items():
            keys = f"{keys}, {key}"
            values = f"{values}, {value}"
        return keys.strip(', '), values.strip(', ')

    # GETTERS
    def get_loans(self) -> [str]:
        # Returns all the names of loans that have been entered in the database
        loans = []
        command = "SELECT name FROM loan"
        self.cursor.execute(command)
        result_set = self.cursor.fetchall()
        for (result,) in result_set:
            loans.append(result)
        return loans

    def get_loan_information(self, loan: str) -> [dict]:
        # Gets all the information about a specific loan
        columns = "duration_in_years, start_date, projected_payoff, due_day, descript, principle, monthly_payment_amount," \
                  f"(SELECT count(*) FROM loan_payments GROUP BY loan_id HAVING loan_id = (SELECT loan_id FROM loan WHERE name = {loan})) payments"
        command = f"SELECT {columns} FROM loan WHERE name = {loan}"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        return {"Duration": result[0], "Start Date": result[1], "Projected Payoff": result[2],
                "Due Day": result[3], "Description": result[4], "Principle": result[5],
                "Monthly Payment Amount": result[6], "Payments Made": result[7]}

    def __get_expense__(self, name: str):
        does_exist = 0
        command = f"SELECT 1 FROM static_expenses WHERE name = {name}"
        self.cursor.execute(command)
        if self.cursor.fetchone() is not None:
            does_exist = 1
        return does_exist

    def get_expenses(self) -> [dict]:
        # Gets all the active expenses
        # This includes all the expenses from the static_expense table and the active loans in the loan table
        command = "SELECT name, amount FROM static_expenses " \
                  "UNION " \
                  "SELECT name, monthly_payment_amount FROM loan WHERE active = 1"
        self.cursor.execute(command)
        return self.cursor.fetchall()

    # SETTERS
    def add_loan(self, loan_info: dict):
        # Adds a loan to the database
        if self.get_loan_information(loan_info["name"]):
            raise AlreadyExistsError(f"{loan_info['name']} is already a known loan\nTry updating it instead.")

        columns, values = self.__dict_to_strs__(loan_info)
        command = f'INSERT INTO loan ({columns}) VALUES ({values})'
        try:
            self.cursor.execute(command)
            self.cnx.commit()
        except mysql.connector.errors.DatabaseError as err:
            print(f'An error has occurred while trying to insert into the database:\n{err}\n')

    def add_expense(self, expense_info: dict):
        # Adds an expense to the database
        if self.__get_expense__(expense_info["name"]):
            raise AlreadyExistsError(f"{expense_info['name']} is already a known expense\nTry updating it instead.")

        columns, values = self.__dict_to_strs__(expense_info)
        command = f'INSERT INTO static_expenses ({columns}) VALUES ({values})'
        try:
            self.cursor.execute(command)
            self.cnx.commit()
        except mysql.connector.errors.DatabaseError as err:
            print(f'An error has occurred while trying to insert into the database:\n{err}\n')

    def make_payment(self, payment_info: dict):
        # Adds a payment for a specific loan to the database
        columns, values = self.__dict_to_strs__(payment_info)
        command = f'INSERT INTO loan_payments ({columns}) VALUES ({values})'
        try:
            self.cursor.execute(command)
            self.cnx.commit()
        except mysql.connector.errors.DatabaseError as err:
            print(f'An error has occurred while trying to insert into the database:\n{err}\n')
        pass

    def update_loan_info(self, loan: str, loan_info: dict):
        # Updates the information of a specific loan in the database
        # TODO: add UPDATE statement so that the user can update loan information
        pass

    def close(self):
        # releases the memory for the cursor and the connection to the database
        self.cursor.close()
        self.cnx.close()


cnx = SQLConnection()
expense = {"name": "\"Car Insurance\"", "amount": "294.22"}
try:
    cnx.add_expense(expense)
except AlreadyExistsError as err:
    print(err)
print(cnx.get_expenses())
cnx.close()
