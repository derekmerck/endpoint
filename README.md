# Python Data Services Library

Derek Merck  
Summer 2020  

Collection of utilities for managing data items and information endpoints with CRUD accessors.

Deriving a class from Hashable, Endpoint, RestAgent, and Serializable creates a highly functional class that can be instantiated from fixed keywords, has access to persistent data (authentication tokens, indexes, etc.), and can connect to specific APIs in order to move or process data.

RestAgent and other utilities are applicable in other domains as well, so this code library is intended to be included in other projects as a git submodule.

```bash
$ git add submodule https://github.com/derekmerck/endpoint /path/to/submodule
```

See submodule documentation at <https://git-scm.com/book/en/v2/Git-Tools-Submodules>

## License

MIT
