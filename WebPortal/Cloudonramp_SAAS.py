#!/usr/bin/python2.7

import sys
import requests
from requests.auth import HTTPBasicAuth

sdwan_base_url = 'https://sdwan-sj06.cisco.com:8443/'
headers = {'content-type': 'application/json'}
sdwan_username = 'vimoreno'
sdwan_pass = 'C1sco123'
auth = HTTPBasicAuth(sdwan_username, sdwan_pass)


def reset_applist():
    """
    API call to remove Application like office365 from the SDWAN Dashboard--> Configuration -->
    Cloud Onramp for SAAS feature
    :return:
    """
    # To delete office365
    reset_url = sdwan_base_url + 'dataservice/template/cloudx/manage/apps'
    payload = {"appList":[{"appType":"box_net","longName":"Box","appVpnList":"10"},
                          {"appType":"salesforce","longName":"Salesforce","appVpnList":"10"},
                          {"appType":"gotomeeting","longName":"Goto Meeting","appVpnList":"10"},
                          {"appType":"dropbox","longName":"Dropbox","appVpnList":"10"}]}
    response = requests.post(reset_url, auth=auth, headers=headers, verify=False, json=payload)
    print ("Removing the application from the App List and Response is ", response.json())
    return response


def add_applist():
    """
    API call to add Application like office365 in the SDWAN Dashboard--> Configuration -->
    Cloud Onramp for SAAS feature
    :return:
    """
    # Adding App to the list
    add_url = sdwan_base_url + 'dataservice/template/cloudx/manage/apps'
    payload = {"appList": [{"appType": "box_net", "longName": "Box", "appVpnList": "10"},
                           {"appType": "salesforce", "longName": "Salesforce", "appVpnList": "10"},
                           {"appType": "gotomeeting", "longName": "Goto Meeting", "appVpnList": "10"},
                           {"appType": "dropbox", "longName": "Dropbox", "appVpnList": "10"},
                           {"appType": "office365", "longName": "Office 365", "appVpnList": "10"}]}
    resp = requests.post(add_url, auth=auth, headers=headers, verify=False, json=payload)
    print ("Adding to the App List is Sucessfull ..!!! and Response is ", resp.json())

    # Activating the App list after adding
    activate_url = sdwan_base_url+'dataservice/template/device/config/attachcloudx'
    activate_payload = {"siteList": [1011], "isEdited": True}
    response = requests.put(activate_url, auth=auth, headers=headers, verify=False, json=activate_payload)
    print ("Activate App List is Sucessfull ..!!! and Response is ", response.json())
    return response


if __name__== '__main__':
    globals()[sys.argv[1]]()
