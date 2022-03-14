from flask import render_template, url_for, request, redirect, flash
from wtforms.widgets.core import html_params
from my_flask_app import app,db
from my_flask_app.models import User,Question
from my_flask_app.forms import LoginForm,TestForm
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/login",methods=['GET','POST'])
def login():
  #Making page only accessible for guests
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()

  #Logs in registered user
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user,remember=form.remember_me.data)
      flash('You\'ve successfully logged in!')
      return redirect(url_for('home'))
    flash('Incorrect email or password supplied.')
    return redirect(url_for('login_error'))
  return render_template('login.html',title='Login', form=form)


@app.route("/login_error",methods=['GET','POST'])
def login_error():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()

   #Logs in registered users
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is not None and user.verify_password(form.password.data):
      login_user(user)
      flash('You\'ve successfully logged in!')
      return redirect(url_for('home'))
    flash('Incorrect email or password supplied.') 
  return render_template('login_error.html',title='Login_error', form=form)


@app.route("/logout")
def logout():
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
  return render_template('account.html',title='Account')




    

@app.route("/test", methods=['POST','GET'])
def test():

  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  if current_user.is_authenticated:
   # if form.validate_on_submit
   # count=0
    #question_id = str(Question.q_id)
    #selected_option = request.form[question_id]
    #for question in questions_list:
      #if question.answer == selected_option:
       # count +=1

    #{% for subfield in form.radio %}
               # <tr>
               #     <td>{{ subfield }}{{ subfield.label }}</td> <br>
             #   </tr>
           # {% endfor %} -->
    
    return render_template("test.html",title="Test",questions_list=questions_list)
  
  else:
    return redirect(url_for('home'))

@app.route("/submittest", methods=['POST','GET'])
def submittest():
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  count=0
  for question in questions_list:
    question_id=str(question.q_id)
    selected_option= request.form[question_id]
    if question.answer == selected_option:
        count +=1
    
    count=str(count)
  
  return render_template("submittest.html",title="testresults",questions_list=questions_list,count=count)
 
