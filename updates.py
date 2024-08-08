### Imports

# Python libraries
import pandas as pd
import requests
import json
import csv
from datetime import datetime, date, time, timezone, timedelta

# ArcGIS
from arcgis.gis import GIS
gis = GIS("home")

# Old facilities
item = gis.content.get("89f6d300592b4e8b99e96eaec852a4d9")
facilities_old = item.tables[0]

# Get facilities data from Arlington open data where transaction was in August 2024 or later
url = "https://datahub-v2.arlingtonva.us/api/recreation/ParkFacilityReservations?$top=100000&$filter=transactionDtm gt 2024-08-01T00:00:00.000Z&$orderby=reservationBeginDate"
payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

# Read in 2024 facilities data as dataframe
facilities_unfiltered = pd.read_json(response.text)
facilities_unfiltered = facilities_unfiltered.sort_values(by=["reservationBeginDate"])

# Convert transactionDtm to string of year-month-day format
tstr = facilities_unfiltered["transactionDtm"].astype(str)
facilities_unfiltered["transactionDtm"] = tstr.str[0:10]
facilities_unfiltered["transactionDtm"]

# Create yesterday
today = date.today()
yesterday = today - timedelta(days = 1)
yesterday = yesterday.isoformat()
yesterday

# Filter for reservations made yesterday
facilities = facilities_unfiltered.loc[facilities_unfiltered["transactionDtm"] == yesterday]

### Imports

# Python libraries
import pandas as pd
import requests
import json
import csv
from datetime import datetime, date, time, timezone, timedelta

# ArcGIS
from arcgis.gis import GIS
gis = GIS("home")

# Old facilities
item = gis.content.get("89f6d300592b4e8b99e96eaec852a4d9")
facilities_old = item.tables[0]

# Get facilities data from Arlington open data where transaction was in August 2024 or later
url = "https://datahub-v2.arlingtonva.us/api/recreation/ParkFacilityReservations?$top=100000&$filter=transactionDtm gt 2024-08-01T00:00:00.000Z&$orderby=reservationBeginDate"
payload = {}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

# Read in 2024 facilities data as dataframe
facilities_unfiltered = pd.read_json(response.text)
facilities_unfiltered = facilities_unfiltered.sort_values(by=["reservationBeginDate"])

# Convert transactionDtm to string of year-month-day format
tstr = facilities_unfiltered["transactionDtm"].astype(str)
facilities_unfiltered["transactionDtm"] = tstr.str[0:10]
facilities_unfiltered["transactionDtm"]

# Create yesterday
today = date.today()
yesterday = today - timedelta(days = 1)
yesterday = yesterday.isoformat()
yesterday

# Filter for reservations made yesterday
facilities = facilities_unfiltered.loc[facilities_unfiltered["transactionDtm"] == yesterday]

### Export
add = facilities_old.edit_features(adds = facilities)
