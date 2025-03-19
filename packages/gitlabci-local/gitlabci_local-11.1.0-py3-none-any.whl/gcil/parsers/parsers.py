#!/usr/bin/env python3

# Standard libraries
from argparse import Namespace
from sys import exc_info
from typing import Optional

# Components
from ..models.pipelines import Pipeline
from ..package.bundle import Bundle
from ..prints.colors import Colors
from ..types.yaml import YAML
from .gitlab import GitLab

# Parsers class, pylint: disable=too-few-public-methods
class Parsers:

    # Members
    __options: Namespace

    # Constructor
    def __init__(
        self,
        options: Namespace,
    ) -> None:

        # Prepare options
        self.__options = options

    # Read
    def read(self) -> Optional[Pipeline]:

        # Read GitLab CI YAML
        try:
            with open(
                    self.__options.configuration,
                    encoding='utf8',
                    mode='r',
            ) as configuration_data:
                data: YAML.Data = YAML.load(configuration_data)
                return GitLab(self.__options).parse(data)
        except YAML.Error as exc:
            print(' ')
            print(
                f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR:' \
                    f' {Colors.BOLD}{exc}{Colors.RESET}'
            )
            print(' ')
        except (FileNotFoundError, PermissionError):
            print(' ')
            print(
                f' {Colors.GREEN}{Bundle.NAME}: {Colors.RED}ERROR:' \
                    f' {Colors.BOLD}{str(exc_info()[1])}{Colors.RESET}'
            )
            print(' ')

        # Failure
        return None
