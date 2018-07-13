from allure import severity, feature

@feature("Account")
class TestLogin(object):

    @feature("Smoke")
    @severity("critical")
    def test_create_account(self):
        print("Success")

    @severity("critical")
    def test_account_and_fill_information_fields(self):
        pass

    @severity("normal")
    def test_try_create_account_without_email(self):
        assert 0, "You couldn't pass"
