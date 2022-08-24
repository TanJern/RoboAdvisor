from flask import render_template, url_for, request, redirect, flash, jsonify
from wtforms.widgets.core import html_params
from my_flask_app import app,db
from my_flask_app.models import User,Question, Strategies,Asset,UserAsset,UserStrategies
from my_flask_app.forms import LoginForm,FilterForm
from flask_login import login_user, logout_user, current_user, login_required
import pickle
import pandas as pd
import numpy as np

#Reading CSV
dataset= pd.read_csv("C:/Users/c2070756/autoassessmenttool/assessment/etfdb.csv")


#Replacing alphabet ratings
alpha_not_accepted=['Liquidity_Rating','Expenses_Rating','Volatility_Rating','Dividend_Rating']
for column in alpha_not_accepted:
    dataset[column]= dataset[column].replace('A+',0)
    dataset[column]= dataset[column].replace('A',1)
    dataset[column]= dataset[column].replace('A-',1)
    dataset[column]= dataset[column].replace('B+',2)
    dataset[column]= dataset[column].replace('B',2)
    dataset[column]= dataset[column].replace('B-',3)
    dataset[column]= dataset[column].replace('C+',3)
    dataset[column]= dataset[column].replace('C',3)
    dataset[column]= dataset[column].replace('C-',3)
    dataset[column]=dataset[column].replace(np.NaN,2)

indices=pickle.load(open("model.pkl","rb"))


@app.route('/')
@app.route('/home')
def home():
  print(indices)
  return render_template('home.html')


#code below are adapted from my own previous work:
#https://git.cardiff.ac.uk/c2070756/2070756_cmt120_cw2
#Login Page
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



#Page for logging in errors
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



#Logout
@app.route("/logout")
def logout():
  logout_user()
  flash('You have been logged out.')
  return redirect(url_for('home'))



#Account page which shows user's bookmarked assets
@app.route("/account")
@login_required
def account():
  #Search filter
  form=FilterForm()
  asset_class=request.args.get("asset_class")
  query=UserAsset.query

  if asset_class=="All":
    query=UserAsset.query.order_by(UserAsset.u_id.asc())
  elif asset_class:
    query=query.filter(UserAsset.asset_class == asset_class)
  else:
    query=UserAsset.query.order_by(UserAsset.u_id.asc())
  user_assets=query.all()

  if form.validate_on_submit(): 
    return redirect(url_for('personal_recommend'))
  return render_template('account.html',title='Account',user_assets=user_assets,form=form)
  


@app.route("/personal_recommend",methods=['GET','POST'])
def personal_recommend():
  flash('Recommendation for ETFs generated.')
  asset_name = request.form["radio"]

  #code below are adapted from this page:
  #https://gist.github.com/Tahsin-Mayeesha/81dcdafc61b774768b64ba5201e31e0a#file-recommending-anime-with-k-nearest-neighbor-ipynb
  #Generate asset ID
  def get_index_from_asset_name(ETF_Name):
    return dataset[dataset["ETF_Name"]==ETF_Name].index.tolist()[0]

  #Generate list of similar assets
  def print_similar_assets(query):
    list=[]
    found_id = get_index_from_asset_name(query)
    for id in indices[found_id][1:]:
        list.append([dataset.iloc[id]["Symbol"],dataset.iloc[id]["ETF_Name"],dataset.iloc[id]["Asset Class"],dataset.iloc[id]["Total Assets($)"],dataset.iloc[id]["Avg Volume"],dataset.iloc[id]["ETF Database Category"]])
    return list
  recommend=print_similar_assets(asset_name)
  return render_template('personal_recommend.html',title='Recommendations',recommend=recommend)



#code below are adapted from my previous own work:
#https://git.cardiff.ac.uk/c2070756/2070756_cmt120_cw2
#Page for all assets
@app.route("/ETF", methods=['POST','GET'])
@login_required
def etf():
  #Search Filter
  form=FilterForm()
  asset_class=request.args.get("asset_class")
  query=Asset.query

  if asset_class=="All":
    query=Asset.query.order_by(Asset.a_id.asc())
  elif asset_class:
    query=query.filter(Asset.asset_class == asset_class)
  else:
    query=Asset.query.order_by(Asset.a_id.asc())

  assets_list=query.all()

  #Bookmark
  if request.method == 'POST':
    checkbox=request.form.getlist('checkbox')
    bookmark=map(int, checkbox)
    print(checkbox)
    for t in bookmark:
      userasset=UserAsset(symbol=assets_list[t].symbol,etf_name=assets_list[t].etf_name,asset_class=assets_list[t].asset_class,total_assets=assets_list[t].total_assets,avg_volume=assets_list[t].avg_volume,etf_database_category=assets_list[t].etf_database_category,liquidity_rating=assets_list[t].liquidity_rating,expenses_rating=assets_list[t].expenses_rating,volatility_rating=assets_list[t].volatility_rating,dividend_rating=assets_list[t].dividend_rating,user_id=current_user.id)
      db.session.add(userasset)
      db.session.commit()
    flash('Assets have been succesfully bookmarked.')
  return render_template('etf.html',title='ETF',assets_list=assets_list,form=form)



