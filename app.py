from flask import render_template, request, flash, redirect, Flask
from forms import HouseForms, train_flask
import pickle
import dill
import pandas as pd
import os.path
import numpy as np
import pandas as pd
# from flask_wtf.csrf import CSRFProtect
# from config import SECRET_KEY

app = Flask(__name__)

# csrf = CSRFProtect()

# def create_app():
#     app = Flask(__name__)
#     csrf.init_app(app)
# create_app()

# current_path = os.path.split(os.path.abspath(__file__))[0]
# with open(os.path.join(current_path,"ridge_model.pkl"),"rb")as f:
#     model = pickle.load(f)
ridge_model = open("ridge_model.pkl","rb")
ridge = pickle.load(ridge_model)

def default_none(input_data):
    if input_data != None:
        return input_data
    else:
        return None

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/map")
def mapper():
    return render_template("orangemap.html")

@app.route("/priceForm")
def root():
    # global model
    global ridge
    form = HouseForms(csrf_enabled=False)  
    return render_template("index1.html",
    title = "House Price Prediction",
    form = form)
#send info from fron end to back end : post.... get: requesting data
@app.route("/calculate", methods = ["POST"])
def index():
    # global model
    global ridge
    form = HouseForms(csrf_enabled=False)
    # if (request.method == "POST") and (form.validate()):
    
    user_dictionary={
        'zip':[str(int(form.zipcode.data))],
        'type':[str(form.buildingType.data)],
        'beds':[float(form.bedrooms.data)],
        'baths':[float(form.bathrooms.data)],
        'sqrft':[float(form.Squarefeet.data)],
        'lot':[float(form.lotsize.data)],
        '$/sqrft':[float(form.per_sqrft.data)]}
    
    user_df=pd.DataFrame(user_dictionary)
    user_df_fit=pd.get_dummies(user_df,columns=['zip','type'])

    n=train_flask()

    for i in n.columns:
        if i in user_df_fit.columns:
            pass
        else:
            user_df_fit[i]=0

    print(user_df_fit)

    # user_df_fit=user_df_fit.set_index('beds')
    
    # prediction = np.expm1(model.predict(user_df_fit))
    prediction = int(np.expm1(ridge.predict(user_df_fit)))

    # prediction=ridge.predict(user_df_fit)

    # prediction=model.predict(user_df_fit)
    # p = round(prediction[0],2)

    print([str(int(form.zipcode.data))])
    print([str(form.buildingType.data)])
    print([float(form.bedrooms.data)])
    print([float(form.bathrooms.data)])
    print([float(form.Squarefeet.data)])
    print([float(form.lotsize.data)])
    print([float(form.per_sqrft.data)])
    print(n.head())

    print(prediction)
    # else:
    #     prediction = "N/A"
    #     print("what")
    
    return render_template("index1.html", title = "House Price Prediction", form = form, prediction = '${:,.2f}'.format(prediction))


                           


if __name__ == ("__main__"):
    app.run(debug=True,port=7500)