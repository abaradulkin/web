from allure import step
from requests import Session


__BASE_URL = "http://spielplatz.taocloud.org/sprint80/"
__HEADERS = {"Accept": "application/json"}
__USERNAME = "admin"


def __request(uri, parameters=None):
    url = __BASE_URL + uri
    request_method = 'GET'
    if parameters:
        request_method = 'POST'
    session = Session()
    session.auth = (__USERNAME, __USERNAME)
    response = session.request(
        request_method,
        url,
        headers=__HEADERS,
        data=parameters,
    )
    response.raise_for_status()
    return response.json()


@step("Create item throw API")
def create_item(item_name):
    assert __request("taoQtiItem/RestQtiItem/createQtiItem/", parameters={"label": item_name})["success"]


# Still not work
def export_item(item_id):
    print(__request("taoQtiItem/RestQtiItem/export/", parameters={"id": item_id}))
