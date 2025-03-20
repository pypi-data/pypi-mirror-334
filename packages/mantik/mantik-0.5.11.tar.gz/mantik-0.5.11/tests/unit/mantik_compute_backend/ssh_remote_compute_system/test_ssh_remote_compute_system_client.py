import io
import pathlib
import unittest.mock

import paramiko
import pytest

import mantik_compute_backend.ssh_remote_compute_system.client as ssh_client
import mantik_compute_backend.ssh_remote_compute_system.exceptions as ssh_exceptions  # noqa E501


def _byte_stream(value: str) -> io.BytesIO:
    return io.BytesIO(value.encode("utf-8"))


@pytest.fixture
def sample_run_id() -> str:
    return "123"


@pytest.fixture
def sample_run_directory(sample_run_id) -> pathlib.Path:
    return pathlib.Path(f"mantik-runs/{sample_run_id}")


def test_run_directory(sample_run_id, sample_run_directory) -> None:
    assert (
        ssh_client.run_directory(run_id=sample_run_id) == sample_run_directory
    )


def _raise_file_not_found_error():
    raise FileNotFoundError


def test_create_remote_dir() -> None:
    """
    Given I don't have a remote directory
    When  I request to create it
    And   the filepath contains intermediate folders which
          do not exist
    Then  the directory gets created
    And   all the intermediate directories also get created
    """
    paths_which_would_be_created = []

    sftp_mock = unittest.mock.Mock()
    sftp_mock.stat = lambda remote_dir: _raise_file_not_found_error()
    sftp_mock.mkdir = lambda remote_dir: paths_which_would_be_created.append(
        remote_dir
    )

    sample_remote_dir = pathlib.Path("root/home/user/folder")
    ssh_client.create_remote_dir(sftp=sftp_mock, remote_dir=sample_remote_dir)

    assert paths_which_would_be_created == [
        "root",
        "root/home",
        "root/home/user",
        "root/home/user/folder",
    ]


@unittest.mock.patch(
    "mantik_compute_backend.ssh_remote_compute_system.client.create_remote_dir"
)
def test_secure_copy_files_to_ssh_server(create_remote_dir_patch) -> None:
    """
    Given I have a set of files
    When  I request to copy them to an SSH server
    Then  the correct `put` command is called
          for all the files
    And   their new filepaths point to the server
    """
    sample_remote_dir = pathlib.Path("mantik-run/123")
    sample_files = [
        pathlib.Path(i_path) for i_path in ["file1.txt", "folder2/file2.txt"]
    ]

    uploaded_file_paths = []

    sftp_mock = unittest.mock.Mock()
    sftp_mock.put = (
        lambda local_file_path, remote_path: uploaded_file_paths.append(
            remote_path
        )
    )

    ssh_client_mock = unittest.mock.Mock()
    ssh_client_mock.open_sftp.return_value = sftp_mock

    ssh_client.secure_copy_files_to_ssh_server(
        ssh_client=ssh_client_mock,
        target_dir=sample_remote_dir,
        files=sample_files,
    )

    expected_uploaded_files = [
        str(sample_remote_dir / i_file) for i_file in sample_files
    ]
    create_remote_dir_patch.assert_called()
    assert uploaded_file_paths == expected_uploaded_files


def test_submit_slurm_job_with_files() -> None:
    """
    When  I request to submit a mantik run to an SSH server
    Then
        - Run directory gets created on SSH server
        - Run files are copied over to SSH server
        - The run gets queues as a SLURM job
        - SLURM job ID gets returned
    """

    SAMPLE_INPUT_FILES = [
        pathlib.Path("home/user/first.file"),
        pathlib.Path("home/user/mantik.sh"),
    ]
    SAMPLE_RUN_DIR = pathlib.Path("mantik-runs/123")
    paths_which_would_be_uploaded = []

    # setup mocks
    sftp_mock = unittest.mock.Mock()
    sftp_mock.put = lambda local_file_path, remote_path: paths_which_would_be_uploaded.append(  # noqa E501
        remote_path
    )
    sftp_mock.stat = lambda remote_dir: _raise_file_not_found_error()

    ssh_client_mock = unittest.mock.Mock()
    ssh_client_mock.open_sftp.return_value = sftp_mock

    fake_stdout = _byte_stream("Submitted batch job fake-job-id")
    fake_stderr = _byte_stream("")

    ssh_client_mock.exec_command.return_value = (
        unittest.mock.Mock(),
        fake_stdout,
        fake_stderr,
    )

    # mock_get_slurm_job_id_from_stdout.return_value = "fake-job-id"
    # call function
    job = ssh_client.submit_slurm_job_with_files(
        connected_ssh_client=ssh_client_mock,
        bash_script_path=SAMPLE_RUN_DIR / pathlib.Path("home/user/mantik.sh"),
        files_to_upload=SAMPLE_INPUT_FILES,
        run_dir=SAMPLE_RUN_DIR,
    )

    expected_uploaded_files = [
        str(SAMPLE_RUN_DIR / i_file) for i_file in SAMPLE_INPUT_FILES
    ]

    assert paths_which_would_be_uploaded == expected_uploaded_files
    ssh_client_mock.exec_command.assert_called_once_with(
        "sbatch mantik-runs/123/home/user/mantik.sh"
    )
    assert job.id == "fake-job-id"


