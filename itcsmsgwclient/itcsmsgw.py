import jsonpickle
import requests

class _Request:
    def __init__(self, serviceId, username, password):
        self.serviceId = serviceId
        self.username = username
        self.password = password
        self.message = []

class GatewayError(Exception):
    def __init__(self, message):
        self.message = message

class Message:
    price = None
    clientReference = None
    settings = None

    def __init__(self, recipient, content):
        self.recipient = recipient
        self.content = content

class MessageOptions:
    priority = None 
    validity = None 
    differentiator = None 
    age = None 
    newSession = None 
    sessionId = None 
    invoiceNode = None 
    autoDetectEncoding = None 
    safeRemoveNonGsmCharacters = None 
    originatorSettings = None 
    gasSettings = None
    sendWindow = None
    parameter = None

class OriginatorSettings:
    def __init__(self, originatorType, originator):
        self.originatorType = originatorType
        self.originator = originator

class GasSettings:
    description = None

    def __init__(self, serviceCode):
        self.serviceCode = serviceCode

class Client:
    def __init__(self, baseAddress, serviceId, username, password):
        self.__baseAddress = baseAddress
        self.__serviceId = serviceId
        self.__username = username
        self.__password = password

    def send(self, messages):
        url = self.__baseAddress + "/sendMessages"
        headers = {"Accept": "application/json", "Content-type": "application/json"}
        request = _Request(self.__serviceId, self.__username, self.__password)
        for message in messages:
            request.message.append(message)
        data = jsonpickle.encode(request, unpicklable=False)
        response = requests.post(url, data, headers=headers)
        if response.status_code != 200:
            raise GatewayError("Gateway status code:" + str(response.status_code))
        return jsonpickle.decode(response.text)