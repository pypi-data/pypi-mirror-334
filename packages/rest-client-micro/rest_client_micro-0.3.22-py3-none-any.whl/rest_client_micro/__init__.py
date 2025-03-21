"""
Wrapper for python requests

Invoke manually via:

```python
from rest_client_micro import RESTClient as rc
from rest_client_micro import RESTObject as ro

rest_object = ro()
rest_object.endpoint = 'https://api.example.com/'
rest_object.params = {'key':'value'}
rest_client = rc()
result = rest_client.execute(rest_object)

if result.error is False:
    `print(result.response)
else:
    `print(result.description)
```

Or create an extended class

```python
    class YourAPIClient(BaseRESTAPI):
        ...
        def your_function(self):
            endpoint = "url/path"
            params = {"key":"value"}
            operation = "get"
            self._run_call(endpoint, params, operation, None)

```
"""

from .response import Response
from .basic_auth import BasicAuth
from .rest_client import RESTClient
from .rest_object import RESTObject
from .base_rest_api import BaseRESTAPI

VERSION = (0, 3, 21)

VERSION_STRING = '.'.join(map(str, VERSION))

Response

BasicAuth

RESTClient

RESTObject

BaseRESTAPI
