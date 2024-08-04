# resources/expense.py

from flask_restful import Resource
from flask import request
from models import db, Expense
from datetime import datetime

class ExpenseResource(Resource):
    def post(self):
        data = request.get_json()
        new_expense = Expense(amount=data['amount'], category=data['category'],
                              description=data['description'], created_at=datetime.now())
        db.session.add(new_expense)
        db.session.commit()
        return new_expense.to_dict(), 201

    def get(self):
        expenses = Expense.query.all()
        return [expense.to_dict() for expense in expenses], 200

    def put(self, id):
        expense = Expense.query.get(id)
        if not expense:
            return {'message': 'Expense not found'}, 404

        data = request.get_json()
        expense.amount = data['amount']
        expense.category = data['category']
        expense.description = data['description']
        db.session.commit()
        return expense.to_dict(), 200

    def delete(self, id):
        expense = Expense.query.get(id)
        if not expense:
            return {"message": "Expense not found"}, 404

        db.session.delete(expense)
        db.session.commit()
        return {"message": "Expense deleted successfully"}, 204