#Page for stock assets
@app.route("/Stock", methods=['POST','GET'])
@login_required
def stock():
  #Search Filter
  form=FilterForm()
  stock_class=request.args.get("stock_class")
  query=Asset.query

  if stock_class=="All":
    query=Asset.query.filter(Asset.asset_class == 'Stock')
  elif stock_class:
    query=query.filter(Asset.etf_database_category == stock_class)
  else:
    query=Asset.query.filter(Asset.asset_class == 'Stock')
  assets_list=query.all()

  #Bookmark
  if request.method == 'POST':
    checkbox=request.form.getlist('checkbox')
    bookmark=map(int, checkbox)
    print(checkbox)
    for t in bookmark:
      userasset=UserAsset(symbol=assets_list[t].symbol,etf_name=assets_list[t].etf_name,asset_class=assets_list[t].asset_class,total_assets=assets_list[t].total_assets,avg_volume=assets_list[t].avg_volume,etf_database_category=assets_list[t].etf_database_category,liquidity_rating=assets_list[t].liquidity_rating,expenses_rating=assets_list[t].expenses_rating,volatility_rating=assets_list[t].volatility_rating,dividend_rating=assets_list[t].dividend_rating,user_id=current_user.id)
      db.session.add(userasset)
      db.session.commit()
    flash('Assets have been succesfully bookmarked.')
  return render_template('stock.html',title='Stock',assets_list=assets_list,form=form)



#Page for bond assets
@app.route("/Bond", methods=['POST','GET'])
@login_required
def bond():
  #Search Filter
  form=FilterForm()
  bond_class=request.args.get("bond_class")
  query=Asset.query

  if bond_class=="All":
    query=Asset.query.filter(Asset.asset_class == 'Bond')
  elif bond_class:
    query=query.filter(Asset.etf_database_category == bond_class)
  else:
    query=Asset.query.filter(Asset.asset_class == 'Bond')
  assets_list=query.all()

  #Bookmark
  if request.method == 'POST':
    checkbox=request.form.getlist('checkbox')
    bookmark=map(int, checkbox)
    print(checkbox)
    for t in bookmark:
      userasset=UserAsset(symbol=assets_list[t].symbol,etf_name=assets_list[t].etf_name,asset_class=assets_list[t].asset_class,total_assets=assets_list[t].total_assets,avg_volume=assets_list[t].avg_volume,etf_database_category=assets_list[t].etf_database_category,liquidity_rating=assets_list[t].liquidity_rating,expenses_rating=assets_list[t].expenses_rating,volatility_rating=assets_list[t].volatility_rating,dividend_rating=assets_list[t].dividend_rating,user_id=current_user.id)
      db.session.add(userasset)
      db.session.commit()
    flash('Assets have been succesfully bookmarked.')
  return render_template('bond.html',title='Bond',assets_list=assets_list,form=form)




#Page for commodity assets
@app.route("/Commodity", methods=['POST','GET'])
@login_required
def commodity():
  #Search Filter
  form=FilterForm()
  commodity_class=request.args.get("commodity_class")
  query=Asset.query

  if commodity_class=="All":
    query=Asset.query.filter(Asset.asset_class == 'Commodity')
  elif commodity_class:
    query=query.filter(Asset.etf_database_category == commodity_class)
  else:
    query=Asset.query.filter(Asset.asset_class == 'Commodity')
  assets_list=query.all()

  #Bookmark
  if request.method == 'POST':
    checkbox=request.form.getlist('checkbox')
    bookmark=map(int, checkbox)
    print(checkbox)
    for t in bookmark:
      userasset=UserAsset(symbol=assets_list[t].symbol,etf_name=assets_list[t].etf_name,asset_class=assets_list[t].asset_class,total_assets=assets_list[t].total_assets,avg_volume=assets_list[t].avg_volume,etf_database_category=assets_list[t].etf_database_category,liquidity_rating=assets_list[t].liquidity_rating,expenses_rating=assets_list[t].expenses_rating,volatility_rating=assets_list[t].volatility_rating,dividend_rating=assets_list[t].dividend_rating,user_id=current_user.id)
      db.session.add(userasset)
      db.session.commit()
    flash('Assets have been succesfully bookmarked.')
  return render_template('commodity.html',title='Commodity',assets_list=assets_list,form=form)



