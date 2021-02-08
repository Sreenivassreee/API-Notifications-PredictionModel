import firebase_admin
import time
import random
from time import strftime
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore import ArrayUnion


cred=credentials.Certificate("health-f2069-firebase-adminsdk-vuq11-e5cb19e14a.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
while True:
    dc = db.collection('Users').get()
    for i in dc:
                    # print(i)
                    a=i.to_dict()
                    b=a['email']
                    doc_ref = db.collection(u'Users').document(b).collection(u'EachPara').document(u'EachPara')
                    bp=random.randint(89,125) #90-120
                    Body_Tempatature=random.randint(95,100) #98 - 97
                    Respiration=random.randint(10,18) #12-16
                    Glucose=random.randint(135,210)  # less 140 to 200
                    Heart_Rate=random.randint(58,84)  # 60-80
                    Oxygen_Saturation=random.randint(93,105)  #95 -100
                    Electro_Cardiogram=random.randint(55,110)  #60-100
                    timeUpdate=strftime("%d/%m/%Y %HH :%MM :%SS")

                    print("Sent to :" + b)
                    doc_ref.set({
          'EachPara': ArrayUnion([
                    {
                                        u"bp":u""+str(bp),
                                        u"Body_Tempatature": u""+str(Body_Tempatature),
                                        u"Respiration":u""+str(Respiration),
                                        u"Glucose":u""+str(Glucose),
                                        u"Heart_Rate":u""+str(Heart_Rate),
                                        u"Oxygen_Saturation":u""+str(Oxygen_Saturation),
                                        u"Electro_Cardiogram":u""+str(Electro_Cardiogram),
                                        u'UpdateTime':u""+str(timeUpdate)
                                        
                              }

                    ]
                    )
                    },merge=True,
                    )
    time.sleep(5)
                    

