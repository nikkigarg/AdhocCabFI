import smtplib

sender = 'sender@gmail.com'

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""


def send_email(receivers, message):
    try:
        smtpObj = smtplib.SMTP('gmail.com')
        smtpObj.sendmail(sender, receivers, message)
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")


"""
    <div>
        <div>
        <img src="" alt="Loading..">
        </div>
        <div style="color:'white'">
            Hi {% Name %},
    
            Please click on the button to complete the verification process for xxxxxx@xxxx.xxx:
            <a href="" alt="Error in link">Click here </a>
        </div>
        <div style="color:'gray'">
            If you didn't attempt to verify your email address with our service, delete this email.

            Thanks & Regards,
            Energy Harbors corporation PVT LTD
            Bangalore - India
        </div>
    </div> 
"""
