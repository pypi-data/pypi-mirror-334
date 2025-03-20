import pytest

import mantik.utils.credentials as credentials
import mantik.utils.env as env


@pytest.fixture()
def token():
    return (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
        "kpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ."
        "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )


@pytest.fixture()
def sub():
    return "1234567890"


def test_get_sub_from_token(token, sub):
    assert credentials._get_sub_from_token(token) == sub


def test_ssh_credentials():
    """
    Given I don't have SSH private key or password
    When  I instantiate the SSH credentials from env vars
    Then  I do not get a failure
    And   the credentials are set as None
    """
    with env.env_vars_overwrite_temporarily(
        {credentials.SSH_USERNAME_ENV_VAR: "fake user"}
    ):
        ssh_creds = credentials.SSHCredentials.from_env_vars()

    assert ssh_creds.password is None
    assert ssh_creds.private_key is None
