CREATE TABLE IF NOT EXISTS customer(
    customer_id SERIAL PRIMARY KEY,
    customername VARCHAR(20) NOT NULL,
    secret_password VARCHAR(50) NOT NULL,
    last_login TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loan(
    loan_id SERIAL PRIMARY KEY,
    original_principal NUMERIC CHECK (original_principal > 0),
    principal NUMERIC CHECK (principal > 0),
    interest_rate NUMERIC CHECK (interest_rate > 0),
    is_fixed_rate BOOLEAN NOT NULL,
    years_to_pay_off SMALLINT CHECK (years_to_pay_off > 0),
    due_date_day SMALLINT CHECK ( due_date_day > 0 AND due_date_day < 32),
    due_date_month SMALLINT CHECK (due_date_month > 0 AND due_date_month < 13),
    minimum_payment NUMERIC CHECK (minimum_payment > 0),
    loan_name VARCHAR(50) NOT NULL,
    notes VARCHAR(200),
    customer_id INTEGER REFERENCES customer (customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS loan_payment(
    loan_payment_id SERIAL PRIMARY KEY,
    payment_date DATE NOT NULL,
    payment_amount NUMERIC,
    tracking_number VARCHAR(50),
    loan_id INTEGER REFERENCES loan (loan_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS subscription(
    subscription_id SERIAL PRIMARY KEY,
    interval_in_months SMALLINT CHECK (interval_in_months > 0),
    auto_renew_date_day SMALLINT CHECK (auto_renew_date_day > 0 AND auto_renew_date_day < 32),
    auto_renew_date_month SMALLINT CHECK (auto_renew_date_month > 0 AND auto_renew_date_month < 13),
    subscription_cost NUMERIC CHECK (subscription_cost > 0),
    subscription_name VARCHAR(50) NOT NULL,
    notes VARCHAR(200),
    customer_id INTEGER REFERENCES customer (customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fixed_expense(
    fixed_expense_id SERIAL PRIMARY KEY,
    fixed_expense_cost NUMERIC CHECK (fixed_expense_cost > 0),
    monthly_due_date SMALLINT CHECK (monthly_due_date > 0 AND monthly_due_date < 32),
    fixed_expense_name VARCHAR(50),
    notes VARCHAR(200),
    customer_id INTEGER REFERENCES customer (customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS fixed_expense_payment(
    fixed_expense_payment_id SERIAL PRIMARY KEY,
    payment_amount NUMERIC CHECK (payment_amount > 0),
    payment_date TIMESTAMP NOT NULL,
    fixed_expense_id INTEGER REFERENCES fixed_expense (fixed_expense_id) ON DELETE CASCADE
);