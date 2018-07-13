from framework.common.string_utilities import get_random_string

instance_id = 0


def create_testtacker():
    test_id = get_random_string(4)
    global instance_id
    instance_id += 1
    result = {
        "Interface Language": "English",
        "Label": "auto_testtacker_{}_{}".format(test_id, instance_id),
        "Login": "testtacker_{}_{}".format(test_id, instance_id),
        "Password": "change_me",
        "Repeat password": "change_me",
    }
    return result
