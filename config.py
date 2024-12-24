from __future__ import annotations

import logging
import typing as t
from pathlib import Path

from sqlmesh.core.config import (
    Config,
    ConnectionConfig,
    GatewayConfig,
    ModelDefaultsConfig,
)
from sqlmesh.dbt.context import DbtContext
from sqlmesh.dbt.loader import DbtLoader
from sqlmesh.dbt.profile import Profile

logger = logging.getLogger(__name__)

if t.TYPE_CHECKING:
    pass


def sqlmesh_config(
    project_root: t.Optional[Path] = None,
    state_connection: t.Optional[ConnectionConfig] = None,
    dbt_target_names: t.Optional[t.List[t.Optional[str]]] = [None],
    variables: t.Optional[t.Dict[str, t.Any]] = None,
    register_comments: t.Optional[bool] = None,
    **kwargs: t.Any,
) -> Config:
    project_root = project_root or Path()
    context = DbtContext(project_root=project_root)
    profiles = [
        Profile.load(context, target_name=dbt_target_name)
        for dbt_target_name in dbt_target_names
    ]
    model_defaults = kwargs.pop("model_defaults", ModelDefaultsConfig())
    if model_defaults.dialect is None:
        model_defaults.dialect = profiles[0].target.dialect

    target_to_sqlmesh_args = {}
    if register_comments is not None:
        target_to_sqlmesh_args["register_comments"] = register_comments

    gateways = {}
    for profile in profiles:
        gateways[profile.target_name] = GatewayConfig(
            connection=profile.target.to_sqlmesh(**target_to_sqlmesh_args),
            state_connection=state_connection,
        )
    default_gateway = (
        profiles[0].target_name
        if "gateways" not in kwargs and len(profiles) > 0
        else ""
    )
    return Config(
        loader=DbtLoader,
        model_defaults=model_defaults,
        variables=variables or {},
        disable_anonymized_analytics=True,
        **{
            "default_gateway": default_gateway,
            "gateways": gateways,  # type: ignore
            **kwargs,
        },
    )


config = sqlmesh_config(
    Path(__file__).parent,
    dbt_target_names=["dev", "prod"],
    # state_connection=DuckDBConnectionConfig(database="local.duckdb"),
)
