import loan_tracker_api as lt
import mysql.connector


def __verify_input__(user_input: str) -> bool:
    pass


def __format_dict__(dictionary: dict) -> str:
    dictionary_str = ""
    for (column, value) in dictionary.items():
        dictionary_str += f'{column}: {value}\n'
    return dictionary_str


def __format_payments__(payments: dict, show_total_payments=False) -> str:
    dictionary_str = '------- Payments -------\n'
    if show_total_payments:
        dictionary_str += f'You have made {len(payments)} payments\n\n'
    for (payment_id, payment) in payments.items():
        dictionary_str += __format_dict__(payment)
    return dictionary_str + '------------------------\n'


def __loan_menu__(loans: dict, prompt: str) -> str:
    menu_str = f'--------- Loans --------\n{prompt}'
    for (loan_id, loan) in loans.items():
        menu_str += f'\n{loan_id}. {loan}'
    menu_str += '\n0. Back\n------------------------\n'
    return menu_str


def __expense_menu__(expenses: dict, prompt: str) -> str:
    menu_str = f'------- Expenses -------\n{prompt}'
    for (expense_id, expense) in expenses.items():
        menu_str += f'\n{expense_id}. {expense}'
    menu_str += '\n0. Back\n------------------------\n'
    return menu_str


def __edit_menu__(expense: dict) -> str:
    menu_str = f'--------- Edit ---------\n' \
               f'Select the values you wish to edit\nSeparate by commas (,)\n'
    menu_str += __format_dict__(expense)
    menu_str += '0. Back\n------------------------\n'
    return menu_str


def __verify__(dictionary: dict) -> int:
    # Will prompt the user to the information is correct
    # Returns a 1 if True and 0 if False
    if len(dictionary) == 0:
        return 0
    else:
        prompt = "Is the information correct?:\n"
        for (column, value) in dictionary.items():
            prompt += f'{column}: {value}\n'
        prompt += '             1. Yes\n[Anything else]. No\n'
        user_input = int(input(prompt))
        if user_input == 1:
            return 1
        else:
            return 0


def view_loans(cnx: lt.SQLConnection):
    while True:
        loans = cnx.get_loans()
        user_input = input(__loan_menu__(loans, 'Select a loan that you want to view'))

        if user_input == '0':
            break
        elif user_input == "":
            continue
        else:
            try:
                print(__format_dict__(cnx.get_loan_information(user_input)))
            except TypeError:
                print('That loan is not in the database')


def view_expenses(cnx: lt.SQLConnection):
    while True:
        expenses = cnx.get_expenses()
        user_input = input(__expense_menu__(expenses, 'Select the expense you wish to view'))

        if user_input == '0':
            break
        elif user_input == "":
            continue
        else:
            try:
                print(__format_dict__(cnx.get_expense_information(user_input)))
            except TypeError:
                print('That expense is not in the database')


def view_payments(cnx: lt.SQLConnection):
    while True:
        loans = cnx.get_loans()
        loans['-1'] = 'All'
        user_input = input(__loan_menu__(loans, 'Select the loan that you want to see the payments of:'))

        if user_input == '0':
            break
        elif user_input == '-1':
            print(__format_payments__(cnx.get_payments()))
        elif user_input == "":
            continue
        else:
            try:
                print(__format_payments__(cnx.get_payments(user_input), True))
            except TypeError:
                print('That Loan is not in the database')


def edit_expense(cnx: lt.SQLConnection):
    while True:
        expenses = cnx.get_expenses()
        user_input = input(__expense_menu__(expenses, "Select the expense you wish to edit"))

        if user_input == '0':
            break
        else:
            while True:
                user_input = input(__edit_menu__(cnx.get_expense_information(user_input)))

                if user_input == '0':
                    break
                else:
                    print(user_input)


def display_expenses(cnx: lt.SQLConnection):
    expenses = cnx.display_expenses()
    output_str = f'------- Expenses -------'
    for (name, amount) in expenses.items():
        output_str += f'\n{name}: {amount:.2f}'
    output_str += '\n------------------------\n'
    print(output_str)


def display_unpaid_loans(cnx: lt.SQLConnection):
    loans = cnx.get_unpaid_loans().items()
    if len(loans) == 0:
        out_str = "You have paid everything off for the month\n"
    else:
        out_str = "You have yet to pay:\n"
        for (loan, day) in loans:
            out_str += f'{loan} still needs to be paid by the {day}\n'
    print(out_str)


def make_payment(cnx: lt.SQLConnection):
    while True:
        loans = cnx.get_loans()
        print("You will be able to verify the payment information after you have entered everything.")
        loan = input(__loan_menu__(loans, 'What loan do you want to make a payment for?'))

        if loan == '0':
            break
        elif loan == "":
            continue
        else:
            payment_information = {}
            while True:

                amount = input("Enter the amount paid: ")
                tracking = input("Enter the tracking number (Press [Enter] if none): ")

                payment_information["loan_id"] = loan
                payment_information["payment_amount"] = amount
                if tracking != "":
                    payment_information["tracking_number"] = tracking

                if __verify__(payment_information):
                    cnx.make_payment(payment_information)
                    print('PAYMENT ADDED\n')
                    break


def main(cnx: lt.SQLConnection):
    while True:
        user_input = input("--------- Menu ---------\n"
                           "1. View Loans\n"
                           "2. View Expenses\n"
                           "3. Edit Expense\n"
                           "4. Display Expenses\n"
                           "5. Make Payment\n"
                           "6. Check Payments\n"
                           "7. View Payments\n"
                           "0. Exit\n"
                           "------------------------\n")

        if user_input == '1':
            view_loans(cnx)
        elif user_input == '2':
            view_expenses(cnx)
        elif user_input == '3':
            edit_expense(cnx)
        elif user_input == '4':
            display_expenses(cnx)
        elif user_input == '5':
            make_payment(cnx)
        elif user_input == '6':
            display_unpaid_loans(cnx)
        elif user_input == '7':
            view_payments(cnx)
        elif user_input == '0':
            cnx.close()
            break
        else:
            print('Not a valid input\n')


try:
    connection = lt.SQLConnection("TJ", "Rub!kSCub3SQL")
    main(connection)
except mysql.connector.errors.ProgrammingError as err:
    print('Invalid Credentials')
