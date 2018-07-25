from allure import step
from requests import Session, utils
from pprint import pprint


__BASE_URL = "http://spielplatz.taocloud.org/sprint81/"
__HEADERS = {"Accept": "application/json"}
__USERNAME = "admin"


def __get_request(uri):
    url = __BASE_URL + uri
    request_method = 'GET'
    session = Session()
    session.auth = (__USERNAME, __USERNAME)
    response = session.request(
        request_method,
        url,
        headers=__HEADERS,
    )
    response.raise_for_status()
    return response.json()


def __post_request(uri, parameters=None):
    url = __BASE_URL + uri
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


def __delete_request(uri, parameters=None):
    url = __BASE_URL + uri
    request_method = 'DELETE'
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
def create_item(item_name=None):
    #assert __get_request("taoQtiItem/RestQtiItem/createQtiItem/", parameters={"label": item_name})["success"]
    print(__post_request("taoQtiItem/RestQtiItem/createQtiItem/", parameters={"label": item_name}))


# Still not work
def export_item(item_id):
    print(__get_request("taoQtiItem/RestQtiItem/export/", parameters={"id": item_id}))


def get_testtakers_list():
    print(__get_request("taoSubjects/RestSubjects"))


def get_items_list(item="Item"):
    return __get_request("tao{0}/Rest{0}".format(item))


def create_item_new(item_label, item="Item"):
    print(__delete_request("tao{0}/Rest{0}".format(item), parameters={"uri": item_label}))


def delete_item(item_label, uri, item="Item"):
    print("Delete", item_label, uri)
    __delete_request("{}?uri={}".format("tao{0}/Rest{0}".format(item), utils.quote(uri)))



#for instance in ["Items", "Tests"]:
for instance in ["Items"]:
    result_raw = get_items_list(instance)
    pprint(result_raw)
    result = {}
    break

    for item in result_raw['data']:
        for property in item['properties']:
            if property['predicateUri'] == 'http://www.w3.org/2000/01/rdf-schema#label':
                result[property['values'][0]['value']] = item['uri']
                break

    for item, uri in result.items():
        if 'auto_' in item:
            delete_item(item, uri, instance)
