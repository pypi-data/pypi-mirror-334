import os
import typing as t
import uuid

import mantik.authentication.auth as auth
import mantik.utils.env_vars as env_vars
import mantik.utils.mantik_api as mantik_api


def init(
    project_id: t.Optional[uuid.UUID] = None,
    run_id: t.Optional[str] = None,
    mantik_access_token: t.Optional[str] = None,
) -> None:
    """Initialise mantik for run bookkeeping

    Including:
    - bookkeep run infrastructure
    """
    try:
        project_id = project_id or os.environ[env_vars.PROJECT_ID_ENV_VAR]
        run_id = (
            run_id
            or os.getenv(env_vars.RUN_ID_ENV_VAR)
            or os.environ[env_vars.MLFLOW_RUN_ID_ENV_VAR]
        )
    except KeyError as e:
        raise RuntimeError(f"mantik.init() requires environment variable {e}")

    mantik_access_token = (
        mantik_access_token
        or os.getenv(env_vars.MANTIK_ACCESS_TOKEN_ENV_VAR)
        or auth.get_valid_access_token()
    )
    mantik_api.run.update_run_infrastructure(
        project_id=project_id,
        run_id=uuid.UUID(run_id),
        token=mantik_access_token,
        infrastructure=mantik_api.run.RunInfrastructure.from_system(),
    )
