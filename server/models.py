from config import db
from sqlalchemy_serializer import SerializerMixin
from flask_bcrypt import check_password_hash

class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    income = db.relationship("Income", back_populates="user")
    expenses = db.relationship("Expense", back_populates="user")

    serialize_rules = ('-income.user', '-expenses.user', '-password')

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

class Income(db.Model, SerializerMixin):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    source = db.Column(db.Text)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP)
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"))

    user = db.relationship("User", back_populates="income")
    budget = db.relationship("Budget", back_populates="money")

    serialize_rules = ('-user.income', '-budget.money')

class Budget(db.Model, SerializerMixin):
    __tablename__ = "budgets"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    money = db.relationship("Income", back_populates="budget")
    to_spend = db.relationship("Expense", back_populates="spending")

    serialize_rules = ('-money.budget', '-to_spend.spending')

class Expense(db.Model, SerializerMixin):
    __tablename__ = "expenses"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    amount = db.Column(db.Integer)
    category = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP)
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"))

    user = db.relationship("User", back_populates="expenses")
    spending = db.relationship("Budget", back_populates="to_spend")

    serialize_rules = ('-user.expenses', '-spending.to_spend')
