import pytest

class TestCase:

    @pytest.fixture(autouse=True)
    def django_test_environment(self, django_test_environment):
        pass