from libsvc.utils import EmailAddress, EmailJinjafier


def test_mail_jinjafier():

    J = EmailJinjafier()

    sender    = EmailAddress("Noone Sender",   "noone-says@nowhere.com")
    recipient = EmailAddress("Noone Receiver", "noone-hears@nowhere.com")

    data = {"dog": "cat", "yellow": "blue"}
    m = J.render_email(data, recipient, sender)
    print(m)

    assert str(m) == """\
To: Noone Receiver <noone-hears@nowhere.com>
From: Noone Sender <noone-says@nowhere.com>
Subject: Automatic Notification
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0

{'dog': 'cat', 'yellow': 'blue'}
"""


if __name__ == "__main__":
    test_mail_jinjafier()
