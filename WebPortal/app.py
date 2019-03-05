from flask import Flask, render_template, jsonify
# from gevent.wsgi import WSGIServer
import json
from requests.auth import HTTPBasicAuth
from flask import jsonify, make_response
import requests
from flask_cors import CORS
import sys


# Initialize the Flask Application
application = Flask(__name__)

application.config['SECRET_KEY'] = 'DNAC_AMEC_UNIVERSITY'

CORS(application)

server_ip = 'https://xx.xx.xx.xx'
sdwan_base_url = 'https://xx.xx.xx.xx:8443'
headers = {'content-type': 'application/json'}
sdwan_username = 'user'
sdwan_pass = 'password'
login_action = '/j_security_check'
login_data = {'j_username': sdwan_username, 'j_password': sdwan_pass}
auth = HTTPBasicAuth(sdwan_username, sdwan_pass)


class RestApiLib(object):
    def __init__(self):
        self.sdwan_base_url = sdwan_base_url
        self.session = {}
        self.login()
        self.headers = headers

    def login(self):
        """
        This function login in to SDWAN portal and create a session
        :return:
        """
        # Url for posting login data
        login_url = sdwan_base_url + login_action
        sess = requests.session()

        # If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if '<html>' in login_response.content:
            print "Login Failed"
            sys.exit(0)
        print "login succedd....................................................."
        self.session[sdwan_base_url] = sess

    def get_request(self, mount_point):
        """
        This function will get the data from the url of user requested
        :param mount_point:
        :return:
        """
        self.mount_point = mount_point
        url = '{0}/dataservice{1}'.format(str(self.sdwan_base_url), str(self.mount_point))
        response = self.session[self.sdwan_base_url].get(url, verify=False)
        data = response.content
        return data

    def post_request(self, mount_point, payload):
        """
        This function is a post call which create a data using the payload in SDWAN dashboard
        :param mount_point: url
        :param payload:
        :return:
        """
        self.mount_point = mount_point
        url = '{0}/{1}'.format(str(self.sdwan_base_url), str(self.mount_point))
        payload = json.dumps(payload)
        response = self.session[self.sdwan_base_url].post(url=url, data=payload, headers=self.headers, verify=False)
        data = response.content
        return data

    def put_request(self, mount_point, payload):
        """
        This function is to update the request using payload
        :param mount_point:
        :param payload:
        :return:
        """
        self.mount_point = mount_point
        url = '{0}/{1}'.format(str(self.sdwan_base_url), str(self.mount_point))
        payload = json.dumps(payload)
        response = self.session[self.sdwan_base_url].put(url=url, data=payload, headers=self.headers, verify=False)
        data = response.content
        return data


def response_headers(data):
    """
    Function is header for Access Control
    :param data:
    :return:
    """
    # unicode_data = json.loads(data.read())
    response_data = jsonify(data)
    resp = make_response(response_data)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@application.route("/home")
def home():
    """
    Test API
    :return:
    """
    return render_template('index_org.html')


