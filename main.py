"""
Script / Utility for Cisco Recruitment project 1

Initial Code write: Michael Hagans, 4.13.2022
"""

import csv
import logging
import os
import re
import sqlite3
from datetime import *

import paramiko
import requests

import database


class Operations:
    """ Handles server connection and operations """

    def __init__(self, username, password, host):
        self.username = username
        self.password = password
        self.host = host
        self.base_url = f'https://{host}:8443/axl/'

    def uptime(self):
        """ Gathers Uptime from server """
        uptime = '228 Days'
        print('uptime is: ', str(uptime))
        return uptime

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
    pull_previous_jobs = input('Would you like to view previous jobs? Enter y/n: ')
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
            logging.warning('Error occurred: %s', str(err))
            print('The following error occurred while attempting to gather data: ', str(err))
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
