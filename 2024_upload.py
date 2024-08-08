# import modules
import pandas as pd
import os
import json
import csv
from datetime import datetime, date, time, timezone

# get facilities data for 2024
file_path_facilities = r"C:\Users\klittle\Downloads\ParkFacilityReservations3.txt\ParkFacilitiesReservations.txt"
facilities = pd.read_csv(file_path_facilities, sep="|", index_col=False, 
                 names=["parkFacilityReservationKey", "locationName", "facilityName", "streetAddressText", "cityName", "zipCode", "reservationBeginDate", "reservationBeginTime", "reservationEndDate", "reservationEndTime", "transactionDtm", "latitudeAndLongitudeCrd", "reservationDsc", "facilityLocationCode", "facilitySpaceCode", "customerName", "customerFirstName", "customerLastName", "householdNbr", "headCnt", "reservationPurposeDsc", "comboKeyCode", "facilityParentCode", "facilityChildCodeList", "facilitySiblingCodeList", "reservationFacilityTypeCode", "reservationTypeName", "featureCodeList", "lightedFieldInd", "fieldTurfTypeDsc", "fieldOperationalStatusDsc", "reservationBeginDtm", "reservationEndDtm", "reservationStatusCode", "calendarIncludeInd", "fieldUseTypeDsc", "parkUrlText"])
facilities = facilities[facilities["reservationBeginDate"].str.contains("2024")]
facilities = facilities.sort_values(by=["reservationBeginDate"])

# removing unnecessary fields
facilities.drop(["parkFacilityReservationKey", "cityName", "latitudeAndLongitudeCrd", "reservationDsc", "facilityLocationCode", "customerFirstName", "customerLastName", "householdNbr", "facilityParentCode", "facilityChildCodeList", "facilitySiblingCodeList", "featureCodeList", "lightedFieldInd", "calendarIncludeInd", "fieldUseTypeDsc", "parkUrlText"], axis=1, inplace=True)

# renaming locationName field ParkName
facilities.rename(columns = {"facilityName" : "parkName"}, inplace = True)

# aggregate records by month, time of day, and reservation length
facilities["reservationBeginDtm"] = pd.to_datetime(facilities["reservationBeginDtm"], format="ISO8601", utc=True, errors="coerce")
facilities["reservationEndDtm"] = pd.to_datetime(facilities["reservationEndDtm"], format="ISO8601", utc=True, errors="coerce")

facilities["resLength"] = facilities["reservationEndDtm"] - facilities["reservationBeginDtm"]
facilities["resLengthHours"] = facilities["resLength"] / pd.Timedelta(hours=1)
facilities.drop(["resLength"], axis=1, inplace=True)

# clip month, day, and time to new fields
begstr = facilities["reservationBeginDtm"].astype(str)

facilities["resMonth"] = begstr.str[5:7]
facilities["resDay"] = begstr.str[8:10]
facilities["resTime"] = begstr.str[10:16]

# aggregate time records into morning, afternoon, evening, and night
def is_time_between(begin_time, end_time, check_time=None):
    # if check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time
    
if facilities["reservationBeginDtm"] == is_time_between(time(22, 00), time(4, 59)):
    facilities["reservationBeginDtm"] = "Night (10PM to 4:59AM)"
elif facilities["reservationBeginDtm"] == is_time_between(time (5, 00), time(11,59)):
    facilities["reservationBeginDtm"] = "Morning (5AM to 11:59AM)"
elif facilities["reservationBeginDtm"] == is_time_between(time (12, 00), time(17,59)):
    facilities["reservationBeginDtm"] = "Afternoon (12PM to 5:59PM)"
elif facilities["reservationBeginDtm"] == is_time_between(time (18, 00), time(21:59)):
    facilities["reservationBeginDtm"] = "Evening (6PM to 9:59PM)"
facilities["reservationBeginDtm"]

# dropping more unnecessary fields
facilities.drop(["streetAddressText", "zipCode", "reservationBeginDate", "reservationBeginTime", "reservationEndDate", "reservationEndTime", "transactionDtm", "facilitySpaceCode", "comboKeyCode", "reservationFacilityTypeCode", "reservationTypeName", "fieldTurfTypeDsc", "reservationBeginDtm", "reservationEndDtm", "fieldOperationalStatusDsc"], axis=1, inplace=True)

# create key for records: concatenated field of location name, park name, reservation month, and reservation time
ln = facilities["locationName"].str.replace("&", "and")
rtu = facilities["resTime"].str.replace(":", "_")
cnu = facilities["customerName"].str.replace("'", "")
facilities["key"] = ln + cnu + facilities["resMonth"] + facilities["resDay"] + rtu
facilities["key"] = facilities["key"].str.replace(" ", "")

# drop duplicates
facilities = facilities.drop_duplicates(subset=["key"], keep="last")

# set index from key
facilities.set_index(keys=["key"], inplace=True)

# export table as csv
outpath = r"C:\Users\klittle\OneDrive - Blue Raster\Desktop\Projects\Parks and facilities\parks_initial.csv"
facilities.to_csv(outpath)
