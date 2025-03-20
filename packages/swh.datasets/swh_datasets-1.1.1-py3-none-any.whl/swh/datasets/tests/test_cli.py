# Copyright (C) 2019-2022  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os
from tempfile import TemporaryDirectory

from click.testing import CliRunner
import pytest

from swh.datasets.cli import datasets_cli_group


@pytest.mark.parametrize("exit_code", [0, 1])
def test_luigi(mocker, tmpdir, exit_code):
    """calls Luigi with the given configuration"""
    # bare bone configuration, to allow testing the compression pipeline
    # with minimum RAM requirements on trivial graphs
    runner = CliRunner()

    subprocess_run = mocker.patch("subprocess.run")
    subprocess_run.return_value.returncode = exit_code

    with TemporaryDirectory(suffix=".swh-datasets-test") as tmpdir:
        result = runner.invoke(
            datasets_cli_group,
            [
                "luigi",
                "--base-directory",
                f"{tmpdir}/base_dir",
                "--dataset-name",
                "2022-12-07",
                "--",
                "foo",
                "bar",
                "--baz",
                "qux",
            ],
            catch_exceptions=False,
        )
        assert result.exit_code == exit_code, result.output

    luigi_config_path = subprocess_run.mock_calls[0][2]["env"]["LUIGI_CONFIG_PATH"]
    subprocess_run.assert_called_once_with(
        [
            "luigi",
            "--module",
            "swh.export.luigi",
            "--module",
            "swh.graph.luigi",
            "--module",
            "swh.datasets.luigi",
            "foo",
            "bar",
            "--baz",
            "qux",
        ],
        env={"LUIGI_CONFIG_PATH": luigi_config_path, **os.environ},
    )
