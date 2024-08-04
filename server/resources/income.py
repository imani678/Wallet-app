# resources/income.py

from flask import request
from datetime import datetime
from models import db, Income
from flask_restful import Resource

class IncomeResource(Resource):
    def get(self):
        incomes = Income.query.all()
        return [income.to_dict() for income in incomes], 200

    def post(self):
        data = request.get_json()
        new_income = Income(source=data['source'], amount=data['amount'], date=datetime.now())
        db.session.add(new_income)
        db.session.commit()
        return new_income.to_dict(), 201

    def put(self, id):
        income = Income.query.get(id)
        if not income:
            return {'message': 'Income not found'}, 404

        data = request.get_json()
        income.source = data['source']
        income.amount = data['amount']
        db.session.commit()
        return income.to_dict(), 200

    def delete(self, id):
        income = Income.query.get(id)
        if not income:
            return {'message': "Income not found"}, 404

        db.session.delete(income)
        db.session.commit()
        return {"message": "Income deleted successfully"}, 204
