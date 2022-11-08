import mysql.connector


class AlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SQLConnection:
    def __init__(self, user_name: str, password: str):
        self.cnx = mysql.connector.connect(user=user_name, password=password, database="loan_tracker")
        self.cursor = self.cnx.cursor()

    # HELPERS
    def __dict_to_strs__(self, dictionary: dict) -> (str, str):
        # Used to format the COLUMNS and the VALUES for INSERT queries
        keys = ""
        values = ""
        for (key, value) in dictionary.items():
            keys = f"{key}, {keys}"
            values = f"{value}, {values}"
        return keys.strip(', '), values.strip(', ')

    def __format_sets__(self, dictionary: dict) -> str:
        # Used to format the SETs in the UPDATE statement
        set_str = ""
        for (key, value) in dictionary.items():
            set_str = f"{key} = {value}, {set_str}"
        return set_str.strip(', ')

    def __does_expense_exist__(self, name: str):
        # Checks to see if the expense already exists in the database
        does_exist = 0
        command = f"SELECT 1 FROM static_expenses WHERE name = {name}"
        self.cursor.execute(command)
        if self.cursor.fetchone() is not None:
            does_exist = 1
        return does_exist

    def __get_id__(self, table: str, name: str) -> int:
        # Gets the ID of name from table
        command = f"SELECT {table}_id FROM {table} WHERE name = {name}"
        self.cursor.execute(command)
        (result,) = self.cursor.fetchone()
        return result

    # GETTERS
    def get_loans(self) -> dict:
        # Returns all the names of loans that have been entered in the database
        loans = {}
        command = "SELECT loan_id, name FROM loan"
        self.cursor.execute(command)
        result_set = self.cursor.fetchall()
        for (loan_id, name) in result_set:
            loans[loan_id] = name
        return loans

    def get_loan_information(self, loan_id: str) -> dict:
        # Gets all the information about a specific loan
        columns = "name, duration_in_years, start_date, projected_payoff, due_day, descript, principle, monthly_payment_amount," \
                  f"(SELECT count(*) FROM payment GROUP BY loan_id HAVING loan_id =  {loan_id}) payments"
        command = f"SELECT {columns} FROM loan WHERE loan_id = {loan_id}"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        return {"Name": result[0], "Duration": result[1], "Start Date": result[2], "Projected Payoff": result[3],
                "Due Day": result[4], "Description": result[5], "Principle": result[6],
                "Monthly Payment Amount": result[7], "Payments Made": result[8]}

    def display_expenses(self) -> dict:
        # Gets all the active expenses and preps them for display
        # This includes all the expenses from the static_expense table and the active loans in the loan table
        command = "WITH individual_expenses AS " \
                  "(SELECT name, amount FROM expense " \
                  " UNION " \
                  " SELECT name, monthly_payment_amount FROM loan WHERE active = 1) " \
                  "SELECT name, amount FROM individual_expenses " \
                  "UNION " \
                  "SELECT \"Total Expenses\" name, sum(amount) amount FROM individual_expenses"
        self.cursor.execute(command)
        expenses = {}
        result = self.cursor.fetchall()
        for (name, amount) in result:
            expenses[name] = amount
        return expenses

    def get_expenses(self) -> dict:
        # Returns all the names of the expenses that have been entered in the database
        command = "SELECT expense_id, name FROM expense"
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return {expense_id: expense for (expense_id, expense) in result}

    def get_expense_information(self, expense_id: str) -> dict:
        command = f"SELECT name, amount FROM expense WHERE expense_id = {expense_id}"
        self.cursor.execute(command)
        result = self.cursor.fetchone()
        return{"Name": result[0], "Amount": result[1]}

    def get_unpaid_loans(self) -> dict:
        # Gets all the loans that have not been paid off for the current month
        command = "SELECT name, due_day " \
                  "FROM loan " \
                  "WHERE loan_id NOT IN" \
                  " (SELECT loan_id " \
                  "  FROM payment " \
                  "  WHERE month(payment_date) = month(curdate()) " \
                  "    AND year(payment_date) = year(curdate()))"
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return {loan: day for (loan, day) in result}

    def get_payments(self, loan_id="") -> dict:
        # Gets all the payments that have been made for a specific loan, or all of them
        # if loan_id is not specified, and orders them by date paid in descending order

        where_clause = ""
        if loan_id != "":
            where_clause = f'WHERE l.loan_id = {loan_id}'
        command = 'SELECT p.payment_id, l.name, p.payment_date ' \
                  'FROM loan l INNER JOIN payment p ON l.loan_id = p.loan_id ' \
                  f'{where_clause} ' \
                  'ORDER BY 2, 3 DESC'
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        return {loan_id: {loan: day} for (loan_id, loan, day) in result}

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
        if self.__does_expense_exist__(expense_info["name"]):
            raise AlreadyExistsError(f"{expense_info['name']} is already a known expense\nTry updating it instead.")

        columns, values = self.__dict_to_strs__(expense_info)
        command = f'INSERT INTO expense ({columns}) VALUES ({values})'
        try:
            self.cursor.execute(command)
            self.cnx.commit()
        except mysql.connector.errors.DatabaseError as err:
            print(f'An error has occurred while trying to insert into the database:\n{err}\n')

    def make_payment(self, payment_info: dict):
        # Adds a payment for a specific loan to the database
        columns, values = self.__dict_to_strs__(payment_info)
        command = f'INSERT INTO payment ({columns}) VALUES ({values})'
        try:
            self.cursor.execute(command)
            self.cnx.commit()
        except mysql.connector.errors.DatabaseError as err:
            print(f'An error has occurred while trying to insert into the database:\n{err}\n')
        pass

    def update_loan_info(self, loan: str, loan_info: dict):
        # Updates the information of a specific loan in the database
        command = "UPDATE loan " \
                  f"SET {self.__format_sets__(loan_info)} " \
                  f"WHERE loan_id = {self.__get_id__('loan', loan)}"
        self.cursor.execute(command)
        self.cnx.commit()

    def update_expense_info(self, expense: str, expense_info: dict):
        # Updates the information of a specific expense in the database
        command = "UPDATE expense " \
                  f"SET {self.__format_sets__(expense_info)} " \
                  f"WHERE expense_id = {self.__get_id__('static_expenses', expense)}"
        self.cursor.execute(command)
        self.cnx.commit()

    def close(self):
        # releases the memory for the cursor and the connection to the database
        self.cursor.close()
        self.cnx.close()