#Page for real estate assets
@app.route("/Realestate", methods=['POST','GET'])
@login_required
def realestate():
  #Search filter
  form=FilterForm()
  real_estate_class=request.args.get("real_estate_class")
  query=Asset.query

  if real_estate_class=="All":
    query=Asset.query.filter(Asset.asset_class == 'Real Estate')
  elif real_estate_class:
    query=query.filter(Asset.etf_database_category == real_estate_class)
  else:
    query=Asset.query.filter(Asset.asset_class == 'Real Estate')
  assets_list=query.all()

  #Bookmark
  if request.method == 'POST':
    checkbox=request.form.getlist('checkbox')
    bookmark=map(int, checkbox)
    print(checkbox)
    for t in bookmark:
      userasset=UserAsset(symbol=assets_list[t].symbol,etf_name=assets_list[t].etf_name,asset_class=assets_list[t].asset_class,total_assets=assets_list[t].total_assets,avg_volume=assets_list[t].avg_volume,etf_database_category=assets_list[t].etf_database_category,liquidity_rating=assets_list[t].liquidity_rating,expenses_rating=assets_list[t].expenses_rating,volatility_rating=assets_list[t].volatility_rating,dividend_rating=assets_list[t].dividend_rating,user_id=current_user.id)
      db.session.add(userasset)
      db.session.commit()
    flash('Assets have been succesfully bookmarked.')
  return render_template('realestate.html',title='Realestate',assets_list=assets_list,form=form)



#Questionnaire for recommender system
@app.route("/test", methods=['POST','GET'])
@login_required
def test():
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  return render_template("test.html",title="Test",questions_list=questions_list)
  


#Results of recommender system
@app.route("/submittest", methods=['POST','GET'])
@login_required
def submittest():
  total_questions=Question.query.order_by(Question.q_id.asc()).count()
  questions_list=Question.query.order_by(Question.q_id.asc()).all()
  answered_questions_list=[]
  count=0

  #Taking count of user's score based on answered question
  for question in questions_list:
    answered_question= request.form[str(question.q_id)]
    answered_questions_list.append({"answered_question":answered_question,"question":question})
    if question.option1 == answered_question:
      count+=1
    elif question.option2 == answered_question:
      count+=2
    elif question.option3 == answered_question:
      count+=3
    elif question.option4 == answered_question:
      count+=4
 

  #Calculation to determine and generate chart for user's asset allocation
  strategies_list=Strategies.query.order_by(Strategies.s_id.asc()).all()
  result=0

  if count>=4 and count <=6:
    result=strategies_list[0]
  elif count >=7 and count <=10:
    result=strategies_list[1]
  elif count >=11 and count <=13:
    result=strategies_list[2]
  elif count >=14 and count <=16:
    result=strategies_list[3]

  
  #code below are adapted from my own previous work:
  #https://git.cardiff.ac.uk/c2070756/aat/-/tree/master/my_flask_app
  #Labeling user's goal and risk tolerance based on survey answers
  user=User.query.get(current_user.id)
  rating=[]
  for question in range(1,len(questions_list)):
    answered_question= request.form[str(questions_list[question].q_id)]
    answered_questions_list.append({"answered_question":answered_question,"question":question})
    if questions_list[question].option1 == answered_question:
      rating.append(0)
    elif questions_list[question].option2 == answered_question:
      rating.append(1)
    elif questions_list[question].option3 == answered_question:
      rating.append(2)
    elif questions_list[question].option4 == answered_question:
      rating.append(3)
   
  user.dividend_rating=rating[0]
  user.volatility_rating=rating[1]
  user.liquidity_rating=rating[2]
  user.expenses_rating=rating[3]
  db.session.commit()
  
  #Saves and updates asset allocation for user
  strategy = UserStrategies(strategy=result.strategy,bond=result.bond, stock=result.stock,commodity=result.commodity,real_estate=result.real_estate,user_id=current_user.id)
  db.session.add(strategy)
  db.session.commit()
  flash('User asset allocation has been updated.')


  #code below are adapted from this page:
  #https://gist.github.com/Tahsin-Mayeesha/81dcdafc61b774768b64ba5201e31e0a#file-recommending-anime-with-k-nearest-neighbor-ipynb

  #Generate asset ID
  def get_index_from_asset_name(ETF_Name):
    return dataset[dataset["ETF_Name"]==ETF_Name].index.tolist()[0]

  #Function generates asset names with similar rating
  def get_asset_from_rating(Liquidity_Rating,Expenses_Rating,Dividend_Rating,Volatility_Rating):
    return dataset[(dataset["Liquidity_Rating"]==Liquidity_Rating) & (dataset["Expenses_Rating"] == Expenses_Rating) & (dataset["Dividend_Rating"] == Dividend_Rating) & (dataset["Volatility_Rating"] == Volatility_Rating)].ETF_Name.tolist() 

  #Generate list of similar assets
  def print_similar_assets(query):
    list=[]
    found_id = get_index_from_asset_name(query)
    for id in indices[found_id][1:]:
        list.append([dataset.iloc[id]["Symbol"],dataset.iloc[id]["ETF_Name"],dataset.iloc[id]["Asset Class"],dataset.iloc[id]["Total Assets($)"],dataset.iloc[id]["Avg Volume"],dataset.iloc[id]["ETF Database Category"]])
    return list

  recommend=print_similar_assets(get_asset_from_rating(user.liquidity_rating,user.expenses_rating,user.dividend_rating,user.volatility_rating)[0])
  
  return render_template("submittest.html",title="testresults",questions_list=questions_list,count=count,answered_questions_list=answered_questions_list,total_questions=total_questions, strategies_list= strategies_list,result=result,strategy=strategy,user=user,recommend=recommend)


     
