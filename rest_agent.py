import typing as typ
from pprint import pprint
from urllib.parse import urljoin
from json import JSONDecodeError
import attr
import requests
from smu7.utils.persistence import ShelfMixin


# REST agent framework that wraps a Requests session object
@attr.s(auto_attribs=True)
class RestAgent(ShelfMixin):
    url: str = None
    username: str = None
    password: str = None
    clear_session: bool  = False  # Ignore shelved session, if it exists
    shelve_session: bool = False  # Preserve login session for later
    shelf_ns: str = "rest_ep"
    dry_run: bool = False

    session: requests.Session = attr.ib(repr=False, init=False, default=None)

    def setup_session(self):
        # Check for existing credentials and use them
        # if they are available on the shelf
        if not self.clear_session and "session" in self.shelf:
            session = self.shelf["session"]
        else:
            session = self.setup_new_session()
            if self.shelve_session:
                self.shelf["session"] = session
        return session

    # Can't setup session with a default -- vars in derived classes will
    # not be available yet, similarly, shelf doesn't exist when this happens
    def __attrs_post_init__(self):
        self.shelf = ShelfMixin.setup_shelf(self)  # Otherwise shelf doesn't exist yet
        self.session = self.setup_session()

    def setup_new_session(self) -> requests.Session:
        raise NotImplemented

    def handle_errors(self, r: requests.Response):
        print(r.status_code)
        print(r.content)
        raise ConnectionError

    def request(self,
                resource: str,
                method: str = "get",
                params: typ.Dict = None,
                headers: typ.Dict = None,
                data: typ.Any = None,
                json: typ.Dict = None,
                files: typ.Dict = None,
                inspect: bool = False,
                verbose: bool = False,
                decoder: typ.Callable = None) -> typ.Union[typ.Dict, str, None]:

        url = urljoin(self.url, resource)
        req = requests.Request(method, url, params=params, headers=headers,
                               data=data, json=json, files=files)
        req_: requests.PreparedRequest = self.session.prepare_request(req)

        if inspect:
            pprint(req_.headers)
            print(req_.body)

        if self.dry_run:
            return

        r = self.session.send(req_)
        if r.status_code != 200:
            self.handle_errors(r)

        if verbose:
            pprint(r.headers)
            if r.cookies.get_dict():
                pprint(r.cookies.get_dict())
            print(r.content)

        try:
            if decoder:
                return decoder(r)
            return r.json()
        except JSONDecodeError:
            return str(r.content)
