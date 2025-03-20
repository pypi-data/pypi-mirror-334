"""
Tests for the Schoenfeld residuals.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def test_schoenfeld_residuals() -> None:
    """
    Run the script_schoenfeld_residuals.py script with three players (-M3)
    to detect some issues that only surface in the multi-party setting.
    """
    test_dir = Path(__file__).parents[0]
    multiplayer_test_mod = test_dir / "script_schoenfeld_residuals.py"
    subprocess.run(
        ["python", str(multiplayer_test_mod), "-M", "3"], timeout=180, check=True
    )
