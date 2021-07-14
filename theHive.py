import requests
import sys
import json
import time
import uuid
from thehive4py.api import TheHiveApi
from thehive4py.exceptions import AlertException
from thehive4py.models import Alert, AlertArtifact, CustomFieldHelper, Tlp

THEHIVE_URL = 'https://so-rc1.yourict.net/thehive'
THEHIVE_API_KEY = ''
VERIFY_CERT = False
ORGANISATION = "Securityonion"

api = TheHiveApi(THEHIVE_URL, THEHIVE_API_KEY, proxies=PROXIES, cert=VERIFY_CERT, organisation=ORGANISATION, version=4)

# Prepare observables
inmemory_file = open('sample.txt', 'rb')
artifacts = [
    AlertArtifact(dataType='ip', data='8.8.8.8',sighted=True, ioc=True,tlp=Tlp.GREEN.value),
    AlertArtifact(dataType='domain', data='google.com',sighted=True, ioc=True, tlp=Tlp.GREEN.value),
    AlertArtifact(dataType='file', data=(inmemory_file, 'sample.txt'), sighted=False, ioc=False, tlp=Tlp.GREEN.value)
]

# Prepare custom fields
customFields = CustomFieldHelper() \
    .add_string('business-unit', 'HR') \
    .add_string('business-impact', 'HIGH') \
    .add_date('occur-date', int(time.time())*1000) \
    .add_number('cvss', 6) \
    .build()

# Prepare the sample Alert
sourceRef = str(uuid.uuid4())[0:6]
alert = Alert(title='New Alert',
              tlp=3,
              tags=['TheHive4Py', 'monops',"iocs"],
              description='IOC hits in the last 1 day',
              type='external',
              source='cert.be',
              sourceRef=sourceRef,
              artifacts=artifacts,
              customFields=customFields
              )

# Create the alert
try:
    response = api.create_alert(alert)

    # Print the JSON response
    print(json.dumps(response.json(), indent=4, sort_keys=True))

except AlertException as e:
    print("Alert create error: {}".format(e))

inmemory_file.close()

# Exit the program
sys.exit(0)
