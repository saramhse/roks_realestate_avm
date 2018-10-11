from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired,optional,NumberRange
import pickle
import numpy as np
import pandas as pd

building_type = [("sfr","Single Family Residence"),('condo', 'Condominium'),('thr', 'Townhome Residence'),('mfr', 'Multifamily Residence') ]
bedrooms_choice = [(1,1),(2,2),(3,3),(4,4),(5,5)]
bathrooms_choice = [(1,1),(2,2),(3,3),(4,4)]

class HouseForms(FlaskForm):
    buildingType = SelectField('Type of House', choices = building_type)
    bedrooms  = SelectField('Number of Bedrooms', choices=bedrooms_choice)
    bathrooms= SelectField('Number of Bathrooms', choices=bathrooms_choice)
    Squarefeet = FloatField("Squarefeet", validators = [DataRequired()])
    zipcode = FloatField("Zipcode", validators = [DataRequired()])
    lotsize = FloatField("Lot Size", validators = [DataRequired()])
    per_sqrft = FloatField("$ per Squarefeet", validators = [DataRequired()])
    yearBuilt = FloatField("Year Built", validators = [DataRequired()])




property_type_choices = [('sfr', 'Single Family Residence'),
                         ('condo', 'Condominium'),
                         ('thr', 'Townhome Residence'),
                         ('mfr', 'Multifamily Residence')
                         ]

def train_flask():
    infile=open('data.pk1','rb')
    train=pickle.load(infile)
    
    cols=['zip','type','beds','baths','sqrft','lot','$/sqrft']
    x=train[cols]
    
    train['price']=np.log1p(train['price'])
    train['$/sqrft']=np.log1p(train['$/sqrft'])
    train['sqrft']=np.log1p(train['sqrft'])
    train['lot']=np.log1p(train['lot'])

    x=pd.get_dummies(x,columns=['zip','type'])

    return x

n=train_flask()
print(n)
# class MortgageInputForm(FlaskForm):
#     loan_amount = FloatField('Originated Amount ($)', validators=[DataRequired()])
#     buyer_credit = FloatField('Buyer\'s credit score (Valid from 500 to 850)', validators=[DataRequired()])
#     cobuyer_credit = FloatField('Cobuyer\'s credit score', validators=[optional(),NumberRange(500.0,850.0,"Check credit score")])
#     loan_to_value = FloatField('Originated Loan to Value ratio (%)',validators=[DataRequired()])
#     debt_to_income = FloatField('Debt to Income Ratio (%)', validators=[DataRequired()])
#     loan_state = SelectField('State', choices=state_choices)
#     loan_purpose = SelectField('Loan Purpose',
#                                choices=loan_purpose_choices)
#     property_type = SelectField('Property Type',
#                                 choices=property_type_choices)
#     occupancy_type = SelectField('Occupancy Type',
#                                  choices=occupancies_type_choices)