@application.route("/api/v1/simulation/great_wall_policy")
def add_ips():
    """
    API call to add Intrustion Prevenition policy in the SDWAN Dashboard--> Configuration -->
    Cloud Onramp for SAAS feature
    :return:
    """
    obj = RestApiLib()
    payload = {"policyDescription": "Greatwall Policy", "policyType": "feature", "policyName": "Greatwall_Policy",
               "policyUseCase": "custom", "policyDefinition":
                   {"assembly": [{"definitionId": "6d372578-a02d-4b73-83db-78f4e4192fc6", "type": "urlFiltering"},
                                 {"definitionId": "26d628ef-4696-448d-8a44-46bbc15ccbe5", "type": "DNSSecurity"},
                                 {"definitionId": "7452b71a-2208-4605-9f66-2e784de5695d", "type": "zoneBasedFW"},
                                 {"definitionId": "cd44e4b6-6777-4309-9c4a-182c12d5cecb", "type": "intrusionPrevention"}],
                    "settings": {"failureMode": "close", "zoneToNozoneInternet": "deny"}}}
    response = obj.put_request('dataservice/template/policy/security/1ca11fbe-cfd5-4f2a-8e26-10e4ca966acf', payload)

    payload = {"templateId": "5da23142-0c39-4fb9-a066-90962408a6a7",
               "deviceIds": ["CSR-461b0d28-6d32-4f60-87ae-bdc75303c798"], "isEdited": True, "isMasterEdited": False}
    response = obj.post_request('dataservice/template/device/config/input/', payload)

    payload_3 = {"templateId": "a1e1d98e-4794-45d5-a60f-159ce1f18ebc", "deviceIds": ["ISR4331/K9-FDO20110MYT"],
               "isEdited": True, "isMasterEdited": False}
    response = obj.post_request('dataservice/template/device/config/input/', payload_3)

    payload_4 = {"deviceTemplateList": [{"templateId": "5da23142-0c39-4fb9-a066-90962408a6a7",
                                       "device": [{"csv-status": "complete",
                                                   "csv-deviceId": "CSR-461b0d28-6d32-4f60-87ae-bdc75303c798",
                                                   "csv-deviceIP": "1.15.1.2", "csv-host-name": "CSR1Kv-Branch-SanJose",
                                                   "/10/GigabitEthernet3/interface/ip/address": "10.15.27.1/24",
                                                   "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn0_next_hop_ip_address_0/address": "173.36.218.161",
                                                   "/0/GigbitEthernet2/interface/ip/address": "173.36.218.181/27",
                                                   "/0/GigbitEthernet2/interface/tunnel-interface/color/value": "public-internet",
                                                   "//system/clock/timezone": "America/Los_Angeles", "//system/host-name": "CSR1Kv-Branch-SanJose",
                                                   "//system/gps-location/latitude": "37.418806", "//system/gps-location/longitude": "-121.919267",
                                                   "//system/system-ip": "1.15.1.2", "//system/site-id": "1512",
                                                   "/10/GigabitEthernet4/interface/ip/address": "10.15.28.1/24",
                                                   "csv-templateId": "5da23142-0c39-4fb9-a066-90962408a6a7"}],
                                       "isEdited": True, "isMasterEdited": False},
                                      {"templateId": "a1e1d98e-4794-45d5-a60f-159ce1f18ebc",
                                       "device": [{"csv-status": "complete", "csv-deviceId": "ISR4331/K9-FDO20110MYT",
                                                   "csv-deviceIP": "1.12.1.1", "csv-host-name": "ISR4331-LasVegas",
                                                   "/10/vpn10_if_name_GigabitEthernet/interface/if-name": "GigbitEthernet0/0/1",
                                                   "/10/vpn10_if_name_GigabitEthernet/interface/ip/address": "10.7.1.1/24",
                                                   "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn0_next_hop_ip_address_0/address": "10.16.10.65",
                                                   "/0/vpn0_if_name_GigabitEthernet/interface/if-name": "GigbitEthernet0/0/0",
                                                   "/0/vpn0_if_name_GigabitEthernet/interface/ip/address": "10.16.10.85/27",
                                                   "/0/vpn0_if_name_GigabitEthernet/interface/tunnel-interface/color/value": "public-internet",
                                                   "//system/clock/timezone": "America/Los_Angeles",
                                                   "//system/host-name": "ISR4331-LasVegas",
                                                   "//system/gps-location/latitude": "36.12",
                                                   "//system/gps-location/longitude": "-115.15",
                                                   "//system/system-ip": "1.12.1.1", "//system/site-id": "1211",
                                                   "csv-templateId": "a1e1d98e-4794-45d5-a60f-159ce1f18ebc"}],
                                       "isEdited": True,"isMasterEdited": False}]}

    response = obj.post_request('dataservice/template/device/config/attachfeature', payload_4)
    print "response for great wall policy step 4  --> ", response
    return response


