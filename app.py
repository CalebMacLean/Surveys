# Imports
from flask import Flask, render_template, session, redirect, flash, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

# App Configurations
RESPONSES_KEY = "responses"

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = '1Hav3AS3cr3t'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']  = False

debug = DebugToolbarExtension(app)

# Application
response = []

@app.route('/')
def view_home_page():
    """Select a Survey"""
    title = survey.title
    instructions = survey.instructions

    return render_template('home.html',
                           title=title, 
                           instructions=instructions)

@app.route('/begin', methods=['POST'])
def start_survey():
    """Clear the Survey of Responses"""
    session[RESPONSES_KEY] = []
    
    return redirect('/questions/0')

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Save response and move on to the next question or end the survey"""
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if(len(responses) == len(survey.questions)):
        # they answered all the questions
        return redirect('/complete')
    else:
        return redirect(f'/questions/{len(responses)}')

@app.route('/questions/<int:question_num>', methods=['GET', 'POST'])
def view_question(question_num):
    """Display the Current Question"""
    responses = session.get(RESPONSES_KEY)
    
    if(responses is None):
        # trying to access the question page too soon
        return redirect('/')
    
    if(len(responses) == len(survey.questions)):
        # they have completed all the questions.
        return redirect('/complete')
    
    if(len(responses) != question_num):
        # trying to access questtions out of order
        flash(f"Invalid question id: {question_num}")
        return redirect(f"/questions/{len(responses)}")
    
    q = survey.questions[question_num]
    
    return render_template('question.html',
                           question_num=question_num,
                           question=q.question,
                           choices= q.choices)

@app.route('/complete')
def complete():
    """Complete the Survey"""
    return render_template('complete.html', survey=survey)