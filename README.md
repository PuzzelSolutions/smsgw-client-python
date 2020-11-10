## Build status

Travis: [![Build Status](https://travis-ci.org/Intelecom/smsgw-client-python.svg)](https://travis-ci.org/Intelecom/smsgw-client-python)

## Pip package ##

```
pip install itcsmsgwclient
```

## Example usage ##

```python
from itcsmsgwclient import itcsmsgwclient

// Initialize the client
client = itcsmsgwclient.Client(baseAddress, serviceId, username, password)

// Single recipient, 0 NOK
messages = [itcsmsgwclient.Message("+47XXXXXXXX", "This is a test")]

response = client.send(messages)
print(response)
```
