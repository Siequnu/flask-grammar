from flask import render_template, current_app, session
from flask_login import current_user, login_required

from . import bp
from .forms import GrammarSubmissionForm
from .models import GrammarCheck

from app import db
from datetime import datetime

import ProWritingAidSDK
from ProWritingAidSDK.rest import ApiException

configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = current_app.config['PRO_WRITING_AID_API_KEY']

api_instance = ProWritingAidSDK.TextApi(ProWritingAidSDK.ApiClient('https://api.prowritingaid.com'))

# Check grammar
@bp.route("/check/", methods=['GET', 'POST'])
@login_required
def check_grammar():
	form = GrammarSubmissionForm()
	if form.validate_on_submit():
		new_grammar_check = GrammarCheck(user_id = current_user.id, timestamp = datetime.now())
		db.session.add(new_grammar_check)
		db.session.commit()
		
		body = form.body.data 
		api_request = ProWritingAidSDK.TextAnalysisRequest(body, ["grammar"], "General", "en")
		api_response = api_instance.post(api_request)
	
		return render_template('check_grammar.html', form = form, api_response = api_response, body = body) 
	return render_template('check_grammar.html', form = form) 