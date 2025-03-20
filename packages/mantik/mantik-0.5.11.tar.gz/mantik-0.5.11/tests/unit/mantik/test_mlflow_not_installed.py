def test_import_fails_without_mlflow_installed():
    try:
        import mantik.mlflow  # noqa: F401
    except ModuleNotFoundError as e:
        if "Install supported MLflow version" not in str(e):
            assert (
                False
            ), "MLflow import should fail with dedicated error message"
        else:
            raise e
