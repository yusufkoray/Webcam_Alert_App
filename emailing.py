import smtplib
from email.message import  EmailMessage
import imghdr
import os

APP_PASSWORD=os.getenv("SON")

SENDER="ykcspor@gmail.com"
RECEIVER="ykcspor@gmail.com"


def send_email(image_path=None):
    email_message = EmailMessage()
    email_message["Subject"] = "New object is seemed!"
    email_message.set_content("Hey, we just saw a new object!")
    if image_path is not None:
        with open(image_path,'rb') as file:
            content=file.read()

        email_message.add_attachment(content,maintype="image",subtype=imghdr.what(None,content))

    gmail=smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,APP_PASSWORD)
    gmail.sendmail(SENDER,RECEIVER,email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email()

