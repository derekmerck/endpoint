# Python Data Services Library

Derek Merck  
Summer 2020  

Collection of utilities for managing data items and information endpoints with CRUD accessors.

Deriving a class from Hashable, Endpoint, RestAgent, and Serializable creates a highly functional class that can be instantiated from fixed keywords, has access to persistent data (authentication tokens, indexes, etc.), and can connect to specific APIs in order to move or process data.

The drawback is that libsvc imports and wraps multiple external packages that may not be useful in the parent package.

RestAgent and other utilities are applicable in other domains as well, so this code library is intended to be included in other projects as a git submodule.

```bash
$ git add submodule https://github.com/derekmerck/endpoint /path/to/submodule
```

See submodule documentation at <https://git-scm.com/book/en/v2/Git-Tools-Submodules>

When installing a parent package as "editable" with pip (`pip install -e .`), setup seems to only link in the parent package and libsvc needs to be installed separately (i.e., `pip install -e . libsvc/libsvc`)

## License

MIT
