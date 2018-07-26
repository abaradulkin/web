import pytest
from demo_test import factory


@pytest.fixture(scope="class", name="items")
def create_3_items():
    items = (factory.get_item() for i in range(3))
    #items = [factory.get_item() for i in range(3)]
    print(type(items))
    yield items


@pytest.fixture(scope="class", name="test")
def create_1_test():
    yield factory.get_test()


class TestDemo(object):
    def test_1(self, items):
        for item in items:
            print(item)
        assert 1

    def test_2(self, test):
        print(test)
        assert 1

    def test_3(self, items, test):
        for item in items:
            print(item)
        print(test)
        assert 1