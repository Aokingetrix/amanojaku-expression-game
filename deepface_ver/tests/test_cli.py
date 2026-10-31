from __future__ import annotations

import os
import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    ("arguments", "exit_code", "output_name", "message"),
    [
        (["--help"], 0, "stdout", "あまのじゃくゲーム"),
        (["--window-size", "tiny"], 2, "stderr", "画面サイズ"),
    ],
)
def test_japanese_cli_output_survives_non_japanese_redirected_encoding(
    arguments, exit_code, output_name, message
):
    environment = dict(os.environ, PYTHONIOENCODING="cp1252", PYTHONUTF8="0")
    result = subprocess.run(
        [sys.executable, "-m", "deepface_ver.scripts.main", *arguments],
        capture_output=True,
        env=environment,
        timeout=15,
        check=False,
    )
    assert result.returncode == exit_code, result.stderr.decode("utf-8", errors="replace")
    assert message in getattr(result, output_name).decode("utf-8")
