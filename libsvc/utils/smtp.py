import smtplib
from email.message import EmailMessage
import attr


@attr.s(auto_attribs=True)
class EmailAddress(object):
    name: str = None
    email: str = None

    def __str__(self):
        return f"{self.name} <{self.email}>"


def mk_email(recipient: EmailAddress,
             sender: EmailAddress,
             subject: str,
             content: str) -> EmailMessage:
    email_msg = EmailMessage()
    email_msg['To'] = str(recipient)
    email_msg['From'] = str(sender)
    email_msg['Subject'] = subject
    email_msg.set_content(content)
    return email_msg


@attr.s(auto_attribs=True)
class EmailMessenger(object):
    host: str = None

    def send(self, msg: EmailMessage):
        s = smtplib.SMTP(self.host)
        s.send_message(msg)
        s.quit()
