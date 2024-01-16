import os

import pytest

from cloudeasy.github.gh_app_oauth import GithubAppOAuth


@pytest.fixture(scope="module")
def gh_oauth_client():
    return GithubAppOAuth(
        client_id=os.environ['GITHUB_APP_CLIENT_ID'],
        client_secret=os.environ['GITHUB_APP_CLIENT_SECRET']
    )


class TestGithubAppOAuth:
    @pytest.mark.skip(reason="Browser required")
    def test_build_request(self, gh_oauth_client):
        auth_url = gh_oauth_client.build_auth_url(redirect_uri="http://localhost:3000/login/github/callback")
        assert auth_url.startswith("https://")

    @pytest.mark.skip(reason="Browser required")
    def test_get_access_token(self, gh_oauth_client):
        code = os.environ['GITHUB_APP_AUTHORIZATION_CODE']
        access_token = gh_oauth_client.get_access_token(code)
        print(access_token)
