from flask import Flask, request, escape, render_template
import pickle 
import numpy as np

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template("index.html")


@app.route('/predict', methods = ["GET","POST"])
def predict():
    if request.method ==  'POST': 
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        # if request.form['credit'] != '-- select Self_Employed --':
        credit = request.form['credit']
        area = request.form['area']
        ApplicantIncome = request.form['ApplicantIncome']
        CoapplicantIncome = request.form['CoapplicantIncome']
        LoanAmount = request.form['LoanAmount']
        Loan_Amount_Term = request.form['Loan_Amount_Term']

        if not gender or not married or not dependents or not education or not employed or not credit or not area or not ApplicantIncome or not CoapplicantIncome or not LoanAmount or not Loan_Amount_Term:
            error_statement = "All Form Fields are Required"
            return render_template("prediction.html", prediction_text=error_statement)
        credit = float(request.form['credit'])
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])    

        # gender
        if (gender == "Male"):
            gender =1
        else:
            gender=0
        
        # married
        if(married=="Yes"):
            married= 1
        else:
            married=0

        # dependents
        if(dependents=='1'):
            dependents =1
        elif(dependents == '2'):
            dependents = 2
        elif(dependents=="3+"):
            dependents = 3
        else:
            dependents= 0
            
        # education
        if (education=="Not Graduate"):
            education=1
        else:
            education=0

        # employed
        if (employed == "Yes"):
            employed=1
        else:
            employed=0

        # property area

        if(area=="Semiurban"):
            area = 1
        elif(area=="Urban"):
            area=2
        else:
            area=0
        
        ApplicantIncomelog = np.log(ApplicantIncome)
        Totalincomelog = np.log(ApplicantIncome+CoapplicantIncome)
        LoanAmountlog = np.log(LoanAmount)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term)

        prediction = model.predict([[gender, married, dependents, education, employed, credit,area, ApplicantIncomelog, LoanAmountlog, Loan_Amount_Termlog, Totalincomelog ]])

        # print(prediction)

        if(prediction=='0'):
            prediction="No"
        else:
            prediction="Yes"


        return render_template("prediction.html", prediction_text="loan status is {}".format(prediction))

    else:
        return render_template("prediction.html")



if __name__== "__main__":
    app.run(debug=True)

