import csv
import imp
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from attr import fields


def email_ops(results, email_address, mail_relay):
    """ sends email with csv """
    try:
        fields = ['Uptime', 'Version', 'Performance', 'Exposed Ports']
        filename = 'Job_Results.csv'
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(fields)
            writer.writerow(results)

        if mail_relay == '':
            print('CSV File saved locally. Email failed due to no valid email relay server.')
            quit()
        sender = 'Server_Checker@cisco.com'
        receivers = [f'{email_address}']
        file_to_send = 'Job_Results.csv'
        mailrelay = smtplib.SMTP(f'{mail_relay}')

        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'Server Check Results'
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        msg.attach(file_to_send)

        mailrelay.sendmail(sender, receivers, msg.as_string())
        mailrelay.quit()
        print('\nEmail Sent\n')
    except Exception as err:
        print(f'Error occured sending email with error: {str(err)}')
        print('\nEmail Failed\n')