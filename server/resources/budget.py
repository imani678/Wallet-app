# resources/budget.py

from flask_restful import Resource
from flask import request
from models import db, Budget

class BudgetResource(Resource):
    def post(self):
        data = request.get_json()
        new_budget = Budget(amount=data['amount'], description=data['description'])
        db.session.add(new_budget)
        db.session.commit()
        return {"message": "Budget added successfully"}, 201

    def get(self):
        budgets = Budget.query.all()
        return [budget.to_dict() for budget in budgets], 200

    def put(self, id):
        budget = Budget.query.get(id)
        if not budget:
            return {'message': 'Budget not found'}, 404

        data = request.get_json()
        budget.amount = data['amount']
        budget.description = data['description']
        db.session.commit()
        return budget.to_dict(), 200

    def delete(self, id):
        budget = Budget.query.get(id)
        if not budget:
            return {'message': "Budget not found"}, 404

        db.session.delete(budget)
        db.session.commit()
        return {"message": "Budget deleted successfully"}, 204
