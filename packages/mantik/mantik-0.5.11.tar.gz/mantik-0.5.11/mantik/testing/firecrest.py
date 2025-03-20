import enum
import typing as t

import firecrest

USER_NAME = "test-account"


class UploadStatus(enum.Enum):
    SUCCESS = "114"
    FAILED = "115"


class FakeParameter(t.TypedDict):
    name: str
    unit: str
    value: t.Any
    description: str


class FakeParameters(t.TypedDict):
    storage: t.List[FakeParameter]
    utilities: t.List[FakeParameter] = None


class FakeExternalUpload(firecrest.ExternalUpload):
    def __init__(self, status: UploadStatus):
        self._status = status
        self._in_progress = iter([True, False])

    def finish_upload(self) -> None:
        return None

    @property
    def in_progress(self) -> bool:
        return next(self._in_progress)

    @property
    def status(self) -> str:
        return self._status.value


class FakeJobSubmit(t.TypedDict):
    firecrest_taskid: str
    job_data_err: str
    job_data_out: str
    job_file: str
    job_file_err: str
    job_file_out: str
    jobid: int
    result: str


class FakeJobAcct(t.TypedDict):
    jobid: str
    name: str
    nodelist: str
    nodes: str
    partition: str
    start_time: str
    state: str
    time: str
    time_left: str
    user: str


class FakeClient(firecrest.Firecrest):
    def __init__(
        self,
        firecrest_url: str = "test-firecrest-url",
        authorization: t.Any = "test-authorization",
        verify: t.Union[str, bool, None] = None,
        sa_role: str = "firecrest-sa",
        job_status: str = "COMPLETED",
        parameters: t.Optional[FakeParameters] = None,
        upload_status: UploadStatus = UploadStatus.SUCCESS,
    ):
        self._firecrest_url = firecrest_url
        self._authorization = authorization
        self._verify = verify
        self._sa_role = sa_role
        self._job_status = job_status
        self._parameters = parameters
        self._upload_status = upload_status

    def mkdir(self, machine: str, target_path: str, p: bool = None) -> None:
        return None

    def parameters(self) -> FakeParameters:
        return self._parameters or FakeParameters(
            storage=[
                FakeParameter(
                    name="FILESYSTEMS",
                    unit="",
                    value=[
                        {
                            "mounted": [
                                "/scratch/snx3000",
                                "/project",
                                "/store",
                            ],
                            "system": "daint",
                        },
                        {
                            "mounted": ["/capstor/scratch/cscs"],
                            "system": "eiger",
                        },
                    ],
                    description="",
                ),
                FakeParameter(
                    name="OBJECT_STORAGE",
                    unit="",
                    value="swift",
                    description="",
                ),
                FakeParameter(
                    name="STORAGE_TEMPURL_EXP_TIME",
                    unit="seconds",
                    value="604800",
                    description="",
                ),
                FakeParameter(
                    name="STORAGE_MAX_FILE_SIZE",
                    unit="MB",
                    value="1024000",
                    description="",
                ),
            ],
            utilities=[
                FakeParameter(name="", unit="", value="", description="")
            ],
        )

    def whoami(self, machine=None) -> t.Optional[str]:
        return USER_NAME

    def external_upload(
        self, machine: str, source_path: str, target_path: str
    ) -> FakeExternalUpload:
        return FakeExternalUpload(status=self._upload_status)

    def submit(
        self,
        machine: str,
        job_script: t.Optional[str] = None,
        local_file: t.Optional[bool] = True,
        script_str: t.Optional[str] = None,
        script_local_path: t.Optional[str] = None,
        script_remote_path: t.Optional[str] = None,
        account: t.Optional[str] = None,
        env_vars: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> FakeJobSubmit:
        return FakeJobSubmit(
            firecrest_taskid="test-task-id-submit",
            job_data_err="",
            job_data_out="",
            job_file="",
            job_file_err="",
            job_file_out="",
            jobid="test-job-id",
            result="",
        )

    def poll(
        self,
        machine: str,
        jobs: t.Sequence[t.Union[str, int]] = None,
        start_time: str = None,
        end_time: str = None,
    ) -> t.List[FakeJobAcct]:
        return [
            FakeJobAcct(
                jobid="test-job-id",
                name="test-job",
                nodelist="None assigned",
                nodes="1",
                partition="test-partition",
                start_time="Unknown",
                state=self._job_status,
                time="Unknown",
                time_left="Unknown",
                user="test-user",
            )
        ]

    def poll_active(
        self, machine: str, jobs: t.Sequence[t.Union[str, int]] = None
    ) -> t.List:
        return []


class FakeClientCredentialsAuth:
    def __init__(
        self,
        client_id: str = "test-user",
        client_secret: str = "test-password",
        token_uri: str = "test-token-uri",
        login_successful: bool = True,
    ):
        self._client_id = client_id
        self._client_secret = client_secret
        self._token_uri = token_uri
        if login_successful:
            self.login_successful = True
        else:
            self.login_successful = False

    def get_access_token(self) -> str:
        if self.login_successful:
            return "test-token"
        else:
            raise firecrest.ClientsCredentialsException(
                responses=["test-response"]
            )
