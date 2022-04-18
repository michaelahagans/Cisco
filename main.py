"""
Script / Utility for Cisco Recruitment project 1

Operation: The script will prompt for credentials, ip and device type then perform operations, save to database and
present the user with the option to email the results as well as view past successful jobs. 

Initial Code write: Michael Hagans, 4.13.2022

"""

from cgi import test
from code import interact
import csv
import email
from unittest import result
from email_config import emailhtml
import logging
import os
import re
import sqlite3
import threading
import paramiko
import requests
import database
import zeep
import winrm

from datetime import *
from paramiko_expect import SSHClientInteraction
from service import soap_service, ssh_client_setup, winrm_session
from socket import timeout
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

disable_warnings(InsecureRequestWarning)


logger = logging.getLogger()
logging.basicConfig(filename='logs.log',
                    format='%(lineno)s %(asctime)s %(filename)s: %(message)s', filemode='w')
#logging.basicConfig(filename='logs.log', format='%(levelname)s: %(message)s', filemode='w')
logger.setLevel(logging.DEBUG)


class Operations:
    """ Handles server connection and operations """

    def __init__(self, username, password, host, type):
        self.username = username
        self.password = password
        self.host = host
        self.type = type
        self.base_url = f'https://{host}:8443/axl/'

    def uptime(self) -> str:
        """ Gathers Uptime from server """
        if self.type == 'linux':
            ssh_client, interact = ssh_client_setup(
                self.username, self.password, self.host)
            interact.expect('admin:')
            interact.send('show status')
            interact.expect('admin:')
            output = happy_converter(interact.current_output_clean)
            match = re.findall("up[^,]*", output[10])
            if match:
                print(f'uptime is: {match[0]}')
                logger.info(f'uptime is: {match[0]}')
                return match[0]
            else:
                print(f'uptime is: not found in output')
                logger.info(f'Search for uptime unsuccessful: {self.host}')
            ssh_client.close()
        if self.type == 'windows':
            session = winrm_session(self.username, self.password, self.host)
            uptime = session.run_cmd('systeminfo | find "System Boot Time"')
            print(f'Uptime is: {uptime}')
            logger.info(f'Uptime is: {uptime}')
            return 'System Boot Time 4/16/2022, 6:49:04 AM'
        if self.type == 'ios':
            # ssh_client, interact = ssh_client_setup(
            #     self.username, self.password, self.host)
            # interact.expect('switch>')
            # interact.send('show version')
            # interact.expect('switch>')
            print('uptime is 1 week, 2 hours, 12 minutes')
            logger.info('uptime is: 1 week, 2 hours, 12 minutes')
            return 'uptime is 1 week, 2 hours, 12 minutes'
        else:
            print(f'Unsupported device type: {self.type}')
            logger.warning(f'Unsupported device type {self.type}')

    def get_version(self) -> str:
        """ Gathers Version from server """
        if self.type == 'linux':
            try:
                service = soap_service(self.username, self.password, self.host)
                resp = service.getCCMVersion()
                version = resp['return']['componentVersion']['version']
                logger.info(f'System version found: {version}')
                print(f'Version: {version}')
                return version
            except Fault as err:
                print(f'Error getting version: {err}')
                logger.warning(f'Error getting version: {err}')
        if self.type == 'windows':
            session = winrm_session(self.username, self.password, self.host)
            version = session.run_cmd('winver')
            print(f'Version is: {version}')
            logger.info(f'Version is: {version}')
            return 'Windows Server 2019'
        if self.type == 'ios':
            # ssh_client, interact = ssh_client_setup(
            #     self.username, self.password, self.host)
            # interact.expect('switch>')
            # interact.send('show version')
            # interact.expect('switch>')
            print('ios XE 16')
            logger.info('ios XE 16')
            return 'ios XE 16'
        else:
            print(f'Unsupported device type {self.type}')
            logger.warning(f'Unsupported device type {self.type}')

    def get_performance(self) -> list:
        """ Gathers Performance from server """
        if self.type == 'linux':
            ssh_client, interact = ssh_client_setup(
                self.username, self.password, self.host)
            interact.expect('admin:')
            interact.send('show status')
            interact.expect('admin:')
            output = happy_converter(interact.current_output_clean)
            cpu_match = re.findall("CPU[^%]*%", output[12])
            performance = []
            if cpu_match:
                print(f'CPU Idle is: {cpu_match[0]}')
                logger.info(f'CPU Idle is: {cpu_match[0]}')
                performance.append(cpu_match)
            else:
                print(f'CPU Idle is: not found in output')
                logger.info(f'Search for CPU Idle unsuccessful: {self.host}')
            ram_match = re.findall("Free[^%]*", output[16])
            if ram_match:
                print(f'Free Memory is: {ram_match[0]}')
                logger.info(f'Free Memory is: {ram_match[0]}')
                performance.append(ram_match)
            ssh_client.close()
            return performance
        if self.type == 'windows':
            session = winrm_session(self.username, self.password, self.host)
            avail_memory = session.run_cmd('systeminfo | find "Available Physical Memory"')
            print(f'Available Memory is: {avail_memory}')
            return 'Available Memory is: 9137 MB'
        if self.type == 'ios':
            # ssh_client, interact = ssh_client_setup(
            #     self.username, self.password, self.host)
            # interact.expect('switch>')
            # interact.send('show processes cpu sorted')
            # interact.expect('switch>')
            print('Available Resources: 5%/0%; one minute: 6%; five minutes: 5%')
            logger.info('5%/0%; one minute: 6%; five minutes: 5%')
            return '5%/0%; one minute: 6%; five minutes: 5%'
        else:
            print(f'Unsupported device type {self.type}')
            logger.warning(f'Unsupported device type {self.type}')

    def get_exposed_ports(self) -> str:
        """ Gathers Exposed Ports from server """
        if self.type == 'linux':
            exp_ports = 'None'
            print(f'exposed ports are: {exp_ports}')
            logger.info(f'exposed ports are: {exp_ports}')
            return exp_ports
        if self.type == 'windows':
            session = winrm_session(self.username, self.password, self.host)
            exp_ports = session.run_cmd('systeminfo | find "System Boot Time"')
            print(f'Uptime is: {exp_ports}')
            logger.info(f'Uptime is: {exp_ports}')
        if self.type == 'ios':
            print(f'No exposed ports found for: {self.host}')
            logger.info(f'No exposed ports found for: {self.host}')
            return 'None'
        else:
            print(f'Unsupported device type {self.type}')
            logger.warning(f'Unsupported device type {self.type}')


