

from config import db


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from flask_bcrypt import check_password_hash

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

# Models go here!
class User(db.Model, SerializerMixin):

    # This is the users table in our database
    __tablename__ = "users"

    # This are the columns in our database
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Text, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # Relationships
    income = db.relationship("Income", back_populates="user")
    expenses = db.relationship("Expense", back_populates="user")

    # Serialize rules
    serialize_rules = ('-income.user', '-expenses.user', '-password')
    # serialize_only = ('user_name', 'email')

    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)


class Income(db.Model, SerializerMixin):

    # This will store the income of our users
    __tablename__ = 'incomes'

    # This will be the columns in our database
    id = db.Column(db.Integer, primary_key=True)
    # This  will keep track of the income of our user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    source = db.Column(db.Text)
    amount = db.Column(db.Integer, nullable=False)
    date = db.Column(db.TIMESTAMP)
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"))

    # Relationships
    user = db.relationship("User", back_populates="income")
    budget = db.relationship("Budget", back_populates="money")

    # Serialize rules
    serialize_rules = ('-user.income', '-budget.money')


class Budget(db.Model, SerializerMixin):

    # This will be the table to stores the user's budget
    __tablename__ = "budgets"

    # This will be the columns in pur database
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.TIMESTAMP)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    # Relationship
    money = db.relationship("Income", back_populates="budget")
    to_spend = db.relationship("Expense", back_populates="spending")

    # Serialize rules
    serialize_rules = ('-money.budget', '-to_spend.spending')


class Expense(db.Model, SerializerMixin):

    # This is the table to store our expenses
    __tablename__ = "expenses"

    # This  will be the columns in our database
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    amount = db.Column(db.Integer)
    category = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP)
    budget_id = db.Column(db.Integer, db.ForeignKey("budgets.id"))

    # Relationship
    user = db.relationship("User", back_populates="expenses")
    spending = db.relationship("Budget", back_populates="to_spend")

    # Serialize rules
    serialize_rules = ('-user.expenses', '-spending.to_spend')
