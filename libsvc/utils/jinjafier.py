import typing as typ
from functools import partial
from email.message import EmailMessage
import attr
from jinja2 import Environment, BaseLoader
from .smtp import EmailAddress, mk_email


@attr.s(auto_attribs=True)
class Jinjafier(object):
    jinja_env: Environment = attr.ib(factory=partial(Environment, loader=BaseLoader()))
    default_templ: str = "{{ data | pprint }}"

    def render(self, data: typ.Dict, templ: str = None, **kwargs) -> str:
        templ = templ or self.default_templ
        jtemplate = self.jinja_env.from_string(templ)
        res = jtemplate.render(data)
        return res


@attr.s(auto_attribs=True)
class EmailJinjafier(Jinjafier):
    default_subj_templ: str = "Automatic Notification"

    def render_email(self,
                     data: typ.Dict,
                     recipient: EmailAddress,
                     sender: EmailAddress,
                     msg_templ: str = None,
                     subj_templ: str = None) -> EmailMessage:
        # Get content
        _data = {"data": data, "recipient": recipient, "sender": sender}
        content = self.render(_data, msg_templ)

        # Get subject
        subj_templ = subj_templ or self.default_subj_templ
        subject = self.render(_data, subj_templ)

        # print(subject)
        # print(content)

        email_msg = mk_email(recipient, sender, subject, content)
        return email_msg
