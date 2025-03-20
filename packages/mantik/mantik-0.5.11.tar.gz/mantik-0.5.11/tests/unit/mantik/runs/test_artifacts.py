import os
import uuid

import pytest

import mantik.runs.artifacts as artifacts


@pytest.mark.parametrize("unzip", [True, False])
def test_download_artifacts(
    mock_authentication,
    tmpdir,
    mock_get_artifacts_url,
    mock_get_url,
    info_caplog,
    unzip,
    zipped_file_name,
) -> None:
    project_id = uuid.uuid4()
    run_id = uuid.uuid4()
    with mock_get_artifacts_url as get_artifacts_url, mock_get_url as get_url:
        artifacts.download_artifacts(
            project_id=project_id,
            run_id=run_id,
            target_dir=str(tmpdir),
            unzip=unzip,
        )

        get_artifacts_url.assert_called()
        get_url.assert_called()
        if not unzip:
            assert (
                f"Successfully downloaded at {str(tmpdir)}/artifacts.zip"
                in info_caplog.text
            )
        else:
            assert (
                f"Artifacts successfully downloaded at {str(tmpdir)}"
                in info_caplog.text
            )
            assert zipped_file_name in os.listdir(tmpdir)
