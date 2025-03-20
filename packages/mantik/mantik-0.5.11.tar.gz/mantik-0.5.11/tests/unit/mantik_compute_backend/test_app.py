import fastapi

import mantik_compute_backend.app as _app
import mantik_compute_backend.exceptions as _exceptions


def test_create_app():
    docs_url = "/foo"
    app = _app.create_app(
        docs_url=docs_url,
        redoc_url="/bar",
        openapi_url="/baz.json",
    )
    assert isinstance(app, fastapi.FastAPI)
    route_paths = [route.path for route in app.routes]
    assert "/submit/{experiment_id}" in route_paths
    assert docs_url in route_paths
    exception_handlers = app.exception_handlers
    assert _exceptions.unicore_exception_handler in exception_handlers.values()
