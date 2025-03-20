from __future__ import annotations

import os
from pathlib import PosixPath

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, CliSubCommand, SettingsConfigDict

# This is a sample subcommand parser
#
# class ServerSettings(BaseModel):
#     """
#     This is the CLI settings / flags for the 'server' subcommand
#     """
#
#     listen_addr: str = Field(
#         description="Listen address for the HTTP server",
#         default="127.0.0.1:8080",
#     )


class Settings(BaseSettings):
    """
    This is your CLI settings.
    It comes with data validation and is 12-factor app compliant.
    """

    config_file: PosixPath = (
        PosixPath(os.getenv("XDG_CONFIG_HOME", "~/.config")).expanduser()
        / "clicamap2cal/config.yaml"
    )
    debug: bool = False

    username: str
    password: str

    # sub-commands example
    # See https://docs.pydantic.dev/latest/concepts/pydantic_settings/#subcommands-and-positional-arguments
    # server: CliSubCommand[ServerSettings]

    model_config = SettingsConfigDict(
        env_prefix="clicamap2cal_",
        env_nested_delimiter="__",
        env_file=".env",
        env_file_encoding="utf-8",
        nested_model_default_partial_update=True,
        cli_parse_args=True,
        cli_kebab_case=True,
        cli_implicit_flags=True,
    )
