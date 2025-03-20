import json
import unittest
from pathlib import Path
from geojson_composer.main import (
    load_json,
    group_features,
    render_template,
    process_files,
    compile_description,
    dict_update_if,
    dict_update,
    FEATURES,
    PROPERTIES,
    DESCRIPTION
)

TEST_DATA_FILE = "sample.geojson"
TEST_TEMPLATE_FILE = "sample_template.jinja"

# Sample GeoJSON data
SAMPLE_GEOJSON_DATA = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": 1,
                "category": "park",
                "groups": ["nature"],
                "name": "DeKorte Park"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-74.10313031539833, 40.786026939284284],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": 2,
                "category": "museum",
                "title": "The Met",
                "description": "test",
                "url": "https://www.metmuseum.org/"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-73.96324400190692, 40.779688420833835],
            },
        },
        {
            "type": "Feature",
            "properties": {
                "id": 3,
                "category": "botanical garden",
                "groups": ["culture", "nature"],
                "images": ["https://njbg.org/logo.png"],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [-74.25534261703388, 41.14022835074001],
            },
        },
    ],
}

# Sample Template
SAMPLE_TEMPLATE_CONTENT = """
{
    "type": "FeatureCollection",
    "features": {{ groups['nature'] | tojson }}
}
"""


class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        """Set up temporary test files."""
        self.test_dir = Path(__file__).parent / "tmp"
        self.test_dir.mkdir(exist_ok=True)

        self.sample_geojson = self.test_dir / TEST_DATA_FILE
        with open(self.sample_geojson, "w", encoding="utf-8") as f:
            json.dump(SAMPLE_GEOJSON_DATA, f, indent=2)

        self.sample_template = self.test_dir / TEST_TEMPLATE_FILE
        with open(self.sample_template, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TEMPLATE_CONTENT)

    def tearDown(self):
        """Clean up temporary test files after each test."""
        for file in self.test_dir.iterdir():
            file.unlink()
        self.test_dir.rmdir()

    def test_load_json(self):
        """Test JSON file loading."""
        data = load_json(str(self.sample_geojson))

        self.assertIsInstance(data, dict)
        self.assertIn(FEATURES, data)
        self.assertEqual(len(data[FEATURES]), 3)

    def test_group_features(self):
        """Test feature grouping function."""
        grouped = group_features(SAMPLE_GEOJSON_DATA[FEATURES])

        self.assertIn("nature", grouped)
        self.assertEqual(len(grouped["nature"]), 2)
        self.assertNotIn("park", grouped)  # Shouldn't group by category

    def test_render_template(self):
        """Test rendering a Jinja2 template with sample data."""
        output = render_template(
            str(self.sample_template),
            SAMPLE_GEOJSON_DATA,
        )

        self.assertIn(FEATURES, output)  # Ensure features are rendered
        parsed_output = json.loads(output)
        self.assertEqual(parsed_output["type"], "FeatureCollection")
        self.assertEqual(len(parsed_output[FEATURES]), 2)

    def test_process_files(self):
        """Test full processing from input to output."""
        output_file = self.test_dir / "output.geojson"

        process_files(
            str(self.sample_geojson),
            str(self.sample_template),
            str(output_file),
        )

        self.assertTrue(output_file.exists())
        with open(output_file, "r", encoding="utf-8") as f:
            output_data = json.load(f)

        self.assertIn(FEATURES, output_data)
        self.assertEqual(len(output_data[FEATURES]), 2)


class TestFilters(unittest.TestCase):

    def test_dict_update(self):
        """Test the dict_update filter."""

        base_dict = {"a": 1, "b": 2}
        update_dict = {"b": 3, "c": 4}

        updated = dict_update(base_dict, update_dict)
        self.assertEqual(updated, {"a": 1, "b": 3, "c": 4})

    def test_dict_update_if(self):
        """Test the dict_update_if filter."""

        base_dict = {"a": 1, "b": 2}
        condition_dict = {"b": 2}
        update_dict = {"b": 3, "c": 4}

        updated = dict_update_if(base_dict, condition_dict, update_dict)
        self.assertEqual(updated, {"a": 1, "b": 3, "c": 4})

    def test_compile_no_description(self):
        feature = SAMPLE_GEOJSON_DATA[FEATURES][0]

        compiled = compile_description(feature)[PROPERTIES].get(DESCRIPTION)
        self.assertIsNone(compiled)

    def test_compile_description_url(self):
        """Test the compile_description filter."""
        feature = SAMPLE_GEOJSON_DATA[FEATURES][1]

        compiled = compile_description(feature)[PROPERTIES][DESCRIPTION]
        self.assertEqual(compiled, '<a href="https://www.metmuseum.org/">The Met</a>test')

    def test_compile_description_images(self):
        """Test the compile_description filter."""
        feature = SAMPLE_GEOJSON_DATA[FEATURES][2]

        compiled = compile_description(feature)[PROPERTIES][DESCRIPTION]
        self.assertEqual(compiled, '<img src="https://njbg.org/logo.png">')


if __name__ == "__main__":
    unittest.main()
