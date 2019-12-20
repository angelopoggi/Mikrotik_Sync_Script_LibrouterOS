
################################
#Email Message Module
#By: Angelo Poggi
#
#
#This class is written to make sending emails much easier int he Mikrotik Sync
#Script
#################################
import smtplib

def message(error_message) :
    stmp_object = smtplib.SMTP ( 'smtp.gmail.com' , 587 )
    stmp_object.ehlo ()
    stmp_object.starttls ()
    # App Password
    stmp_object.login ('angelo.poggi@webair.com', 'udodumoavliwfmrp')
    stmp_object.sendmail ( 'angelo.poggi@webair.com' ,
                           'Rickie.Harripersaud@webair.com' ,
                           '''Subject: Sync Script Error Report\n
                          {}'''.format ( error_message ) )


    stmp_object.quit ()