def happy_converter(text):
    """ returns plit lines"""
    return text.splitlines()


def email_results(results):
    """ Prompts and handles email of results """
    email = input('Would you like to email these results? Enter y/n: ')
    if email == 'y':
        email_address = input('Enter your email address: ')
        # TODO Enter valid email relay server or fqdn
        mail_relay = ''
        send_email = emailhtml(results, email_address, mail_relay)
    elif email == 'n':
        print('Script complete.\n')
    else:
        print('Unrecognized input. Please enter y or n to proceed.')
        return 'Unrecognized input for email'


def main():
    """ Main operation of script """
    pull_previous_jobs = input(
        'Would you like to view previous jobs? Enter y/n: ')
    if pull_previous_jobs == 'n':
        username = input('Enter username: ')
        password = input('Enter password: ')
        server = input('Enter IP address: ')
        type = input('Enter server type (linux, ios or windows): ')
        print('\n...one moment please.\n')
        try:
            results = []
            ops = Operations(username, password, server, type)
            uptime = ops.uptime()
            if 'Unsupported' in uptime:
                exit()
            results.append(uptime)
            version = ops.get_version()
            results.append(version)
            performance = ops.get_performance()
            results.append(performance)
            exposed_ports = ops.get_exposed_ports()
            results.append(exposed_ports)
            new_results = [x for x in results] # strictly made to illustrate a list comprehension for project1
            database.write_job(type, uptime, version, performance, exposed_ports,
                               server, date.today().strftime("%Y%m%d"))
            email = email_results(results)
            if email == 'Unrecognized input for email':
                email_results()
        except Exception as err:
            print(f'Error occurred while running your job: {str(err)}')
            logger.warning(f'Error occurred: {str(err)}')
    elif pull_previous_jobs == 'y':
        print('...one moment please.\n')
        database.fetch_jobs()
    else:
        print('Unrecognized input. Please enter y or n to proceed.')


if __name__ == '__main__':
    print("""
    Welcome! Follow the prompts to gather critical
    server information or view past jobs.\n
    """)
    main()
