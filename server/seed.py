# For our dummy data when testing out our application
from datetime import datetime
from app import app
from models import db, User, Income, Budget,Expense


with app.app_context():
    print("Inputting data")
    User.query.delete()
    Income.query.delete()
    Budget.query.delete()
    Expense.query.delete()

    # To append our new users to this empty array
    new_user = []
    #Adding data to the user table
    charles = User(user_name="Charles Kibet", email="charles@gmail.com", password="charles"
                   )
    new_user.append(charles)
    guido = User(user_name="Guido Python", email="guido@gmail.com", password="charles"
                 )
    new_user.append(guido)
    db.session.add_all(new_user)
    db.session.commit()
    print("Users added successfully")

    #Adding data to the income tables
    new_income = []
    income1 = Income(user=charles, amount=4000, date=datetime.now())
    income2 = Income(user=guido, amount=4000, date=datetime.now())
    new_income.append(income1)
    new_income.append(income2)
    db.session.add_all(new_income)
    db.session.commit()
    print("Income added successfully")
    
    #Adding data to the budgets table
    new_budget = []
    budget1 = Budget(amount=4000,description="Entertainment")
    budget2 = Budget(amount=4000,description="Entertainment")
    new_budget.append(budget1)
    new_budget.append(budget1)
    db.session.add_all(new_budget)
    db.session.commit()
    print("Budgets added successfully")
    
    #Adding data to the Expense table
    new_expense = []
    expense1 = Expense(user=charles,amount=5000,category="Entertainment",description="Leisure",created_at=datetime.now())
    expense2 = Expense(user=guido,amount=5000,category="Transport",description="Gas",created_at=datetime.now())
    new_expense.append(expense1)
    new_expense.append(expense2)
    
    db.session.add_all(new_expense)
    db.session.commit()
    print("Expensed data added successfully")


    