# Introduction

Try the APIs for Cisco DNA Center and SD-WAN. This demonstration shows how you can create a portal to automate common management controller tasks to streamline operations across multiple management controllers.  This is done by leveraging the management controller’s Representational State Transfer (REST) APIs.  This demo leverages these REST APIs to configure devices in the campus as well as in the Branch environment (across a WAN connection to the campus).

REST is an architecture style for designing networked applications. REST uses Hypertext Transfer Protocol (HTTP or HTTPS) to send a request to a web service, which returns a response. The standard HTTP methods are GET (retrieve information), PUT (update an object), POST (create an object) and DELETE (remove an object). Learn more about REST APIs with the [Cisco DevNet Learning Labs](https://learninglabs.cisco.com).

This GitHub repository provides the necessary REST API calls to Cisco DNA Center for claiming devices to a pre-defined workflow in Cisco DNA Center and assigning a Border node to an existing Fabric.  This repository also provides REST API calls to Cisco vManage to configure an Intrusion Prevention System policy.

# Cisco DNA Center and vManage Introduction

Cisco DNA Center is a campus network management controller used to manage, monitor and secure a campus environment.  Cisco DNA Center secures campus environments by implementing a fabric(s), segments users within that fabric, and implements group based policies.  This part of the solution is called SD-Access.  Cisco DNA Center can also be used to manage (push device configuration, upgrade device images) and monitor (through Assurance) both fabric and non-fabric environments.  Assurance monitors device, endpoint/client and application health.  

Cisco vManage is an WAN management controller that is used to provide a cloud-first architecture that separates data and control planes.  Cisco vManage is a fabric that allows to securely and easily connect your WAN to data centers, branches, campuses, and colocation facilities to improve network speed, security, and efficiency.  This WAN fabric is called SD-WAN.

The Cisco SD-WAN fabric and solution connects users at the branch to applications in the cloud in a seamless, secure, and reliable fashion. Cisco vManage is used to manage and monitor the branch devices.  

Cisco SD-WAN reduces complexity by having a single management interface (vManage) for both the network and security. Cisco SD-WAN security capabilities include an application-aware enterprise firewall, Intrusion Prevention Security (IPS), DNS layer enforcement (Cisco Umbrella™), and URL filtering.

# Cisco DNA Center and vManage REST APIs

Both Cisco vManage controller and Cisco DNA Center are open and programmable. With this openness and programmability, you can access the available REST APIs, create API calls, obtain device and interface information using code, pass parameters and write applications, and work on innovative solutions.

Learn more about these APIs at [vManage REST APIs documentation](https://developer.cisco.com/sdwan/) and [Cisco DNA Center Platform documentation](https://developer.cisco.com/site/dna-center-rest-api/).


# Installation of WebPortal to execute REST APIs to Cisco DNA Center/vManage

On Ubuntu 18.04 VM with Python 2.7, install the following packages:

```
sudo apt-get install -y nodejs
sudo apt-get install -y npm
sudo npm install -g pm2
sudo npm install -g http-server
sudo apt-get install unzip
sudo apt-get install python-pip
```

Clone the repository with the following command:

`git clone https://github.com/CiscoDevNet/multi-domain-api.git`

and then go to WebPortal directory.

Verify that path is `/usr/local/bin/http-server` and then execute the following command.

`pm2 startup`

If not, change path after `pm2 start <http-server path> -- <where the build folder is located>` and start the UI server, e.g.,

`pm2 start /usr/local/bin/http-server -- /home/…./WebPortal/build --p 7000`

Copy the line `sudo env PATH=…` from the above output and then execute, e.g., 

```sudo env PATH=$PATH:/usr/bin /us/local/lib/node_modules/pm2/bin/pm2 startup system -u user --hp /home/user```

Install python related packages using the following commands

```
sudo pip install flask
sudo pip install requests
sudo pip install flask_cors
```

After installing the packages, go to the application path

```cd /home/……/WebPortal/```

Then execute the following command

```nohup python app.py &```

Go to the browser and enter `https://<server_ip>:7000` for accessing the WebPortal.

# API Operations

## Cisco DNA Center Use case 1 - PnP Operations
In the first use case, PnP is used to “claim” devices to a pre-defined workflow.  This process is used for day zero bootstrap configuration.  This workflow can be tailored to site, certain features, devices, etc.

There are many PnP APIs.  There are some examples below that were performed prior to this demo.  These can be done via the API, manually or via a process of automated Cisco DNA Center steps.



|  API  |  Operation  | Description  |
|  ---  |  ---  |   ---  |
|  [/dna/intent/api/v1/onboarding/pnp-settings/savacct ](https://pubhub.devnetcloud.com/media/dna-center-api-1210/docs/swagger_dnacp_1210.html#!/PnP/addVirtualAccount)  |  POST | Add Virtual Account |
|  [/dna/intent/api/v1/onboarding/pnp-workflow](https://pubhub.devnetcloud.com/media/dna-center-api-1210/docs/swagger_dnacp_1210.html#!/PnP/addAWorkflow)  |  POST  | Add a Workflow |
|  [/dna/intent/api/v1/onboarding/pnp-device](https://pubhub.devnetcloud.com/media/dna-center-api-1210/docs/swagger_dnacp_1210.html#!/PnP/addDeviceToPnpDatabase)  |  POST  | Add a Device |
|  [/dna/intent/api/v1/template-programmer/project](https://pubhub.devnetcloud.com/media/dna-center-api-1210/docs/swagger_dnacp_1210.html#!/Template_Programmer/createProject)  |  POST  | Create Project |
|  [/dna/system/api/v1/site](https://pubhub.devnetcloud.com/media/dna-center-api-1210/docs/swagger_dnacp_1210.html#!/Sites/createSite)  |  POST  | Create Site |

The next PnP API is the one that was performed in this demo.  
Claim devices to a site (that has a pre-defined workflow):


```
POST https://<DNA Center hostname/IP>/dna/intent/api/v1/onboarding/pnp-device/site-claim

BODY
Model:

{
  "deviceId": "string",
  "siteId": "string",
  "type": "Default"
}

Demo Example:
{  "deviceId": "<Device name>",  "siteId": ”MEL03",  "type": ”BorderRouter"}
{  "deviceId": "MEL03-C9200-01",  "siteId": ”MEL03",  "type": ”Access"}
{  "deviceId": "MEL03-C9200-02",  "siteId": ”MEL03",  "type": ”Access"}
{  "deviceId": "MEL03-C9200-03",  "siteId": ”MEL03",  "type": ”Access"}
{  "deviceId": "MEL03-C9300-01",  "siteId": ”MEL03",  "type": ”Access"}
{  "deviceId": "MEL03-C9800-05",  "siteId": ”MEL03",  "type": ”Access"}
{  "deviceId": "MEL03-C9500-01",  "siteId": ”MEL03",  "type": ”Core"}
{  "deviceId": "MEL03-ISR4461-01",  "siteId": ”MEL03",  "type": ”BorderRouter"}
{  "deviceId": "MEL03-C9500-01",  "siteId": ”MEL03",  "type": ”Core"}
{  "deviceId": "MEL03-IE3300-01",  "siteId": ”MEL03",  "type": ”Access"}
```
![](DNAC_Usecase1.png)

## Cisco DNA Center Use Case 2 - Add Fabric Border to existing Fabric
Once a fabric is created, we have the ability to add fabric borders that will connect to our Datacenter(s), WAN, Branch and other environments.  In the second use case, we are adding recently claimed and provisioned devices to an existing fabric.

NOTE: Base provisioning is necessary post PnP and before devices can be added to the Fabric.  This was not performed in this demo.  Additionally, APIs for adding Fabric Edge, WLC and Control Plane Node roles are not yet available in Cisco DNA Center version 1.2.10.

```
POST  https://<Cisco DNA Center IP/Hostname>/dna/intent/api/v1/business/sda/border-device/

BODY

Model:

[
  {
    "deviceManagementIpAddress": "string",
    "siteHierarchy": "string",
    "externalDomainRoutingProtocolName": "string",
    "externalConnectivityIpPoolName": "string",
    "internalAutonomouSystemNumber": "string",
    "borderSessionType": "string",
    "connectedToInternet": true,
    "externalConnectivitySettings": [
      {
        "interfaceName": "string",
        "externalAutonomouSystemNumber": "string",
        "l3Handoff": [
          {
            "virtualNetwork": {
              "virtualNetworkName": "string"
            }
          }
        ]
      }
    ]
  }
]
```

Demo Example:

```
[  {    "deviceManagementIpAddress": "10.0.255.34",    ”siteHierarchy”: Australia,Victoria,Melbourne,MEL03”,"externalDomainRoutingProtocolName": ”BGP", "internalAutonomouSystemNumber":”BGPUplink”, "internalAutonomouSystemNumber": ”65000”,"borderSessionType": ”Anywhere",   "connectedToInternet": true,    "externalConnectivitySettings": [      {        "interfaceName": ”Interface TenGigabitEthernet1/0/12",        "externalAutonomouSystemNumber": ”65001",        "l3Handoff": [          {            "virtualNetwork": {              "virtualNetworkName": ”Campus"            }          }        ]      }    ]  }]
```

![](DNAC_Usecase2.png)



## vManage Use Case 1 - Add Intrusion Prevention System Policy:
In this demo, we are adding an IPS policy to an existing security policy.  The following REST API will add an IPS policy to the existing SD-WAN security policy called “Greatwall_Policy” using the HTML web portal that you built.

```
PUT https://<vManage hostname/IP>/dataservice/template/policy/security/1ca11fbe-cfd5-4f2a-8e26-10e4ca966acf

BODY

Demo Example:
{"policyDescription":"Greatwall Policy","policyType":"feature","policyName":"Greatwall_Policy","policyUseCase":"custom","policyDefinition":{"assembly":[{"definitionId":"6d372578-a02d-4b73-83db-78f4e4192fc6","type":"urlFiltering"},{"definitionId":"26d628ef-4696-448d-8a44-46bbc15ccbe5","type":"DNSSecurity"},{"definitionId":"7452b71a-2208-4605-9f66-2e784de5695d","type":"zoneBasedFW"},{"definitionId":"d7018da7-7a59-4611-9287-6f3716a3a447","type":"intrusionPrevention"}],"settings":{"failureMode":"close","zoneToNozoneInternet":"deny"}}}
```

![](vManage_Usecase1.png)

# Get the code

Clone the repository with the following command:
`git clone https://github.com/CiscoDevNet/multi-domain-api.git`


# Requirements

- Use pip to install the necessary requirements.

  ```sudo pip install -r requirements.txt```

- Cisco DNAC 1.2.10 is required for the new intent based APIs (fabric component)
- Cisco DNAC requires the Cisco DNAC Platform application to be installed. Details on how to install this can be found [here](https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/dna-center/1-2-10/admin/guide/b_dnac_admin_guide_1_2_10/b_dnac_admin_guide_1_2_10_chapter_0100.html).

