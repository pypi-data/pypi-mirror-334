import mantik_compute_backend.unicore.exceptions as exceptions


def test_unicore_exception():
    exc = exceptions.UnicoreError("Test")
    assert str(exc) == "Test"


def test_authentication_failed_exception():
    exc = exceptions.AuthenticationFailedException("Test")
    assert str(exc) == "Test"
    # Make sure the error inherits from UnicoreError
    assert exceptions.UnicoreError in exc.__class__.__bases__
