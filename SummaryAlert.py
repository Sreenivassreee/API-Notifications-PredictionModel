
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
message['Subject'] = 'Your Daily Summary'

account_sid = 'AC15bfbba323ed72afb597c40f7ea81ac8'
auth_token = 'c4c14c6080f82c237148c8ca72766b49'

firstTime=""
first=""
last=""
lastTime=""
middle1=""
middle1Time=""
middle2=""
middle2Time=""

def getEachPersonData(email,mobile):
    EachUserData=db.collection(u'Users').document(email).collection(u'EachPara').document(u'EachPara').get().to_dict()
    EachUserNotifications=db.collection(u'Users').document(email).collection(u'EachPara').document(u'Notifications').get().to_dict()
    k=EachUserNotifications['sms']
    print(k)
    print("EachUserData \n")

    data=EachUserData["EachPara"]
    first = data[0]
    firstTime = data[0]["UpdateTime"]
    last = data[len(data) - 1]
    lastTime = data[len(data) - 1]["UpdateTime"]
    middle1 = data[int(len(data) / 4)]
    middle1Time = data[int(len(data) / 4)]["UpdateTime"]
    middle2 = data[int(len(data) / 2)]
    middle2Time = data[int(len(data) / 2)]["UpdateTime"]

    finalMessage = "\n" + "Day starting report \n Time: " + firstTime + "\n " + str(
        first) + "\n\n\n  report 2 \n Time: " + middle1Time + "\n" + str(
        middle1) + "\n\n\n  report 3 \n Time: " + middle2Time + "\n" + str(
        middle2) + "\n\nEvening report  \n Time: " + lastTime + "\n" + str(last)

    if(EachUserNotifications['mail']):
        sendMail(email,finalMessage)
    if(EachUserNotifications['whatsapp']):
        print(EachUserNotifications['whatsapp'])
        sendWhatsApp(mobile, finalMessage)
    if(EachUserNotifications['sms']):
        print(EachUserNotifications['sms'])
        sendsms(mobile,finalMessage)


    time.sleep(3)

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
def sendWhatsApp(mobile,finalMessage):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body='Summary from TCS Health \n'+finalMessage,
        from_='whatsapp:+14155238886',
        to='whatsapp:+91'+mobile
    )
    print('whatsapp message Send to '+ email)

def sendMail(receiver_address,finalMessage):

    mail_content =finalMessage;
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()

    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail is Send to '+ email)



for i in doc:
    a = i.to_dict()
    email = a['email']
    name=a["name"]
    age=a["age"]
    mobile=a["mobile"]

    getEachPersonData(email,mobile);

