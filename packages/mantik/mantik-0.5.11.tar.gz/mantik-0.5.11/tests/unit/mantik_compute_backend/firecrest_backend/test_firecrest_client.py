import logging
import pathlib

import mantik.testing as testing
import mantik_compute_backend.firecrest as firecrest
import mantik_compute_backend.firecrest._exceptions as firecrest_exceptions


class TestFirecrestClient:
    def test_get_scratch_fails_for_not_scratch_or_home_given(
        self, expect_raise_if_exception
    ):
        machine = "test-machine"
        parameters = testing.firecrest.FakeParameters(
            storage=[
                testing.firecrest.FakeParameter(
                    name="FILESYSTEMS",
                    unit="",
                    value=[
                        {
                            "mounted": [
                                "/project",
                            ],
                            "system": machine,
                        },
                    ],
                    description="",
                ),
            ],
        )

        client = firecrest.client.Client(
            client=testing.firecrest.FakeClient(parameters=parameters),
            machine=machine,
            account=testing.firecrest.USER_NAME,
            sleep_time=0,
        )

        with expect_raise_if_exception(firecrest_exceptions.FirecrestError()):
            client._get_scratch_dir()

    def test_get_scratch_dir_for_duplicate_scratch_and_machine(self):
        machine = "test-machine"
        parameters = testing.firecrest.FakeParameters(
            storage=[
                testing.firecrest.FakeParameter(
                    name="FILESYSTEMS",
                    unit="",
                    value=[
                        {
                            "mounted": [
                                "/scratch",
                                "/scratch",
                            ],
                            "system": machine,
                        },
                        {
                            "mounted": [
                                "/scratch",
                                "/scratch",
                            ],
                            "system": machine,
                        },
                    ],
                    description="",
                ),
            ],
        )
        expected = pathlib.Path(
            f"/scratch/{testing.firecrest.USER_NAME}/mantik"
        )

        client = firecrest.client.Client(
            client=testing.firecrest.FakeClient(parameters=parameters),
            machine=machine,
            account=testing.firecrest.USER_NAME,
            sleep_time=0,
        )

        result = client._get_scratch_dir()

        assert result == expected

    def test_get_scratch_dir_from_home_if_no_scratch_given(self):
        machine = "test-machine"
        parameters = testing.firecrest.FakeParameters(
            storage=[
                testing.firecrest.FakeParameter(
                    name="FILESYSTEMS",
                    unit="",
                    value=[
                        {
                            "mounted": [
                                "/home",
                            ],
                            "system": machine,
                        },
                    ],
                    description="",
                ),
            ],
        )
        expected = pathlib.Path(f"/home/{testing.firecrest.USER_NAME}/mantik")

        client = firecrest.client.Client(
            client=testing.firecrest.FakeClient(parameters=parameters),
            machine=machine,
            account=testing.firecrest.USER_NAME,
            sleep_time=0,
        )

        result = client._get_scratch_dir()

        assert result == expected

    def test_upload_files_to_run_directory(self, caplog):
        caplog.set_level(logging.INFO)
        run_dir = pathlib.Path("/path/to/remote/mantik/mlflow-run-id")
        files = [
            pathlib.Path("/absolute/path/to/file1.py"),
            pathlib.Path("/absolute/path/to/folder/file2.py"),
        ]
        expected_source_and_target_paths = [
            "Uploading file /absolute/path/to/file1.py to "
            "/path/to/remote/mantik/mlflow-run-id",
            "Uploading file /absolute/path/to/folder/file2.py to "
            "/path/to/remote/mantik/mlflow-run-id/folder",
        ]
        client = firecrest.client.Client(
            client=testing.firecrest.FakeClient(),
            machine="daint",
            account="test-account",
            sleep_time=0,
        )

        client._upload_files_to_run_directory(run_dir=run_dir, files=files)

        for path in expected_source_and_target_paths:
            assert (
                path in caplog.text
            ), f"Path '{path}' not found in caplog.text"

    def test_upload_files_to_run_directory_fails(
        self, expect_raise_if_exception
    ):
        run_dir = pathlib.Path("/path/to/remote/mantik/mlflow-run-id")
        files = [
            pathlib.Path("/absolute/path/to/file1.py"),
        ]
        client = firecrest.client.Client(
            client=testing.firecrest.FakeClient(
                upload_status=testing.firecrest.UploadStatus.FAILED
            ),
            machine="daint",
            account="test-account",
            sleep_time=0,
        )

        with expect_raise_if_exception(firecrest_exceptions.FirecrestError()):
            client._upload_files_to_run_directory(run_dir=run_dir, files=files)
