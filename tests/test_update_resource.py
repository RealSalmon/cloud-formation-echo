import index
from test_index import get_event


def test_update_resource():
    event = get_event()
    response = index.update_resource(event, dict())
    assert response['PhysicalResourceId'] == event['ResourceProperties']['Echo']
