import index
from test_index import get_event


def test_create_resource():
    event = get_event()
    response = index.create_resource(event, dict())
    assert response['PhysicalResourceId'] == event['ResourceProperties']['Echo']