@application.route("/api/v1/simulation/resetSDWan")
def reset_sdwan():
    """
    Function to remove Intrustion Prevenition policy from the SDWAN Dashboard--> Configuration --> Security and
    :return:
    """
    reset_url = sdwan_base_url + '/dataservice/template/cloudx/manage/apps'
    payload = {"appList": [{"appType": "box_net", "longName": "Box", "appVpnList": "10"},
                           {"appType": "salesforce", "longName": "Salesforce", "appVpnList": "10"},
                           {"appType": "gotomeeting", "longName": "Goto Meeting", "appVpnList": "10"},
                           {"appType": "dropbox", "longName": "Dropbox", "appVpnList": "10"}]}
    response = requests.post(reset_url, auth=auth, headers=headers, verify=False, json=payload)
    print ("Removing the application from the App List and Response is ", response.json())

    obj = RestApiLib()
    payload = {"policyDescription":"Greatwall Policy","policyType":"feature","policyName":"Greatwall_Policy",
               "policyUseCase":"custom","policyDefinition":
                   {"assembly":[{"definitionId":"6d372578-a02d-4b73-83db-78f4e4192fc6","type":"urlFiltering"},
                                {"definitionId":"26d628ef-4696-448d-8a44-46bbc15ccbe5","type":"DNSSecurity"},
                                {"definitionId":"7452b71a-2208-4605-9f66-2e784de5695d","type":"zoneBasedFW"}],
                    "settings":{"failureMode":"close","zoneToNozoneInternet":"deny"}}}
    response = obj.put_request('dataservice/template/policy/security/1ca11fbe-cfd5-4f2a-8e26-10e4ca966acf', payload)

    payload_2 = {"templateId":"5da23142-0c39-4fb9-a066-90962408a6a7",
                 "deviceIds":["CSR-461b0d28-6d32-4f60-87ae-bdc75303c798"],"isEdited":True,"isMasterEdited":False}
    response = obj.post_request('dataservice/template/device/config/input/', payload_2)

    payload_3 = {"templateId":"a1e1d98e-4794-45d5-a60f-159ce1f18ebc",
                 "deviceIds":["ISR4331/K9-FDO20110MYT"],"isEdited":True,"isMasterEdited":False}
    response = obj.post_request('dataservice/template/device/config/input/', payload_3)

    payload_4 = {"deviceTemplateList":[{"templateId":"5da23142-0c39-4fb9-a066-90962408a6a7",
                                        "device":[{"csv-status":"complete",
                                                   "csv-deviceId":"CSR-461b0d28-6d32-4f60-87ae-bdc75303c798",
                                                   "csv-deviceIP":"1.15.1.2",
                                                   "csv-host-name":"CSR1Kv-Branch-SanJose","/10/GigabitEthernet3/interface/ip/address":"10.15.27.1/24",
                                                   "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn0_next_hop_ip_address_0/address":"173.36.218.161",
                                                   "/0/GigbitEthernet2/interface/ip/address":"173.36.218.181/27",
                                                   "/0/GigbitEthernet2/interface/tunnel-interface/color/value":"public-internet",
                                                   "//system/clock/timezone":"America/Los_Angeles",
                                                   "//system/host-name":"CSR1Kv-Branch-SanJose",
                                                   "//system/gps-location/latitude":"37.418806",
                                                   "//system/gps-location/longitude":"-121.919267","//system/system-ip":"1.15.1.2",
                                                   "//system/site-id":"1512","/10/GigabitEthernet4/interface/ip/address":"10.15.28.1/24",
                                                   "csv-templateId":"5da23142-0c39-4fb9-a066-90962408a6a7"}],
                                        "isEdited":True,"isMasterEdited":False},
                                       {"templateId":"a1e1d98e-4794-45d5-a60f-159ce1f18ebc",
                                        "device":[{"csv-status":"complete","csv-deviceId":"ISR4331/K9-FDO20110MYT",
                                                   "csv-deviceIP":"1.12.1.1",
                                                   "csv-host-name":"ISR4331-LasVegas",
                                                   "/10/vpn10_if_name_GigabitEthernet/interface/if-name":"GigbitEthernet0/0/1",
                                                   "/10/vpn10_if_name_GigabitEthernet/interface/ip/address":"10.7.1.1/24",
                                                   "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/vpn0_next_hop_ip_address_0/address":"10.16.10.65",
                                                   "/0/vpn0_if_name_GigabitEthernet/interface/if-name":"GigbitEthernet0/0/0",
                                                   "/0/vpn0_if_name_GigabitEthernet/interface/ip/address":"10.16.10.85/27",
                                                   "/0/vpn0_if_name_GigabitEthernet/interface/tunnel-interface/color/value":"public-internet",
                                                   "//system/clock/timezone":"America/Los_Angeles","//system/host-name":"ISR4331-LasVegas",
                                                   "//system/gps-location/latitude":"36.12","//system/gps-location/longitude":"-115.15",
                                                   "//system/system-ip":"1.12.1.1","//system/site-id":"1211",
                                                   "csv-templateId":"a1e1d98e-4794-45d5-a60f-159ce1f18ebc"}],
                                        "isEdited":True,"isMasterEdited":False}]}
    response = obj.post_request('dataservice/template/device/config/attachfeature', payload_4)
    print "response for great wall policy step 4  --> ", response
    return response


@application.route("/api/v1/simulation/cloud_onramp_saas")
def add_applist():
    """
    API call to add Application like office365 in the SDWAN Dashboard--> Configuration -->
    Cloud Onramp for SAAS feature
    :return:
    """
    # Adding App to the list
    add_url = sdwan_base_url + '/dataservice/template/cloudx/manage/apps'
    payload = {"appList": [{"appType": "box_net", "longName": "Box", "appVpnList": "10"},
                           {"appType": "salesforce", "longName": "Salesforce", "appVpnList": "10"},
                           {"appType": "gotomeeting", "longName": "Goto Meeting", "appVpnList": "10"},
                           {"appType": "dropbox", "longName": "Dropbox", "appVpnList": "10"},
                           {"appType": "office365", "longName": "Office 365", "appVpnList": "10"}]}
    resp = requests.post(add_url, auth=auth, headers=headers, verify=False, json=payload)
    print ("Adding to the App List is Sucessfull ..!!! and Response is ", resp.json())

    # Activating the App list after adding
    activate_url = sdwan_base_url+'/dataservice/template/device/config/attachcloudx'
    activate_payload = {"siteList": [1011], "isEdited": True}
    response = requests.put(activate_url, auth=auth, headers=headers, verify=False, json=activate_payload)
    print ("Activate App List is Sucessfull ..!!! and Response is ", response.json())
    response = response_headers(resp.json())
    return response


if __name__ == '__main__':
    # http_server = WSGIServer(('', 5001), application)
    # http_server.serve_forever()
    application.run(host='0.0.0.0')
