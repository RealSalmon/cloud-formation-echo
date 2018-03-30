#! /usr/bin/env python

import http.client
import json
import logging
import os
from urllib.parse import urlparse
from uuid import uuid4


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get('LOGLEVEL', 'INFO').upper())

MSG_EMPTY_PROPS = 'Empty resource properties'
MSG_MISSING_ECHO = 'Required resource property "Echo" is not set'
MSG_UNKNOWN_ERROR = 'Execution error - See CloudWatch logs for ' \
                    'the Lambda function backing this custom resource for ' \
                    'details'
MSG_UNKNOWN_REQUEST = 'Unknown request type "%s"'
SUCCESS = 'SUCCESS'
FAILED = 'FAILED'


def delete_resource(response):
    return response


def create_resource(event, response):
    response['PhysicalResourceId'] = event['ResourceProperties']['Echo']
    return response


def update_resource(event, response):
    return create_resource(event, response)


def lambda_handler(event, context=None):

    reqtype = event.get('RequestType')
    rprops = event.get('ResourceProperties')

    response = {
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'Status': SUCCESS,
        'PhysicalResourceId': event.get('PhysicalResourceId', str(uuid4())),
        'Data': {}
    }

    # Make sure resource properties are there
    if rprops is None:
        return send_fail(event, response, MSG_EMPTY_PROPS)

    if 'Echo' not in rprops and reqtype != 'Delete':
        return send_fail(event, response, MSG_MISSING_ECHO)

    try:
        if reqtype == 'Delete':
            response = delete_resource(response)
        elif reqtype == 'Create':
            response = create_resource(event, response)
        elif reqtype == 'Update':
            response = update_resource(event, response)
        else:
            return send_fail(
                event, response, MSG_UNKNOWN_REQUEST % event['RequestType']
            )
    except Exception as E:
        send_fail(event, response, MSG_UNKNOWN_ERROR)
        raise E

    return send_response(event, response)


def send_response(request, response, status=None, reason=None):
    """ Send our response to the pre-signed URL supplied by CloudFormation
    If no ResponseURL is found in the request, there is no place to send a
    response. This may be the case if the supplied event was for testing.
    """
    if status is not None:
        response['Status'] = status

    if reason is not None:
        response['Reason'] = reason

    logger.debug('Response body is: %s', response)

    if 'ResponseURL' in request and request['ResponseURL']:
        url = urlparse(request['ResponseURL'])
        body = json.dumps(response)
        https = http.client.HTTPSConnection(url.hostname)
        logger.debug('Sending response to %s', request['ResponseURL'])
        https.request('PUT', url.path + '?' + url.query, body)
    else:
        logger.warning('No response sent (ResponseURL was empty)')

    return response


def send_fail(request, response, reason=None):
    if reason is not None:
        logger.error(reason)
    else:
        reason = MSG_UNKNOWN_ERROR

    return send_response(request, response, FAILED, reason)
