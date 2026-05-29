import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
NS = {"kml": "http://www.opengis.net/kml/2.2"}


def run_oceano2kml(config, output_dir):
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "oceano2kml.py"),
            "-c",
            str(config),
            "-o",
            str(output_dir),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )


def parse_kml(path):
    return ElementTree.parse(path)


def placemark_count(tree):
    return len(tree.findall(".//kml:Placemark", NS))


def point_count(tree):
    return len(tree.findall(".//kml:Point", NS))


def linestring_count(tree):
    return len(tree.findall(".//kml:LineString", NS))


def placemark_descriptions(tree):
    return [
        description.text or ""
        for description in tree.findall(".//kml:Placemark/kml:description", NS)
    ]


class RegressionTests(unittest.TestCase):
    def test_pirata_fr31_generation(self):
        with tempfile.TemporaryDirectory() as output_dir:
            output_path = Path(output_dir)
            result = run_oceano2kml(ROOT / "pirata-fr31.toml", output_path)
            kml_path = output_path / "pirata-fr31.kml"
            self.assertTrue(kml_path.exists())
            tree = parse_kml(kml_path)

        self.assertIn("CTD: 78 stations", result.stdout)
        self.assertIn("XBT: 76 profiles", result.stdout)
        self.assertIn("TSG: 16116 data", result.stdout)
        self.assertEqual(placemark_count(tree), 155)
        self.assertEqual(point_count(tree), 154)
        self.assertEqual(linestring_count(tree), 1)

    def test_amazomix_generation_includes_ladcp(self):
        with tempfile.TemporaryDirectory() as output_dir:
            output_path = Path(output_dir)
            result = run_oceano2kml(ROOT / "amazomix.toml", output_path)
            kml_path = output_path / "amazomix.kml"
            self.assertTrue(kml_path.exists())
            tree = parse_kml(kml_path)
            descriptions = placemark_descriptions(tree)

        self.assertIn("CTD: 71 stations", result.stdout)
        self.assertIn("LADCP: 71 profiles", result.stdout)
        self.assertIn("XBT: 20 profiles", result.stdout)
        self.assertIn("TSG: 20385 data", result.stdout)
        self.assertEqual(placemark_count(tree), 163)
        self.assertEqual(point_count(tree), 162)
        self.assertEqual(linestring_count(tree), 1)
        self.assertEqual(
            sum("LADCP Profile:" in description for description in descriptions),
            71,
        )

    def test_xbt_only_configuration_does_not_require_ctd(self):
        with tempfile.TemporaryDirectory() as output_dir:
            output_path = Path(output_dir)
            config = output_path / "xbt-only.toml"
            config.write_text(
                """
cruise = "XBT-ONLY"
time = "TIME"
latitude = "LATITUDE"
longitude = "LONGITUDE"
profile = "PROFILE"

[ctd]
file = "none"

[xbt]
file = "data/fr31/OS_PIRATA-FR31_XBT.nc"
name = "Xbt"
name_format = 3
plots = "http://example.org/xbt-{:03d}.png"

[tsg]
file = "none"
""",
                encoding="utf-8",
            )

            result = run_oceano2kml(config, output_path)
            tree = parse_kml(output_path / "xbt-only.kml")

        self.assertIn("XBT: 76 profiles", result.stdout)
        self.assertEqual(placemark_count(tree), 76)
        self.assertEqual(point_count(tree), 76)
        self.assertEqual(linestring_count(tree), 0)


if __name__ == "__main__":
    unittest.main()
