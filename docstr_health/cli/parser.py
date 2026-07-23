import argparse
from pathlib import Path

from ..core import __version__
from ..core.config import config


def get_parser():
    parser = argparse.ArgumentParser(
        prog="docstr-health",
        description="Health score and visualization for Python projects.",
    )

    parser.add_argument(
        "project_path",
        type=Path,
        nargs="?",
        default=Path("."),
        help="Path to the directory to check.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Show version and exit.",
    )

    main_group = parser.add_argument_group("basic parameters")

    main_group.add_argument(
        "--repo-url",
        type=str,
        help="Scan a project from a remote Git repository.",
    )

    main_group.add_argument(
        "--pypi-package",
        type=str,
        help="Scan a project from a remote PyPi package.",
    )

    main_group.add_argument(
        "--cache-dir",
        type=Path,
        default=config.get_cache_dir(),
        help=f"Directory for cached repositories (default: {config.get_cache_dir()})",
    )

    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Do not save cache for remote repositories.",
    )

    parser.add_argument(
        "--compact",
        action="store_true",
        help="Display only general statistics, hiding the list of functions.",
    )

    parser.add_argument(
        "--doc-modules",
        action="store_true",
        help="Check __doc__ of the files themselves",
    )

    parser.add_argument(
        "--ignore-tests",
        action="store_true",
        help="Ignore Test Units",
    )

    parser.add_argument(
        "--short-names",
        action="store_true",
        help="Replaces full path to the file with short ones",
    )

    measurement_group = parser.add_argument_group("parameters of methods measurement")

    measurement_group.add_argument(
        "--threshold-bad",
        type=int,
        help="",
        default=config.parameters["threshold_bad"],
    )

    measurement_group.add_argument(
        "--threshold-warning",
        type=int,
        help="",
        default=config.parameters["threshold_warning"],
    )

    measurement_group.add_argument(
        "--threshold-special",
        type=int,
        help="",
        default=config.parameters["threshold_special"],
    )

    measurement_group.add_argument(
        "--threshold-epic",
        type=int,
        help="",
        default=config.parameters["threshold_epic"],
    )

    # parser.add_argument(
    #     "--details-skipped",
    # )

    return parser
