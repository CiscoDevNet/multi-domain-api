#!/usr/bin/python2.7

import json
import requests
import sys

sdwan_base_url = 'https://sdwan-sj06.cisco.com:8443'
headers = {'content-type': 'application/json'}
sdwan_username = 'vimoreno'
sdwan_pass = 'C1sco123'
login_action = '/j_security_check'
login_data = {'j_username': sdwan_username, 'j_password': sdwan_pass}


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


def reset_ips():
    """
    Function to remove Intrustion Prevenition policy from the SDWAN Dashboard--> Configuration --> Security
    :return:
    """
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


if __name__== '__main__':
    globals()[sys.argv[1]]()
