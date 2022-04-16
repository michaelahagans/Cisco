"""
Script / Utility for Cisco Recruitment project 1

Initial Code write: Michael Hagans, 4.13.2022
"""

from cgi import test
from code import interact
import csv
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

logging.basicConfig(format="%(lineno)d | %(utctime)s | %(levelname)s | %(message)s")


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
        try:
            interact.expect('admin:')
        except timeout:
            logging.warning('Timed out making SSH connection to server')
        interact.send('show status')
        interact.expect('admin:')
        output = happy_converter(interact.current_output_clean)
        pattern = "up\s[0-9]*\sdays"
        #test_string = '09:51:55 up 40 days, 20:41,  1 user,  load average: 0.12, 0.09, 0.09'
        result = re.match(pattern, output)
        if result:
            logging.info('uptime is: ', result)
        else:
            pattern = "up"
            result = re.match(pattern, output)
            if result:
                logging.info('Uptime is less than 1 day')
                return 'uptime is less than 1 day'
            else:
                logging.warning('Search for uptime unsuccessful')  
        ssh_client.close()          
        return result

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
            logging.warning('Error occurred: ', str(err))
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
