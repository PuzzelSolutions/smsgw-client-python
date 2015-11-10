## Build status

Travis: [![Build Status](https://travis-ci.org/Intelecom/smsgw-client-python.svg)](https://travis-ci.org/Intelecom/smsgw-client-python)

## Pip package ##

Not published yet.

```
pip install itcsmsgw
```

## Example usage ##

```python
import itcsmsgw

// Initialize the client
client = itcsmsgw.Client(baseAddress, serviceId, username, password)

// Single recipient, 0 NOK
messages = [itcsmsgw.Message("+47XXXXXXXX", "This is a test")]

response = client.send(messages)
print(response)
```