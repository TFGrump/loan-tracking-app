import mysql.connector


class SQLConnection:
    def __init__(self):
        self.cnx = mysql.connector.connect(user="TJ", password="Rub!kSCub3SQL", database="loan_tracker", host="127.0.0.1")
        self.cursor = self.cnx.cursor()

    # HELPERS
    def __dict_to_str__(self, dictionary: dict) -> (str, str):
        # Used to format the COLUMNS and the VALUES for INSERT queries
        keys = ""
        values = ""
        for (key, value) in dictionary.items():
            keys = f"{key}, {keys}"
            values = f"{value}, {values}"
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

    # SETTERS
    def add_loan(self, loan_info: dict):
        # Adds a loan to the database
        columns, values = self.__dict_to_str__(loan_info)
        command = f'INSERT INTO loan ({columns}) VALUES ({values})'
        try:
            self.cursor.execute(command)
        except mysql.connector.errors.DatabaseError as err:
            print(f'An error has occurred while trying to insert into the database: \n{err}')

    def make_payment(self, payment_info: dict):
        # Adds a payment for a specific loan to the database
        # TODO: add insert statements so that the user can add payments that they have made on loans
        pass

    def update_loan_info(self):
        # Updates the information of a specific loan in the database
        # TODO: add update statements so that the user can update loan information
        pass

    def close(self):
        # releases the memory for the cursor and the connection to the database
        self.cursor.close()
        self.cnx.close()


cnx = SQLConnection()
print(cnx.get_loans())
loan_information = cnx.get_loan_information('\'Car loan\'')
for (key, value) in loan_information.items():
    print(f'{key}: {value}')
cnx.close()
