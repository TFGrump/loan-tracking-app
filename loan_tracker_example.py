import loan_tracker_api as lt

cnx = lt.SQLConnection()
loan_info = {'monthly_payment_amount': '1300.00'}
cnx.update_loan_info('\'Student Loans\'', loan_info)
loan = cnx.get_loan_information("\'Student Loans\'")

print("Info for \"Student Loans\"")
for (thing, value) in loan.items():
    print(f'{thing}: {value}')

print('\nExpenses:')
expenses = cnx.get_expenses()
for (expense, amount) in expenses:
    print(f'{expense}: {amount:.2f}')


cnx.close()