sample_rsa_key_string = """\
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAniaaz+wiZ2wBMUA/HThQVLQ9k7HS97JNXgNhlxMjtTb7Zmnu
jZGOGi2cOdjQJz91L09DRRPcGm8zlzu96ZNeqZgS7cmW2pKb5wIeKQgFATsXOw0R
hOd3wt65yUW7S1PzhhAFH4CqdtYjwzJyiPUmzgiXTYHiunrTSHoQ/DmuZanqVrXA
WmA7y5RqfRF5n17mlDgQPlow2KFbB2WWmkrO50OaHRdexbAYisvlsGIfhcVJynzF
BGxvP5XacQBgldca53SSHd+jJetdu+Ix9ugkaf8kOSYi9lujVEB/dlR/LEuY6TwW
m0Amf7PJhGgc9Iix2J29CMp1IyFVfgPNAh/GDwIDAQABAoIBAFw+JhPaJeLusu9Y
CrfvTaNqEXRgxq0keU25aSVly3D55b5BURuPZzPLoJB47kfGEoKKl7DluX5Nl+jA
tq9S/maqxXeeGffYhUhDCvZhsBGctpsBr1M2crrdj71eh7SS/boXA/Xw5Pw1QFys
wvMxEfYgOqfBd03PMAbY86k5t4ehnVxOgkEJ8B6bqgbKpaarrHjace98ZUUJ5mEh
tZz8Xz4J16QL2FEsYkddnqJM5r7u/sdU0GPVtA5aT246wkIPOcqAIvUHpuTKiOvC
IYJn+Pg+qcMGP9xZZIcUhjbTVwYsbB84fu1tkJ95qkq6ulJD3YqHeZsoAhZ6vBZH
cjUuDlkCgYEA1e7yG5wZy/C46kljAA9sEPbSZHx1R6Sabnh6vVo10vlcJ628ept3
pdP7xlFrmwIDmYWY1FG3tlve26hi9LppKqAwoa6YNbpN9A3pZh4hhKq3Ces7dAlF
9ZMsr7PkWuWvb7aNK0F4Oo2jI8ZacziU02uBbYQrHEH1K4nIjsIX0h0CgYEAvT+n
2LCO2kGUkQ4/F0kfpquz8T91ITxWTZLSPPk2YaZwFc6SiSgenTB5ipLIPxe9SKJ3
Wpiqqe14XVZu7RnG6x3e3LeQexmJuZoS/LghbAX6yJ7wcZNryQkO9EHBLAcY+yus
g5kvxkznXF8/cxeFomqxWwopBr30BH8e7k7sgRsCgYEApna2VvuBKyqViGAwM5TM
fuq/zUb2rxeKvxjqULqIFTDJH2rVtQWR9SvcxnUGaOgJSwUkZVlsvO4BnCQLU+hU
+sEI9lX3xB7Cl3vXuAkMBcIciRBMA79Pe4XYiKNOtdfxSdjfQeBAoDcj0St/qBZH
37bQUBo+vU8paYZd0499n5UCgYAx99TBihyt1BL+GdzesRgCUeO5FyA+HkhLQzDv
mH2bWu7NUzWtsUIkDuCIjikBP6tiukL5UMX/CAx32JKBWAUFn2VwsaccWanbr6rD
v3pTo2CMCCtEUcBr3FBufc4baeRWrTlnpdLPcQ7FfQCrytImCDW76/rZJN6BMW9h
TMV1cQKBgGplT2d5KjBxSBAY3iXumTsXntQDsENVXwff78AThX7rbKrCpbh+MT0m
BZQmrrjhfEsMM/3YyZZUMboID0LVBNroaB0DuwX3XXYNw1Ym09tcflCgOSB5a05s
dnZ30Gx+9oEx1KGWneYETXDUPxqgMa3kl956JrgWxy2+UyKo8mQi
-----END RSA PRIVATE KEY-----"""

