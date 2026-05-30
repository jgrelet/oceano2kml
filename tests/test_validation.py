import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path to import oceano2kml module
sys.path.insert(0, str(Path(__file__).parents[1]))
from oceano2kml import (
    require_config_keys,
    require_variables,
    require_input_file,
    is_enabled,
    PROFILE_INSTRUMENTS,
)


class TestConfigKeysValidation(unittest.TestCase):
    """Tests for require_config_keys function."""

    def test_valid_keys(self):
        """Test that valid keys pass without error."""
        cfg = {'cruise': 'TEST', 'time': 'TIME', 'latitude': 'LAT', 'longitude': 'LON', 'profile': 'PROF'}
        # Should not raise any error
        require_config_keys(cfg, ['cruise', 'time'])

    def test_missing_single_key(self):
        """Test error raised when one key is missing."""
        cfg = {'cruise': 'TEST'}
        with self.assertRaises(ValueError) as ctx:
            require_config_keys(cfg, ['cruise', 'time'], 'test config')
        self.assertIn("test config", str(ctx.exception))
        self.assertIn("missing required key(s): time", str(ctx.exception))

    def test_missing_multiple_keys(self):
        """Test error raised when multiple keys are missing."""
        cfg = {'cruise': 'TEST'}
        with self.assertRaises(ValueError) as ctx:
            require_config_keys(cfg, ['cruise', 'time', 'latitude'], '[global]')
        self.assertIn("[global]", str(ctx.exception))
        self.assertIn("time", str(ctx.exception))
        self.assertIn("latitude", str(ctx.exception))

    def test_empty_config(self):
        """Test error raised with empty config."""
        cfg = {}
        with self.assertRaises(ValueError) as ctx:
            require_config_keys(cfg, ['cruise'])
        self.assertIn("cruise", str(ctx.exception))


class TestIsEnabled(unittest.TestCase):
    """Tests for is_enabled function."""

    def test_file_none_disabled(self):
        """Test that file='none' returns False."""
        section = {'file': 'none'}
        self.assertFalse(is_enabled(section))

    def test_file_missing_disabled(self):
        """Test that missing file key defaults to 'none' and returns False."""
        section = {}
        self.assertFalse(is_enabled(section))

    def test_file_empty_string_disabled(self):
        """Test that empty file string returns True."""
        section = {'file': ''}
        self.assertTrue(is_enabled(section))

    def test_file_valid_enabled(self):
        """Test that valid file path returns True."""
        section = {'file': 'data/test.nc'}
        self.assertTrue(is_enabled(section))

    def test_file_relative_path_enabled(self):
        """Test that relative path returns True."""
        section = {'file': '../data/test.nc'}
        self.assertTrue(is_enabled(section))


class TestRequireInputFile(unittest.TestCase):
    """Tests for require_input_file function."""

    def test_existing_file(self):
        """Test that existing file passes without error."""
        with tempfile.NamedTemporaryFile(suffix='.nc', delete=False) as f:
            temp_path = f.name
        try:
            # Should not raise any error
            require_input_file(temp_path)
        finally:
            os.unlink(temp_path)

    def test_missing_file(self):
        """Test error raised for non-existent file."""
        with self.assertRaises(FileNotFoundError) as ctx:
            require_input_file("/nonexistent/path/to/file.nc")
        self.assertIn("Input file not found", str(ctx.exception))
        self.assertIn("/nonexistent/path/to/file.nc", str(ctx.exception))

    def test_relative_path_missing(self):
        """Test error raised for non-existent relative path."""
        with self.assertRaises(FileNotFoundError) as ctx:
            require_input_file("data/nonexistent.nc")
        self.assertIn("data/nonexistent.nc", str(ctx.exception))


class TestProfileInstruments(unittest.TestCase):
    """Tests for PROFILE_INSTRUMENTS constant."""

    def test_contains_all_instruments(self):
        """Test that all expected instruments are present."""
        expected_instruments = {'ctd', 'ladcp', 'xbt'}
        self.assertEqual(set(PROFILE_INSTRUMENTS.keys()), expected_instruments)

    def test_ctd_structure(self):
        """Test CTD instrument has required fields."""
        ctd = PROFILE_INSTRUMENTS['ctd']
        self.assertIn('label', ctd)
        self.assertIn('count_label', ctd)
        self.assertIn('color', ctd)
        self.assertIn('icon', ctd)
        self.assertEqual(ctd['label'], 'CTD Station')
        self.assertEqual(ctd['count_label'], 'stations')

    def test_ladcp_structure(self):
        """Test LADCP instrument has required fields."""
        ladcp = PROFILE_INSTRUMENTS['ladcp']
        self.assertEqual(ladcp['label'], 'LADCP Profile')
        self.assertEqual(ladcp['count_label'], 'profiles')

    def test_xbt_structure(self):
        """Test XBT instrument has required fields."""
        xbt = PROFILE_INSTRUMENTS['xbt']
        self.assertEqual(xbt['label'], 'XBT Profile')
        self.assertEqual(xbt['count_label'], 'profiles')


class TestRequireVariables(unittest.TestCase):
    """Tests for require_variables function."""

    def test_mock_dataset_missing_variable(self):
        """Test error raised when dataset is missing a variable."""
        # Create a mock dataset with only some variables
        class MockDataset:
            variables = {'TIME': {}, 'LATITUDE': {}, 'LONGITUDE': {}}

        with self.assertRaises(ValueError) as ctx:
            require_variables(MockDataset(), ['TIME', 'PROFILE'], 'test.nc')
        self.assertIn("test.nc", str(ctx.exception))
        self.assertIn("PROFILE", str(ctx.exception))

    def test_mock_dataset_all_variables_present(self):
        """Test that no error is raised when all variables are present."""
        class MockDataset:
            variables = {'TIME': {}, 'LATITUDE': {}, 'LONGITUDE': {}, 'PROFILE': {}}

        # Should not raise any error
        require_variables(MockDataset(), ['TIME', 'LATITUDE', 'LONGITUDE', 'PROFILE'], 'test.nc')


if __name__ == '__main__':
    unittest.main()
