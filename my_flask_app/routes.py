from flask import render_template, url_for, request, redirect, flash
from wtforms.widgets.core import html_params
from my_flask_app import app,db
from my_flask_app.models import User,Question
from my_flask_app.forms import LoginForm,QuestionForm,EditForm,FilterForm
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
@login_required
def test():
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
    
  return render_template("test.html",title="Test",questions_list=questions_list)
  


@app.route("/submittest", methods=['POST','GET'])
@login_required
def submittest():
  total_questions=Question.query.order_by(Question.q_id.asc()).count()
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  answered_questions_list=[]
  count=0
  for question in questions_list:
    answered_question= request.form[str(question.q_id)]
    answered_questions_list.append({"answered_question":answered_question,"question":question})
    if question.answer == answered_question:
      count+=1    

  return render_template("submittest.html",title="testresults",questions_list=questions_list,count=count,answered_questions_list=answered_questions_list,total_questions=total_questions)
 

@app.route("/managetest", methods=['POST','GET'])
@login_required
def managetest():
  form=FilterForm()
  level=request.args.get("level")

  if level=="Beginner":
    query=Question.query.filter_by(level="Beginner")

  elif level=="Intermediate":
    query=Question.query.filter_by(level="Intermediate")

  elif level=="Advanced":
    query=Question.query.filter_by(level="Advanced")

  else:
    query=Question.query.order_by(Question.q_id.asc())

  questions_list=query.all()

  return render_template("managetest.html",title="ManageTest",questions_list=questions_list,form=form)


@app.route("/newtest", methods=['POST','GET'])
@login_required
def newtest():    
  form=QuestionForm()
  if form.validate_on_submit():
    question=Question(question=form.question.data,option1=form.option1.data,option2=form.option2.data,option3=form.option3.data,option4=form.option4.data,answer=form.answer.data,feedback=form.feedback.data)
    db.session.add(question)
    db.session.commit()
    flash('Question has been added!','success')
    return redirect(url_for('managetest'))
  return render_template("newtest.html",title="NewTest",form=form)


@app.route("/question/<int:q_id>", methods=['POST','GET'])
@login_required
def question(q_id):    
  question=Question.query.get_or_404(q_id)
  form=EditForm()
  if form.validate_on_submit():
    question.question=form.question.data
    question.option1=form.option1.data
    question.option2=form.option2.data
    question.option3=form.option3.data
    question.option4=form.option4.data
    question.answer=form.answer.data
    question.feedback=form.feedback.data
    db.session.commit()
    flash('Updated')
    return redirect(url_for('question',q_id=question.q_id))
  elif request.method=='GET':
    form.question.data=question.question
    form.option1.data=question.option1
    form.option2.data=question.option2
    form.option3.data=question.option3
    form.option4.data=question.option4
    form.answer.data=question.answer
    form.feedback.data=question.feedback
    
  return render_template("question.html",title="Question",question=question,form=form)


@app.route("/delete/<int:q_id>", methods=['POST'])
@login_required
def delete(q_id):
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  question=Question.query.get_or_404(q_id)

 
  db.session.delete(question)
  db.session.commit()

  flash('Question has been deleted.')

  return redirect(url_for('managetest'))
  
 
     
