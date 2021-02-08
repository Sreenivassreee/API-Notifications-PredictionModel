import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred=credentials.Certificate("health-f2069-firebase-adminsdk-vuq11-e5cb19e14a.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

def diabetes(Glucose):
    if Glucose<=140:
        return False
    elif Glucose>200:
        return  "diabetes"
    elif 140<Glucose>200:
        return "Prediabetes"
    else:
        return False

def CHD(bp,heartRate):
    if bp<90 and heartRate<60:
        return True
    else :
        return False

def Hypoxemia(oxygenSaturation):
    if oxygenSaturation==96 or oxygenSaturation==97 or oxygenSaturation==98:
        return False
    else:
        return True

def asthma(oxygenSaturation,bp,respiration):
    pulse=bp
    if (oxygenSaturation==92 or oxygenSaturation==93 or oxygenSaturation==94 or oxygenSaturation==95)and (100>=bp or bp<=125) and (20>=respiration or respiration<=30):
            return False
    else:
        return True

print(diabetes(140))
print(CHD(10,50))
print(Hypoxemia(100))
print(asthma(93,120,25))