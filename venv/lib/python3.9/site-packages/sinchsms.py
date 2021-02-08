#!/usr/bin/env python
"""
sinchsms - a module to send sms using the Sinch REST apis, www.sinch.com
"""

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import json
import base64

class SinchSMS(object):

    """ A class for handling communication with the Sinch REST apis. """

    SEND_SMS_URL = 'https://messagingApi.sinch.com/v1/sms/'
    CHECK_STATUS_URL = 'https://messagingApi.sinch.com/v1/message/status/'

    def __init__(self, app_key, app_secret):
        """Create a SinchSMS client with the provided app_key and app_secret.

           Visit your dashboard at sinch.com to locate your application key and secret.
           These can be found under apps/credentials section.
        """
        b64bytes = base64.b64encode(('application:%s:%s' % (app_key, app_secret)).encode())
        self._auth = 'basic %s' % b64bytes.decode('ascii')

    def _request(self, url, values=None):
        """ Send a request and read response.

            Sends a get request if values are None, post request otherwise.
        """
        if values:
            json_data = json.dumps(values)
            request = urllib2.Request(url, json_data.encode())
            request.add_header('content-type', 'application/json')
            request.add_header('authorization', self._auth)
            connection = urllib2.urlopen(request)
            response = connection.read()
            connection.close()
        else:
            request = urllib2.Request(url)
            request.add_header('authorization', self._auth)
            connection = urllib2.urlopen(request)
            response = connection.read()
            connection.close()

        try:
            result = json.loads(response.decode())
        except ValueError as exception:
            return {'errorCode': 1, 'message': str(exception)}

        return result

    def send_message(self, to_number, message, from_number=None):
        """ Send a message to the specified number and return a response dictionary.

            The numbers must be specified in international format starting with a '+'.
            Returns a dictionary that contains a 'MessageId' key with the sent message id value or
            contains 'errorCode' and 'message' on error.

            Possible error codes:
                 40001 - Parameter validation
                 40002 - Missing parameter
                 40003 - Invalid request
                 40100 - Illegal authorization header
                 40200 - There is not enough funds to send the message
                 40300 - Forbidden request
                 40301 - Invalid authorization scheme for calling the method
                 50000 - Internal error
        """

        values = {'Message': message}
        if from_number is not None:
            values['From'] = from_number

        return self._request(self.SEND_SMS_URL + to_number, values)

    def check_status(self, message_id):
        """ Request the status of a message with the provided id and return a response dictionary.

            Returns a dictionary that contains a 'status' key with the status value string or
            contains 'errorCode' and 'message' on error.

            Status may have one of four values:
                Pending - The message is in the process of being delivered.
                Successful - The message has been delivered to the recipient.
                Unknown - The status of the provided message id is not known.
                Faulted - The message has not been delivered, this can be due to an
                          invalid number for instance.
        """

        return self._request(self.CHECK_STATUS_URL + str(message_id))

def _main():
    """ A simple demo to be used from command line. """
    import sys

    def log(message):
        print(message)

    def print_usage():
        log('usage: %s <application key> <application secret> send <number> <message> <from_number>' % sys.argv[0])
        log('       %s <application key> <application secret> status <message_id>' % sys.argv[0])

    if len(sys.argv) > 4 and sys.argv[3] == 'send':
        key, secret, number, message = sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5]
        client = SinchSMS(key, secret)
        if len(sys.argv) > 6:
            log(client.send_message(number, message, sys.argv[6]))
        else:
            log(client.send_message(number, message))
    elif len(sys.argv) > 3 and sys.argv[3] == 'status':
        key, secret, message_id = sys.argv[1], sys.argv[2], sys.argv[4]
        client = SinchSMS(key, secret)
        log(client.check_status(message_id))
    else:
        print_usage()
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    _main()
