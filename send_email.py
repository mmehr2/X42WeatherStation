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
    body += "\tWeb Server:\t%s\n" % ws_addr
    body += "\tREST API Server:\t%s\n" % api_addr
    body += "\t\tMeasurement:\t%s/sensors\n" % api_addr
    body += "\t\tLatest data:\t%s/sensors/latest\n" % api_addr
    body += "\t\tLast 15 minutes of data:\t%s/sensors/latest/15\n" % api_addr
    body += "\t\tRelay ON:\tcurl -i -H \"Content-Type: application/json\" -X POST %s/led/0/1\n" % api_addr
    body += "\t\tRelay OFF:\tcurl -i -H \"Content-Type: application/json\" -X POST %s/led/0/0\n" % api_addr
    body += "\t\tTake picture:\tcurl -i -H \"Content-Type: application/json\" -X POST %s/camera/0/3\n" % api_addr
    body += "Sincerely,\n"
    body += "\n"
    body += "The Management\n"
    return body
 
def send_mail(toaddr_list, subject, body):
    global fromaddr, password
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr_list
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr_list, text)
    server.quit()

if __name__=="__main__":
    argc = len(sys.argv)
    nosend = sys.argv[1] if argc>1 else ""
    if nosend == "":
        print "Usage: send_email.py [S|NS]"
        print "  Sends email about ngrok port 80 and 8080 client addresses (different each powerup)."
        print "  Email parameters are stored in the settings database."
        print "  The S flag, if present, will generate and send the email."
        print "  The NS flag, if present, suppresses the actual send for debugging."
        exit(0)
    init()
    wsaddr = dbs.get('Ngrok_Web')
    apiaddr = dbs.get('Ngrok_API')
    body = get_ngrok_notice(wsaddr, apiaddr)
    toaddr = dbs.get('Ngrok_Mailto')
    subject = "New X42WS Addresses"
    print "Email to:", toaddr
    print "Email from:", fromaddr
    print "Email subject:", subject
    print "Email body:"
    print body
    if nosend == 'S' or nosend == 's':
        send_mail(toaddr, subject, body)
