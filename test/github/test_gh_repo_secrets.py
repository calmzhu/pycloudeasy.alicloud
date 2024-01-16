import os

import pytest

from cloudeasy.github.manager import RepoSecret


@pytest.fixture(scope="function")
def repo_secret(pat):
    return RepoSecret(pat)


@pytest.fixture(scope="session")
def gh_repo():
    return os.environ['GH_TEST_REPO'].split("/")


@pytest.fixture(scope="session")
def secret_meta():
    return "TEST_SECRET_NAME", "TEST_SECRET_VALUE"


class TestGithubRepoSecrets:

    @pytest.mark.run(order=1)
    def test_get_repo_public_key(self, repo_secret, gh_repo, cache):
        key = repo_secret.get_repo_public_key(*gh_repo)
        cache.set('PUBLIC_KEY', key)
        assert 'key' in key and 'key_id' in key

    @pytest.mark.run(order=2)
    def test_set_repo_secrets(self, repo_secret, gh_repo, cache, secret_meta):
        key = cache.get("PUBLIC_KEY", None)
        _NAME, _DATA = secret_meta
        gh_repo_owner, gh_repo_name = gh_repo
        secret = repo_secret.put_repo_secrets(
            gh_repo_owner, gh_repo_name, _NAME,
            data=_DATA,
            encrypted_key_id=key['key_id'],
            public_key=key['key'])
        assert secret is True

    @pytest.mark.run(order=2)
    def test_set_repo_secrets(self, repo_secret, gh_repo, cache):
        gh_repo_owner, gh_repo_name = gh_repo
        x = repo_secret.set_repo_secret(gh_repo_owner, gh_repo_name, "TEST_SECRET_NAME", "TEST_SECRET_VALUE")
        assert x is True

    @pytest.mark.run(order=3)
    def test_get_repo_secrets(self, repo_secret, gh_repo, cache, secret_meta):
        secret_name, secret_value = secret_meta
        gh_repo_owner, gh_repo_name = gh_repo
        secret = repo_secret.get_repo_secret(gh_repo_owner, gh_repo_name, secret_name)
        assert secret['name'] == secret_name

    @pytest.mark.run(order=3)
    def test_list_repo_secrets(self, repo_secret, gh_repo, cache):
        x = repo_secret.list_repo_secrets(*gh_repo)
        cache.set("SECRET_NAME", x["secrets"][0]['name'])
        assert bool(cache.get("SECRET_NAME", None)) is True
