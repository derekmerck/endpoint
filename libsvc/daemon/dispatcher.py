"""
Translate messages to channels into notification emails using
redis pubsub framework
"""

import typing as typ
import logging
import pickle
import time
from email.message import EmailMessage
from redis import Redis
import attr
from ..utils import EmailAddress, EmailMessenger, EmailJinjafier
from ..persistence import RedisPersistenceBackend

DISPATCHER_POLLING_DELAY = 2.0

DEFAULT_MSG_TEMPL = """\
recipient:
  {{ recipient | string }}
  
sender:
  {{ sender | string }}
  
content:
  {{ data | pprint }}
"""


@attr.s(auto_attribs=True)
class Subscriber(EmailAddress):
    institution: str = None
    p: Redis.pubsub = None


@attr.s(auto_attribs=True)
class Dispatcher(RedisPersistenceBackend):

    db = 1  # Uses 0 for regular key/values
    namespace: str = "notify"

    smtp_host: str = None
    email_messenger: EmailMessenger = attr.ib()
    @email_messenger.default
    def mk_email_messenger(self) -> EmailMessenger:
        return EmailMessenger(host=self.smtp_host)

    default_msg_templ: str = DEFAULT_MSG_TEMPL
    default_subj_templ: str = "Automatic Notification"
    default_sender: EmailAddress = EmailAddress("Notifictions", "no-reply@example.com")
    email_jinjafier: EmailJinjafier = attr.ib(init=False)
    @email_jinjafier.default
    def mk_email_jinjafier(self) -> EmailJinjafier:
        return EmailJinjafier(default_templ=self.default_msg_templ,
                              default_subj_templ=self.default_subj_templ)

    subscribers: typ.List[Subscriber] = attr.ib(factory=list)

    def mk_subscriber(self,
                      name: str,
                      email: str,
                      institution: str,
                      channels: typ.List[str]) -> Subscriber:
        p = self.gateway.pubsub()
        for c in channels:
            # glob patterns - *,?,[] are legal
            if c.find("*") > 0 or c.find("?") > 0 or c.find("[") > 0:
                p.psubscribe(self.t(c))
            else:
                p.subscribe(self.t(c))
        s = Subscriber(name, email, institution, p)
        return s

    def add_subscriber(self,
                      name: str,
                      email: str,
                      institution: str,
                      channels: typ.List[str]):
        s = self.mk_subscriber(name, email, institution, channels)
        self.subscribers.append(s)

    def submit_message(self, channels: typ.List, message_data: typ.Dict):
        m = pickle.dumps(message_data)
        for c in channels:
            self.gateway.publish(self.t(c), m)

    def get_messages(self, s: Subscriber) -> typ.List:
        res = []
        msg = True
        while msg:
            msg = s.p.get_message()
            if msg and msg.get("data"):
                try:
                    found_message_data = pickle.loads(msg.get("data"))
                    res.append(found_message_data)
                except TypeError as e:
                    # Unpickle failed, it's a startup message or something
                    pass
        return res

    def handle_messages(self, dry_run=False) -> typ.List[EmailMessage]:
        res = []
        for recipient in self.subscribers:
            messages = self.get_messages(recipient)  # Ony returns unpickled entries
            for message_data in messages:
                msg_templ  = message_data.get("msg_templ") or self.default_msg_templ
                subj_templ = message_data.get("subj_templ") or self.default_subj_templ
                sender     = message_data.get("sender") or self.default_sender
                email_msg  = self.email_jinjafier.render_email(message_data,
                                                               recipient=recipient,
                                                               sender=sender,
                                                               msg_templ=msg_templ,
                                                               subj_templ=subj_templ)
                if not dry_run:
                   self.email_messenger.send( email_msg )
                res.append(email_msg)
        return res

    def run(self):
        while True:
            self.handle_messages()
            time.sleep(DISPATCHER_POLLING_DELAY)
