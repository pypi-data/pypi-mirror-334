# RestClientMicro

Run REST calls

# Usage

```python
from rest_client_micro import RESTClient as rc
from rest_client_micro import RESTObject as ro

rest_object = ro()
rest_object.endpoint = 'https://api.scryfall.com/cards/named'
rest_object.params = {'exact':'Overgrown Tomb'}
rest_client = rc()
result = rest_client.execute(rest_object)
print(result)
```

e.g

runs a Magic the Gathering card search against the exact name 'Overgrown Tomb'.

Returns the content of the response

```python
{
    'error': False,
    'response':"{\"object\":\"card\",\"id\":\"eff1f52c-5c43-4260-aaa0-6920846a191c\",\"oracle_id\":\"975ec9a3-6f20-4177-8211-82526e092538\",\"multiverse_ids\":[453003],\"mtgo_id\":69919,\"arena_id\":68734,\"tcgplayer_id\":175196,\"cardmarket_id\":363554,\"name\":\"Overgrown Tomb\",.....ll\"}}"
}
```

Or an object describing an error

```python
{
    "error":True,
    "description":"Resource not found"
    }
or
{
    "error":True,
    "description":"Unterminated string starting at: line 1 column 14 (char 13)"
}
```

## Auth

```python
from rest_client_micro import RESTClient as rc, RESTObject as ro, BasicAuth as ba

rest_object = ro()
rest_object.endpoint = 'http://localhost:3876/auth'
rest_object.params = ''
rest_object.basic_auth = ba('user', 'secretpass')
rest_client = rc()
result = rest_client.execute(config=rest_object)
```

# Build

```bash
python -m build
python -m twine upload dist/*
```
