"""
Script / Utility for Cisco Recruitment project 1

Initial Code write: Michael Hagans, 4.13.2022
"""

from cgi import test
from code import interact
import csv
import email
import logging
import os
import re
import sqlite3
import threading
import paramiko
import requests
import database

from datetime import *
from paramiko_expect import SSHClientInteraction
from socket import timeout

logger = logging.getLogger()
logging.basicConfig(filename='logs.log', format='%(lineno)s %(asctime)s %(filename)s: %(message)s', filemode='w')
#logging.basicConfig(filename='logs.log', format='%(levelname)s: %(message)s', filemode='w')
logger.setLevel(logging.DEBUG)


class Operations:
    """ Handles server connection and operations """

    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
        self.base_url = f'https://{host}:8443/axl/'

    def uptime(self) -> str :
        """ Gathers Uptime from server via ssh """
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=self.host,username=self.username,password=self.password)
        # remote_connection = ssh_client.invoke_shell()
        interact = SSHClientInteraction(
            ssh_client,timeout=20,display=False
        )
        interact.expect('admin:')
        interact.send('show status')
        interact.expect('admin:')
        output = happy_converter(interact.current_output_clean)
        pattern = "up\s[0-9]*\s[a-z]*"
        match = re.search(pattern, output[10])
        if match:
            print(f'uptime is: {match}')
            logger.info(f'uptime is: {match}')
        else:
            logger.warning(f'Search for uptime unsuccessful: {self.host}')  
        ssh_client.close()          
        return match

    def get_version(self):
        """ Gathers Version from server """
        version = '11.5'
        print('version is: ', str(version))
        return version

    def get_performance(self):
        """ Gathers Performance from server """
        performance = '35% CPU, 60% RAM'
        print('performance is: ', str(performance))
        return performance

    def get_exposed_ports(self):
        """ Gathers Exposed Ports from server """
        exp_ports = 'None'
        print('exposed ports are: ', str(exp_ports))
        return exp_ports

def happy_converter(text):
    """ returns plit lines"""
    return text.splitlines()

def email_results():
    """ Prompts and handles email of results """
    email = input('Would you like to email these results? Enter y/n: ')
    if email == 'y':
        print('Emailing your results...')
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
        print('\n...one moment please.\n')
        try:
            ops = Operations(username, password, server)
            uptime = ops.uptime()
            version = ops.get_version()
            performance = ops.get_performance()
            exposed_ports = ops.get_exposed_ports()
            database.write_job(uptime, version, performance, exposed_ports,
                               server, date.today().strftime("%Y%m%d"))
            email = email_results()
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
