from flask import Flask,request
from python_rave import Rave,RaveExceptions, Misc

rave = Rave("FLWPUBK-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", 
"FLWSECK-XXXXXXXXXXXXXXXXXXXXXXXXXXXX", usingEnv = False)

app = Flask(__name__)

@app.route('/payload', methods=['GET','POST'])

def payload():
# Payload with pin

    payload ={
        "cardno":request.form.get ["cardno"] ,
        "cvv":request.form.get["cvv"],
        "expirymonth":request.form.get["expirymonth"],
        "expiryyear":request.form.get["expiryyear"],
        "amount":request.form.get["amount"],
        "email":request.form.get["email"],
        "phonenumber":request.form.get["phonenumber"],
        "firstname":request.form.get["firstname"],
        "lastname":request.form.get["lastname"],
        "IP":request.form.get["IP"],
        "pin":request.form.get["pin"]
        }   
    try:
        res = rave.Card.charge(payload)

        if res["suggestedAuth"]:
            arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

            if arg == "pin":
                Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
            if arg == "address":
                Misc.updatePayload(res["suggestedAuth"], payload, 
                address= {"billingzip": "07205", "billingcity": "Hillside", 
                "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})

            res = rave.Card.charge(payload)

        if res["validationRequired"]:
            rave.Card.validate(res["flwRef"], "")

            res = rave.Card.verify(res["txRef"])
            print(res["transactionComplete"])

    except RaveExceptions.CardChargeError as e:
        print(e.err["errMsg"])
        print(e.err["flwRef"])

    except RaveExceptions.TransactionValidationError as e:
        print(e.err)
        print(e.err["flwRef"])

    except RaveExceptions.TransactionVerificationError as e:
        print(e.err["errMsg"])
        print(e.err["txRef"])

@app.route('/', methods=['GET', 'POST'])
def index():
    print("Posted data : {}".format(request.form))

    return """
<form method="post">
    Card Number <input type="cardno"> <br/> 
    CVV <input type="cvv" id="idtxt2"><br/> 
   Firstname  <input type="firstname"><br/> 
   Lastname<input type="firstname"><br/> 
    <input type="submit" Value="submit">
</form>
"""

if __name__ == '__main__':
    app.run(port=5000,debug=True)