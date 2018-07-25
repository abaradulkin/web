from framework.common.string_utilities import get_random_string
from collections import namedtuple

Group = namedtuple("Group", ["label"])
Group.__new__.__defaults__ = ("auto_group",)

Delivery = namedtuple("Delivery", ["label", "test", "group"])
Delivery.__new__.__defaults__ = ("auto_delivery", None, None)

Item = namedtuple("Item", ["label"])
Item.__new__.__defaults__ = ("auto_item",)

LTI = namedtuple("LTI", ["label", "key", "secret"])
LTI.__new__.__defaults__ = ("auto_item", None, None)

Test = namedtuple("Test", ["label"])
Test.__new__.__defaults__ = ("auto_test",)

User = namedtuple("User", ["label", "login", "language", "password", "role"])
User.__new__.__defaults__ = ("auto_testtaker", "auto_testtaker", "English", "change_me", "Test Taker")


class TaoObjectFactory(object):
    __instance_id = 0
    __group_pattern = "auto_group_{}_{}"
    __delivery_pattern = "auto_delivery_{}_{}"
    __item_pattern = "auto_item_{}_{}"
    __test_pattern = "auto_test_{}_{}"
    __testtaker_pattern = "auto_testtaker_{}_{}"

    def __init__(self, test_id=None):
        self.test_id = test_id if test_id else get_random_string(4)

    def create_group(self):
        self.__instance_id += 1
        return Group(self.__group_pattern.format(self.test_id, self.__instance_id))

    def create_delivery(self, test_obj=None, group_obj=None):
        self.__instance_id += 1
        return Delivery(label=self.__delivery_pattern.format(self.test_id, self.__instance_id),
                        test=test_obj, group=group_obj)

    def create_item(self):
        self.__instance_id += 1
        return Item(self.__item_pattern.format(self.test_id, self.__instance_id))

    def create_lti(self):
        self.__instance_id += 1
        return LTI(label="auto_lti_{}_{}".format(self.test_id, self.__instance_id),
                   key="auto_lti_key_{}_{}".format(self.test_id, self.__instance_id),
                   secret="auto_lti_secret_{}_{}".format(self.test_id, self.__instance_id))

    def create_test(self):
        self.__instance_id += 1
        return Test(self.__test_pattern.format(self.test_id, self.__instance_id))

    def create_user(self, label=None, login=None, language=None, password=None, role=None):
        self.__instance_id += 1
        label = label if label else self.__testtaker_pattern.format(self.test_id, self.__instance_id)
        login = login if login else label
        parameters = {"label": label, "login": login}
        if language:
            parameters["language"] = language
        if password:
            parameters["password"] = password
        if role:
            parameters["role"] = role
        result = User()
        return result._replace(**parameters)
