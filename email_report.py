import smtplib
################################
#Email Message Module
#By: Angelo Poggi
#
#
#This Module creates a conenction to Gmail using an app password
#uses gmail SMTP
#
#################################

def email_report(from_address,app_password,to_address,error_message):
    stmp_object = smtplib.SMTP('smtp.gmail.com', 587)
    stmp_object.ehlo()
    stmp_object.starttls()
    #App Password
    stmp_object.login(from_address, app_password)
    stmp_object.sendmail(from_address,
                         to_address,
                         '''Subject: Generated from Sync Script\n
                          {}'''.format(error_message))
    stmp_object.quit()

