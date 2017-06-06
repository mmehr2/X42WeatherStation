'''
Send an email to your account advising the proper addresses to call for X42WS demo website and API usage.

'''

import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import settings as dbs

def init():
    global fromaddr, password
    fromaddr = dbs.get('Mail_User')
    password = dbs.get('Mail_Password')

def get_ngrok_notice(ws_addr, api_addr):
    body = "Please use the following addresses for X42WS weather station access:\n"
    body += "\tWeb Server:\thttps://%s.ngrok.io\n" % ws_addr
    body += "\tREST API Server:\thttps://%s.ngrok.io/weather/api\n" % api_addr
    body += "\t\tMeasurement:\thttps://%s.ngrok.io/weather/api/sensors\n" % api_addr
    body += "\t\tLatest data:\thttps://%s.ngrok.io/weather/api/sensors/latest\n" % api_addr
    body += "\t\tLast 15 minutes of data:\thttps://%s.ngrok.io/weather/api/sensors/latest/15\n" % api_addr
    body += "\t\tRelay ON:\tcurl -i -H \"Content-Type: application/json\" -X POST https://%s.ngrok.io/weather/api/led/0/1\n" % api_addr
    body += "\t\tRelay OFF:\tcurl -i -H \"Content-Type: application/json\" -X POST https://%s.ngrok.io/weather/api/led/0/0\n" % api_addr
    body += "\t\tTake picture:\tcurl -i -H \"Content-Type: application/json\" -X POST https://%s.ngrok.io/weather/api/camera/0/3\n" % api_addr
    body += "Sincerely,\n"
    body += "\n"
    body += "The Management\n"
    return body
 
def send_mail(toaddr, subject, body):
    global fromaddr, password
    #fromaddr = "michael.mehr.ucsc@gmail.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

if __name__=="__main__":
    argc = len(sys.argv)
    wscode = sys.argv[1] if argc>1 else ""
    restcode = sys.argv[2] if argc>2 else ""
    nosend = sys.argv[3] if argc>3 else ""
    if wscode == "":
        print "Usage: send_email.py XXXXXX YYYYYY [NS]"
        print "  where XXXXX is the ngrok port 80 client hex code, and"
        print "  where YYYYY is the ngrok port 8080 client hex code."
        print "  The NS flag, if present, suppresses the actual send for debugging."
        exit(0)
    init()
    body = get_ngrok_notice(wscode, restcode)
    toaddr = "mmehr2@yahoo.com, mmehr2x-dev@yahoo.com"
    subject = "New X42WS Addresses"
    print "Email to:", toaddr
    print "Email from:", fromaddr
    print "Email subject:", subject
    print "Email body:"
    print body
    if nosend == "":
        send_mail(toaddr, subject, body)
