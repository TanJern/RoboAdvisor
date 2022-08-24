from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField
from wtforms.validators import DataRequired
from my_flask_app.models import User,Question
from flask_login import current_user


class LoginForm(FlaskForm):
  username = StringField('Username',validators=[DataRequired()])
  password = PasswordField('Password',validators=[DataRequired()])
  remember_me=BooleanField('Remember Me')
  submit = SubmitField('Login')


class QuestionForm(FlaskForm):
  question = TextAreaField('Question',validators=[DataRequired()])
  option1 = StringField('Option1',validators=[DataRequired()])
  option2 = StringField('Option2',validators=[DataRequired()])
  option3 = StringField('Option3',validators=[DataRequired()])
  option4 = StringField('Option4',validators=[DataRequired()])


class FilterForm(FlaskForm):
    asset_class = SelectField('Asset Class', choices=[("All", "All(Assets)"), ("Stock", "Stock"), ("Bond", "Bond"), ("Commodity", "Commodity"), ("Real Estate", "Real Estate")])

    stock_class = SelectField('Stock Class', choices=[("All", "All(Stocks)"), ("All Cap Equities", "All Cap Equities"), ("Large Cap Blend Equities", "Large Cap Blend Equities"), ("Large Cap Blend Equities", "Large Cap Blend Equities"), ("Large Cap Growth Equities", "Large Cap Growth Equities"), ("Large Cap Value Equities", "Large Cap Value Equities"), ("Asia Pacific Equities", "Asia Pacific Equities"), ("China Equities", "China Equities"), ("Emerging Markets Equities", "Emerging Markets Equities"), ("Europe Equities", "Europe Equities"),("Japan Equities", "Japan Equities")])

    bond_class = SelectField('Bond Class', choices=[("All", "All(Bonds)"), ("Total Bond Market", "Total Bond Market"), ("Corporate Bonds", "Corporate Bonds"), ("California Munis", "California Munis"), ("Emerging Markets Bonds", "Emerging Markets Bonds"), ("Government Bonds", "Government Bonds"), ("High Yield Bonds", "High Yield Bonds"), ("Inflation-Protected Bonds", "Inflation-Protected Bonds"), ("International Government Bonds", "International Government Bonds"), ("Inverse Bonds", "Inverse Bonds"),("Leveraged Bonds", "Leveraged Bonds"),("Money Market", "Money Market"),("Mortgage Backed Securities", "Mortgage Backed Securities"),("National Munis", "National Munis"),("New York Munis", "New York Munis"),("Preferred Stock/Convertible Bonds", "Preferred Stock/Convertible Bonds"),("Real Estate", "Real Estate") ])

    commodity_class = SelectField('Commodity Class', choices=[("All", "All(Commodities)"), ("Agricultural Commodities", "Agricultural Commodities"), ("Commodities", "Commodities"), ("Inverse Commodities", "Inverse Commodities"), ("Leveraged Commodities", "Leveraged Commodities"),("Metals", "Metals"),("Oil & Gas", "Oil & Gas"),("Precious Metals", "Precious Metals")])

    real_estate_class = SelectField('Real Estate Class', choices=[("All", "All(Real Estates)"), ("Real Estate", "Real Estate"), ("Global Real Estate", "Global Real Estate"), ("Leveraged Real Estate", "Leveraged Real Estate")])

    submit = SubmitField('Filter')