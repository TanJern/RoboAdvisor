from my_flask_app import db
from my_flask_app.models import User,Question

db.drop_all()
db.create_all()

user1=User(firstname='user1',username="user1@test.ac.uk",password='passuser1')


q1 = Question(question="In what circumstances is an economy said to be in recession?", option1="A. If real GDP falls in one quarter compared with the quarter before.", option2="B. If real GDP falls for two consecutive quarters.", option3="C. If real GDP falls in one year compared with the year before.", option4="D. If real GDP falls for two consecutive years.",answer="B. If real GDP falls for two consecutive quarters.",feedback="Statement B is correct: this is the definition of a recession used by economists.",level="Advanced",tag="Micro")

q2= Question(question="Which of the following statements is false?", option1="A. The GDP deflator is a price index that covers all goods and services included in GDP.", option2="B. The RPI is a price index that covers a wide range of goods and services bought by households.", option3="C. The CPI is a price index that covers a wide range of goods and services bought by households.", option4="D. The CPI generally rises more quickly than the RPI.",answer="D. The CPI generally rises more quickly than the RPI.",feedback="Statement D is false. The CPI generally rises more slowly than the RPI.",level="Beginner",tag="Macro")

q3= Question(question="Which of the following would cause a bank to lose reserves?", option1="A. One of the bank's depositors makes an internet payment to another of its depositors.", option2="B. One of the bank's depositors pays out a cheque to another of its depositors.", option3="C. One of the bank's depositors pays out a cheque to a depositor of another bank.", option4="D. The bank raises the interest rate it pays on deposits.",answer= "C. One of the bank's depositors pays out a cheque to a depositor of another bank.",feedback="Statement C is correct. In this case, the bank must give reserves to the bank of the person who receives the cheque.",level="Beginner",tag="macro")

q4= Question(question="Which of thwould cause a bank to lose reserves?", option1="A. One of the bank's deposes an internet payment to another of its depositors.", option2="B. One of the bank'spositors pays out a cheque to another of its depositors." ,answer= "B. One of thenk's depositors pays out a cheque to a depositor of another bank.",feedback="Statement is correct. In this case, the bank must give reserves to the bank of the person who receives the cheque.",level="Intermediate",tag="Micro")



db.session.add(user1)
db.session.add(q1)
db.session.add(q2)
db.session.add(q3)
db.session.add(q4)




db.session.commit()