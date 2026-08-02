from pathlib import Path
import subprocess
import tempfile
import unittest
import xml.etree.ElementTree as ET


PROCESSOR = Path(__file__).with_name("process_svg.py")


class ProcessSvgTest(unittest.TestCase):
    def run_processor(
        self, svg: str
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path]:
        directory = tempfile.TemporaryDirectory()
        _ = self.addCleanup(directory.cleanup)
        candidate_path = Path(directory.name, "candidate.svg")
        target_path = Path(directory.name, "card.svg")
        _ = candidate_path.write_text(svg)
        _ = target_path.write_text("existing valid card")
        result = subprocess.run(
            ["python3", str(PROCESSOR), str(candidate_path), str(target_path)],
            capture_output=True,
            check=False,
            text=True,
        )
        return result, candidate_path, target_path

    def test_preserves_attribute_whitespace_and_retitles_language_card(self) -> None:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg" width="300"  height="120">'
            '<text data-testid="header">Most Used Languages</text>'
            '<g data-testid="lang-items"></g></svg>'
        )

        result, candidate_path, target_path = self.run_processor(svg)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(candidate_path.exists())
        processed = target_path.read_text()
        self.assertIn('width="300"  height="120"', processed)
        self.assertIn("Most Owned Languages", processed)
        _ = ET.fromstring(processed)

    def test_rejects_error_card_without_overwriting_it(self) -> None:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            "<text>Something went wrong!</text></svg>"
        )

        result, candidate_path, target_path = self.run_processor(svg)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a language card", result.stderr)
        self.assertEqual(candidate_path.read_text(), svg)
        self.assertEqual(target_path.read_text(), "existing valid card")

    def test_rejects_marker_without_expected_header(self) -> None:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            '<g data-testid="lang-items"></g></svg>'
        )

        result, candidate_path, target_path = self.run_processor(svg)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("expected language-card header", result.stderr)
        self.assertEqual(candidate_path.read_text(), svg)
        self.assertEqual(target_path.read_text(), "existing valid card")

    def test_rejects_malformed_xml_without_overwriting_it(self) -> None:
        svg = (
            '<svg xmlns="http://www.w3.org/2000/svg"><g data-testid="lang-items"></svg>'
        )

        result, candidate_path, target_path = self.run_processor(svg)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid SVG XML", result.stderr)
        self.assertEqual(candidate_path.read_text(), svg)
        self.assertEqual(target_path.read_text(), "existing valid card")


if __name__ == "__main__":
    _ = unittest.main()