sample_dsa_key_string = """\
-----BEGIN DSA PRIVATE KEY-----
MIIDTQIBAAKCAQEAj3k12bmq6b+r7Yh6z0lRtvMuxZ47rzcY6OrElh8+/TYG50NR
qcQYMzm4CefCrhxTm6dHW4XQEa24tHmHdUmEaVysDo8UszYIKKIv+icRCj1iqZNF
NAmg/mlsRlj4S90ggZw3CaAQV7GVrc0AIz26VIS2KR+dZI74g0SGd5ec7AS0NKas
LnXpmF3iPbApL8ERjJ/6nYGB5zONt5K3MNe540lZL2gJmHIVORXqPWuLRlPGM0WP
gDsypMLg8nKQJW5OP4o7CDihxFDk4YwaKaN9316hQ95LZv8EkD7VzxYj4VjUh8YI
6X8hHNgdyiPLbjgHZfgi40K+SEwFdjk5YBzWZwIdALr2lqaFePff3uf6Z8l3x4Xv
MrIzuuWAwLzVaV0CggEAFqZcWCBIUHBOdQKjl1cEDTTaOjR4wVTU5KXALSQu4E+W
5h5L0JBKvayPN+6x4J8xgtI8kEPLZC+IAEFg7fnKCbMgdqecMqYn8kc+kYebosTn
RL0ggVRMtVuALDaNH6g+1InpTg+gaI4yQopceMR4xo0FJ7ccmjq7CwvhLERoljnn
08502xAaZaorh/ZMaCbbPscvS1WZg0u07bAvfJDppJbTpV1TW+v8RdT2GfY/Pe27
hzklwvIk4HcxKW2oh+weR0j4fvtf3rdUhDFrIjLe5VPdrwIRKw0fAtowlzIk/ieu
2oudSyki2bqL457Z4QOmPFKBC8aIt+LtQxbh7xfb3gKCAQBP0RrX8gWXyHeWQg++
b67Zs3dNpdMn9wQo7Kwvf2H4mNtiC3NFdDpH7k5nM1x56vT6WSMBHvQYK1lESGeN
fSxnCThHo8iIkmb4sgemlE1euJ1DcTKhe6TclHcCrXBNj2OmuY2Oi8Nzj6G0g2HQ
4reuV8DFpxP0p11bO8fEk7mL2DMsGIwSXCHkPJxUxyM016oAHLapSr/tXpmKP1kQ
51cykgKAhBa/XiLhg/7JirvRRkeQf6uRfohg80mDBabaOb4wZvGF7em1uTycL4OW
VMYAqdbSHRbm8p3pG/JaqcNkhmGDMgPBcS+QdxADGhE5BZJuDwHU1WremvFX3TPn
xfWdAhw+k76LbnfdGfIUqucJBIbh9YnpjzhWZ8A9hL+J
-----END DSA PRIVATE KEY-----"""

sample_ecdsa_key_string = """\
-----BEGIN EC PRIVATE KEY-----
MIHcAgEBBEIBc+IJfN989qG3ygTtXCpkNhBvahHNFeRO/vVkuz8NhcdDPahUL7Z3
lHDhINccqPlCjlWAK9WemtsGAEu4ma2OEYCgBwYFK4EEACOhgYkDgYYABAEpR8BY
3J+9uu9bUyFnV96Y0CsEBF3bKBpz7xlhEjLUZ6MwGNAHBrzqUc5arCD6S5UGzJhz
XBnRT2Ir7mfNOsfb5wFe0+ugcElsYfvTOqgar02GdEnqq6QvZP4TM5rwYx0KNq7u
Ud4OVQaCZwpWRnN9tpXSFeFXHmc2PHqHzCpAnncrNg==
-----END EC PRIVATE KEY-----"""

sample_ed25519_key_string = """\
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACBWBVCBpi6gVwsFvIIGpAVt3BzfROEeHcYBN3RiF4VLdgAAAJAoA9cWKAPX
FgAAAAtzc2gtZWQyNTUxOQAAACBWBVCBpi6gVwsFvIIGpAVt3BzfROEeHcYBN3RiF4VLdg
AAAEBFus8OzEI0F9Ik8zwwLBEcZJ2QFGRSNRyAkU71wTkFslYFUIGmLqBXCwW8ggakBW3c
HN9E4R4dxgE3dGIXhUt2AAAABm5vbmFtZQECAwQFBgc=
-----END OPENSSH PRIVATE KEY-----"""


sample_broken_key_string = """\
1234-i'll-be-broken-forever-more"""


@pytest.mark.parametrize(
    "private_key_string,expected_key_type",
    (
        [sample_rsa_key_string, paramiko.RSAKey],
        [sample_dsa_key_string, paramiko.DSSKey],
        [sample_ecdsa_key_string, paramiko.ECDSAKey],
        [sample_ed25519_key_string, paramiko.Ed25519Key],
    ),
)
def test_get_private_key_from_key_string(
    private_key_string: str, expected_key_type
):
    parsed_key = ssh_client.get_private_key_from_key_string(
        private_key=private_key_string
    )
    assert isinstance(parsed_key, expected_key_type)


def test_get_private_key_from_key_string_invalid_key_raises_error():
    with pytest.raises(
        ssh_exceptions.SSHError, match="Private key is invalid."
    ):
        ssh_client.get_private_key_from_key_string(
            private_key=sample_broken_key_string
        )
