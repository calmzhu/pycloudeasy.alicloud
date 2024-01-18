import pytest

from cloudeasy.github.manager import GitHubUserManager


@pytest.fixture(scope="function")
def user(pat):
    return GitHubUserManager(pat)


class TestUser:

    def test_list_emails(self, user):
        emails = user.list_user_emails()
        assert len(emails) > 0

    def test_list_user_public_email(self, user):
        public_emails = user.list_user_public_emails()
        assert len(public_emails) > 0

    def test_get_user_profile(self, user):
        profile = user.get_user_profile()
        assert profile['type'] == 'User'
