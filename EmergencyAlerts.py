import firebase_admin
import time
from firebase_admin import credentials
from firebase_admin import firestore
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
import clx.xms
import requests

cred=credentials.Certificate("health-f2069-firebase-adminsdk-vuq11-e5cb19e14a.json")
firebase_admin.initialize_app(cred)
db=firestore.client()
doc=db.collection('Users').get()

sender_address = 'inframind2020@gmail.com'
sender_pass = 'acqjnigebufdrkra'
message = MIMEMultipart()
message['From'] = sender_address

message['Subject'] = 'Emergency Notifications'

account_sid = 'AC15bfbba323ed72afb597c40f7ea81ac8'
auth_token = 'c4c14c6080f82c237148c8ca72766b49'

UserParameters=""
Time=""

def get_each_person_data(email,mobile):
    print(email)
    each_user_data=db.collection(u'Users').document(email).collection(u'EachPara').document(u'EachPara').get().to_dict()
    each_user_notifications=db.collection(u'Users').document(email).collection(u'EachPara').document(u'Notifications').get().to_dict()
    k=each_user_notifications['sms']
    print(k)

    print("Emergency Alert \n")
    data=each_user_data["EachPara"]
    last = data[len(data) - 1]
    last_time = data[len(data) - 1]["UpdateTime"]
    bp =data[len(data) - 1]["bp"]
    body_tempatature =data[len(data) - 1]["Body_Tempatature"]
    respiration = data[len(data) - 1]["Respiration"]
    glucose = data[len(data) - 1]["Glucose"]
    heart_rate = data[len(data) - 1]["Heart_Rate"]
    oxygen_saturation = data[len(data) - 1]["Oxygen_Saturation"]
    electro_cardiogram = data[len(data) - 1]["Electro_Cardiogram"]
    time_update =data[len(data) - 1]["UpdateTime"]

    def diabetes(glucose):
        if glucose <= 140:
            return "Safe"
        elif glucose > 200:
            return "UnSafe"
        elif 140 < glucose > 200:
            return "UnSafe"
        else:
            return "Safe"

    def chd(bp, heart_rate):
        if bp < 90 and heart_rate < 60:
            return "UnSafe"
        else:
            return "Safe"

    def hypoxemia(oxygen_saturation):
        if oxygen_saturation == 96 or oxygen_saturation == 97 or oxygen_saturation == 98:
            return "UnSafe"
        else:
            return "Safe"

    def asthma(oxygen_saturation, bp, respiration):
        pulse = bp
        if (oxygen_saturation == 92 or oxygen_saturation == 93 or oxygen_saturation == 94 or oxygen_saturation == 95) and (
                100 >= bp or bp <= 125) and (20 >= respiration or respiration <= 30):
            return "Safe"
        else:
            return "UnSafe"

    def set_data_to_firebase(email,diabaties,chd,hypoxemia,asthma):
        if diabaties=="Safe":
            dia=False
        else :
            dia=True
        if chd=="Safe":
            chd_status=False
        else :
            chd_status=True

        if hypoxemia=="Safe":
            hypoxemia_status=False
        else :
            hypoxemia_status=True
        if asthma=="Safe":
            asthma_status=False
        else :
            asthma_status=True
        print(chd)
        print(hypoxemia)
        print(asthma)
        docData = db.collection(u'Users').document(email).collection(u'EachPara').document(u'diseases')
        docData.set({
            "CHD": chd_status,
            "asthma": asthma_status,
            "hypoxemia": hypoxemia_status,
            "diabetes": dia
        })

    diabetes_status= diabetes(int(glucose))
    chd_status=chd(int(bp), int(heart_rate))
    hypoxemia_status=hypoxemia(int(oxygen_saturation))
    asthma_status= asthma(oxygen_saturation, bp, respiration)

    finalMessage ="DiabetesStatus :: "+diabetes_status +"\n\n"+"CHDStatus :: "+ chd_status +"\n\n"+"HypoxemiaStatus :: "+hypoxemia_status+"\n\n"+"AsthmaStatus : : "+asthma_status+"\n\n"+"Time Update :: "+time_update
    print(finalMessage)
    if(each_user_notifications['mail']):
        if diabetes_status=="UnSafe" or chd_status =="UnSafe" or hypoxemia_status=="UnSafe" or asthma_status=="UnSafe":
            print("Triggering")
            send_mail(email,finalMessage)
    if(each_user_notifications['whatsapp']):
        if diabetes_status=="UnSafe" or chd_status =="UnSafe" or hypoxemia_status=="UnSafe" or asthma_status=="UnSafe" :
            send_whats_app(mobile, finalMessage)
    if(each_user_notifications['sms']):
        if(diabetes_status=="UnSafe" or chd_status =="UnSafe" or hypoxemia_status=="UnSafe" or asthma_status=="UnSafe"):
            sendsms(mobile,finalMessage)


    time.sleep(3)
    set_data_to_firebase(email,diabetes_status,chd_status,hypoxemia_status,asthma_status)


def sendsms(mobile,finalMessage):
    client = clx.xms.Client(service_plan_id='5acc72a3624e429683617749e30ff7fd',
                            token='ac1135063e804837a570d3fb9fd60095')
    create = clx.xms.api.MtBatchTextSmsCreate()
    create.sender = '447537404817'
    create.recipients = {'91'+mobile}

    create.body = finalMessage
    print('sms is Send to '+ email)


    try:
        batch = client.create_batch(create)
    except (requests.exceptions.RequestException,
            clx.xms.exceptions.ApiException) as ex:
        print('Failed to communicate with XMS: %s' % str(ex))
def send_whats_app(mobile,finalMessage):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Summary from TCS Health \n'+finalMessage,
        from_='whatsapp:+14155238886',
        to='whatsapp:+91'+mobile
    )
    print('whatsapp message Send to '+ email)

def send_mail(receiver_address,finalMessage):

    mail_content =finalMessage;
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail is Send to '+ email)





for i in doc:
    # print(i)
    a = i.to_dict()
    email = a['email']
    name=a["name"]
    age=a["age"]
    mobile=a["mobile"]

    get_each_person_data(email,mobile);

