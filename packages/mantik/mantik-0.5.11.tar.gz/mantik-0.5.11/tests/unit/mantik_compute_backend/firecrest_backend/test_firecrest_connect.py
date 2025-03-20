import functools

import firecrest
import pytest

import mantik.testing as testing
import mantik_compute_backend.firecrest._exceptions as _exceptions
import mantik_compute_backend.firecrest.connect as _connect


@pytest.mark.parametrize(
    ("login_successful", "expected"),
    [
        (False, _exceptions.AuthenticationFailedException()),
        (True, testing.firecrest.FakeClient),
    ],
)
def test_create_firecrest_api_connection(
    expect_raise_if_exception, monkeypatch, login_successful, expected
):
    monkeypatch.setattr(
        firecrest,
        "Firecrest",
        testing.firecrest.FakeClient,
    )
    monkeypatch.setattr(
        firecrest,
        "ClientCredentialsAuth",
        functools.partial(
            testing.firecrest.FakeClientCredentialsAuth,
            login_successful=login_successful,
        ),
    )
    with expect_raise_if_exception(expected):
        result = _connect.create_firecrest_api_connection(
            token_url="test-token-url",
            api_url="test-api-url",
            user="test-user",
            password="test-password",
        )
        assert isinstance(result, expected)
