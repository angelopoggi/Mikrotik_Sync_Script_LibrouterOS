
################################
#Email Message Module
#By: Angelo Poggi
#
#
#This class is written to make sending emails much easier in the Mikrotik Sync
#Script
################################
import smtplib
import configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def message(user_message) :
    config = configparser.ConfigParser ()

    config.read ( 'config.ini' )
    email_address = config.get ( 'email' , 'email_address' )
    email_password = config.get ( 'email' , 'email_password' )
    send_to = config.get ( 'email' , 'send_to' )

    message = MIMEMultipart("Alternative")
    message["Subject"] = "Mikrotik Sync Script E-Mail"
    message["from"] = email_address
    message["to"] = send_to


    html_message = '''
    <html>
    <body>
    <p>
    This is a system generated message</p>
    <br>
    {}'''.format(user_message)

    content = MIMEText(html_message,"html")
    message.attach(content)

    with smtplib.SMTP('smtp.gmail.com' , 587) as server:

        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(
            email_address, send_to, message.as_string()
        )
        server.quit()





