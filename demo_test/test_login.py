from allure import severity, feature

@feature("Login")
class TestLogin(object):

    @feature("Smoke")
    @severity("critical")
    def test_base_login(self):
        print("Success")

    @severity("critical")
    def test_login_with_empty_field(self):
        pass

    @severity("normal")
    def test_login_with_wrong_pass(self):
        assert 0, "You couldn't pass"
