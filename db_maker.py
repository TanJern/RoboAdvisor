from my_flask_app import db
from my_flask_app.models import User,Question,Strategies,Asset,UserAsset,UserStrategies

db.drop_all()
db.create_all()

#User account
user1=User(firstname='user1',username="user1@test.ac.uk",password='passuser1')

#Survey questions
q1 = Question(question="What's your understanding of stocks, bonds, commodities, and real estate?", option1="None", option2="Some", option3="Good", option4="Extensive")

q2= Question(question="Which is your investment goal?", option1="Retirement", option2="Generate long term wealth", option3="Build a rainy day fund", option4="Saving for major upcoming expenses")

q3= Question(question="When markets are on a decline, you would...", option1="sell everything", option2="sell some", option3="do nothing", option4="buy more")

q4= Question(question="When making a long-term investment, I plan to keep the money invested for...", option1="1-2 years", option2="3-5 years", option3="6-8 years", option4="more than 8 years")

q5= Question(question="The sources of my income are...", option1="very unstable", option2="unstable", option3="somewhat stable", option4="stable")





#Invesment strategies
s1 = Strategies(strategy="Very conservative", bond=60, stock=20, commodity=5, real_estate=30)

s2 = Strategies(strategy="Conservative", bond=55, stock=25, commodity=5, real_estate=15)

s3 = Strategies(strategy="Moderate", bond=45, stock=35, commodity=10, real_estate=10)

s4 = Strategies(strategy="Growth", bond=25, stock=55, commodity=10, real_estate=10)


#Assets
a1= Asset(symbol="test", etf_name="testing", asset_class="test", total_assets=100,avg_volume=100.00,etf_database_category='test', liquidity_rating="testing", expenses_rating="test", volatility_rating="test",dividend_rating="test")


#UserAssets
u1= UserAsset(symbol="test", etf_name="testing", asset_class="test", total_assets=100,avg_volume=100.00,etf_database_category='test', liquidity_rating="testing", expenses_rating="test", volatility_rating="test",dividend_rating="test",user_id=1)


#User Invesment strategies
us1 = UserStrategies(strategy="Very conservative", bond=60, stock=20, commodity=5, real_estate=30,user_id=1)



db.session.add(user1)
db.session.add(q1)
db.session.add(q2)
db.session.add(q3)
db.session.add(q4)
db.session.add(q5)
db.session.add(s1)
db.session.add(s2)
db.session.add(s3)
db.session.add(s4)
db.session.add(a1)
db.session.add(u1)
db.session.add(us1)

db.session.commit()