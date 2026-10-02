import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent


class CommandLineFunctionalTests(unittest.TestCase):
    def test_offline_command_completes_and_creates_all_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_directory = Path(temporary_directory) / "evidence"
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "research_agent",
                    "Explainable decisions in autonomous research agents",
                    "--offline",
                    "--output",
                    str(output_directory),
                ],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertIn("Retained 3 evidence records.", completed.stdout)
            self.assertEqual(
                {
                    "research-report.json",
                    "research-report.md",
                    "workflow-trace.json",
                },
                {path.name for path in output_directory.iterdir()},
            )


if __name__ == "__main__":
    unittest.main()