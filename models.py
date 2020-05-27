from flask import current_app
from app import db
import app.models
from datetime import datetime

class GrammarCheck(db.Model):
	__table_args__ = {'sqlite_autoincrement': True}
	id = db.Column(db.Integer, primary_key=True)
	timestamp = db.Column(db.DateTime, default=datetime.now())
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	def __repr__(self):
		return '<Grammar Check {}>'.format(self.id)

# Delete all records of a grammar check
def delete_all_grammar_check_records_from_user_id(user_id):
	checks = GrammarCheck.query.filter_by(user_id=user_id).all()
	if checks is not None:
		for check in checks:
			db.session.delete(check)
	db.session.commit()
