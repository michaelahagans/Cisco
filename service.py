from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
import paramiko
import winrm

from paramiko_expect import SSHClientInteraction



def soap_service(username, password, host):
    """ Returns Soap Service"""
    wsdl = 'AXLAPI.wsdl'
    location = f'https://{host}:8443/axl/'
    binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
    session = Session()
    session.verify = False
    session.auth = HTTPBasicAuth(username, password)

    transport = Transport(cache=SqliteCache(), session=session, timeout=20)
    history = HistoryPlugin()
    client = Client(wsdl=wsdl, transport=transport, plugins=[history])
    service = client.create_service(binding, location)
    return service


def ssh_client_setup(username, password, host):
    """ init ssh """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    # remote_connection = ssh_client.invoke_shell()
    interact = SSHClientInteraction(
        ssh_client, timeout=20, display=False
    )
    return ssh_client, interact


def winrm_session(username, password, host):
    """ return winrm session """
    session = winrm.Session(host, auth=(
        username, password))
    return session
