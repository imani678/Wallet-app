import os
from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import app, db, init_app  # Ensure correct imports from config
from models import User, Income, Budget, Expense  # Import all models to register them
from resources.user import Register, Login
from resources.expense import ExpenseResource
from resources.budget import BudgetResource
from resources.income import IncomeResource

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your_jwt_secret_key')

# Initialize the app with SQLAlchemy
init_app(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

api = Api(app)

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(IncomeResource, '/incomes', '/incomes/<int:id>')
api.add_resource(ExpenseResource, '/expenses', '/expenses/<int:id>')
api.add_resource(BudgetResource, '/budgets', '/budgets/<int:id>')

if __name__ == '__main__':
    app.run()
