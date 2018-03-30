from uuid import uuid4
import index


def get_event():
    return {
        'StackId': str(uuid4()),
        'RequestId': str(uuid4()),
        'LogicalResourceId': str(uuid4()),
        'RequestType': 'Create',
        'ResourceProperties': {'Echo': 'ohai'},
    }


def test_empty_params():
    event = get_event()
    del event['ResourceProperties']
    response = index.lambda_handler(event)
    assert response['Status'] == 'FAILED'
    assert response['StackId'] == event['StackId']
    assert response['LogicalResourceId'] == event['LogicalResourceId']
    assert response['RequestId'] == event['RequestId']
    assert response['Reason'] == index.MSG_EMPTY_PROPS


def test_no_echo():
    event = get_event()
    del event['ResourceProperties']['Echo']
    response = index.lambda_handler(event)
    assert response['Status'] == 'FAILED'
    assert response['StackId'] == event['StackId']
    assert response['LogicalResourceId'] == event['LogicalResourceId']
    assert response['RequestId'] == event['RequestId']
    assert response['Reason'] == index.MSG_MISSING_ECHO


def test_delete():
    event = get_event()
    event['RequestType'] = 'Delete'
    response = index.lambda_handler(event)
    assert response['Status'] == 'SUCCESS'
    assert response['StackId'] == event['StackId']
    assert response['LogicalResourceId'] == event['LogicalResourceId']
    assert response['RequestId'] == event['RequestId']


def test_create():
    event = get_event()
    event['RequestType'] = 'Create'
    response = index.lambda_handler(event)
    assert response['Status'] == 'SUCCESS'
    assert response['StackId'] == event['StackId']
    assert response['LogicalResourceId'] == event['LogicalResourceId']
    assert response['RequestId'] == event['RequestId']
    assert response['PhysicalResourceId'] == event['ResourceProperties']['Echo']


def test_update():
    event = get_event()
    event['RequestType'] = 'Update'
    response = index.lambda_handler(event)
    assert response['Status'] == 'SUCCESS'
    assert response['StackId'] == event['StackId']
    assert response['LogicalResourceId'] == event['LogicalResourceId']
    assert response['RequestId'] == event['RequestId']
    assert response['PhysicalResourceId'] == event['ResourceProperties']['Echo']


def test_send_fail():
    event = get_event()
    event['ResponseURL'] = 'http://httpbin.org?bleh=1'
    response = index.send_fail(event, {'blah': 'bleh'}, 'beyond hope')
    assert response['blah'] == 'bleh'
    assert response['Reason'] == 'beyond hope'
    assert response['Status'] == 'FAILED'


def test_send_fail_unknown():
    event = get_event()
    event['ResponseURL'] = 'http://httpbin.org?bleh=1'
    response = index.send_fail(event, {'blah': 'bleh'}, None)
    assert response['blah'] == 'bleh'
    assert response['Reason'] == index.MSG_UNKNOWN_ERROR
    assert response['Status'] == index.FAILED


def test_send_response():
    event = get_event()
    event['ResponseURL'] = 'http://httpbin.org?bleh=1'
    response = index.send_response(event, {'blah': 'bleh'}, index.SUCCESS, None)
    assert response['Status'] == index.SUCCESS
    assert response['blah'] == 'bleh'


def test_bad_request_type():
    event = get_event()
    event['ResponseURL'] = 'http://httpbin.org?bleh=1'
    event['RequestType'] = 'yadda'
    response = index.lambda_handler(event)
    assert response['Status'] == index.FAILED
    assert response['Reason'] == index.MSG_UNKNOWN_REQUEST % "yadda"
