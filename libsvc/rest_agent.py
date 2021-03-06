import typing as typ
import time
from enum import Enum
from pprint import pprint
from urllib.parse import urljoin
from json import JSONDecodeError
import attr
import requests
from libsvc.persistence import ShelfMixin

MAX_CONNECTION_ATTEMPTS = 10

class RequestType(Enum):
    GET = "get"
    PUT = "put"
    POST = "post"
    DELETE = "delete"


RTy = RequestType


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

    def setup_session(self) -> requests.Session:
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

    # Trivial session initialization, overload this to setup a more complicated
    # session with auth
    def setup_new_session(self) -> requests.Session:
        session = requests.Session()
        return session

    def handle_errors(self, r: requests.Response):
        print(r.status_code)
        print(r.content)
        raise ConnectionError

    def request(self,
                resource: str,
                method: typ.Union[RequestType, str] = "get",
                params: typ.Dict = None,
                headers: typ.Dict = None,
                data: typ.Any = None,
                json: typ.Dict = None,
                files: typ.Dict = None,
                inspect: bool = False,
                verbose: bool = False,
                ignore_errors: bool = False,
                decoder: typ.Callable = None) -> typ.Union[typ.Dict, typ.List, str, None]:

        url = urljoin(self.url, resource)

        if isinstance(method, RequestType):
            method = method.value

        req = requests.Request(method, url, params=params, headers=headers,
                               data=data, json=json, files=files)
        req_: requests.PreparedRequest = self.session.prepare_request(req)

        if inspect:
            print(url)
            print(method)
            pprint(req_.headers)
            print(req_.body)

        if self.dry_run:
            return

        for attempt in range(MAX_CONNECTION_ATTEMPTS+1):
            try:
                r = self.session.send(req_)
            except ConnectionError as e:
                print(f"-->Connection failed! (attempt {attempt})")
                if attempt == MAX_CONNECTION_ATTEMPTS:  # Last loop
                    print("-->Could not connect")
                    raise e
                time.sleep(1.0)  # Give the connection a second to cool down
                continue
            break

        if r.status_code != 200:
            if not ignore_errors:
                self.handle_errors(r)
            else:
                return

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
            # Don't cast this to string -- it messes up binary data responses
            return r.content
