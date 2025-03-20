from collections import defaultdict
import json
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from typing import Optional
import logging
import sys

logging.basicConfig(level=logging.INFO)

ID = "id"
NAME = "name"
TITLE = "title"
DESCRIPTION = "description"
URL = "url"
IMAGES = "images"

FEATURES = "features"
PROPERTIES = "properties"
GROUPS_PROPERTY = "groups"
DEFAULT_GROUP = "_default"


def dict_update(original: dict, updates: dict) -> dict:
    original.update(updates)
    return original


def dict_update_if(target: dict, condition: dict, updates: dict) -> dict:
    return (
        dict_update(target, updates)
        if all(target.get(k) == v for k, v in condition.items())
        else target
    )


def compile_description(feature: dict) -> dict:
    """Compile the description of the feature.

    Args:
        feature (dict): the feature dictionary

    Returns:
        dict: feature with compiled description (URL and images HTML)
    """
    name = feature.get(PROPERTIES, {}).get("name", "") \
        or feature.get(PROPERTIES, {}).get("title", "")
    url = feature.get(PROPERTIES, {}).get("url", "")
    description = feature.get(PROPERTIES, {}).get("description", "")

    if url and name:
        description = f'<a href="{url}">{name}</a>{description}'

    images = feature.get(PROPERTIES, {}).get("images", [])
    if images:
        for image in images:
            description += f'<img src="{image}">'

    if description:
        feature[PROPERTIES][DESCRIPTION] = description

    return feature


def load_json(filename: str) -> dict:
    """Load Json from file as a dict.

    Args:
        filename (str): source file

    Returns:
        dict: Json dictionary
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logging.exception(f"Error loading JSON from {filename}")
        return {}


def group_features(features: list[dict]) -> dict[str, list[dict]]:
    """If a feature contains groups property, add it to the corresponding
    dictionary or default group.

    Args:
        features (list[dict]): List of feature dictionaries.

    Returns:
        dict: of features by group
    """
    groups: dict = defaultdict(list)

    for feature in features:
        properties = feature.get(PROPERTIES, {})

        if properties:
            for group in properties.get(GROUPS_PROPERTY, [DEFAULT_GROUP]):
                groups[group].append(feature)

    return groups


def render_template(template_path: str, geojson: dict) -> str:
    """Render the template with the specified GeoJson.

    Args:
        template_path (str): the template path
        geojson (dict): GeoJson data

    Returns:
        str: the template rendered as a string
    """
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    env.filters["dict_update"] = dict_update
    env.filters["dict_update_if"] = dict_update_if
    env.filters["compile_description"] = compile_description

    template = env.get_template(os.path.basename(template_path))
    features = geojson.get(FEATURES, [])
    groups = group_features(features)

    return template.render(geojson=geojson, features=features, groups=groups)


def process_files(
    input_path: str, template_path: str, output_path: Optional[str]
) -> None:
    """Process the file(s) in the provided path.

    Args:
        input_path (str): search path, a file or a directory
        template_path (str): the path to the template
        output_path (str): target path, stdout if empty
    """

    geojson: dict = {"type": "FeatureCollection", FEATURES: []}
    file_paths: list[str] = []

    input_path = Path(input_path)
    if input_path.is_dir():
        file_paths = list(input_path.glob("*.json")) + list(
            input_path.glob("*.geojson")
        )
    else:
        file_paths = [input_path]

    # We want to keep all the features loaded from all files, therefore
    # we join them into one big list
    for path in file_paths:
        file_features = load_json(path).get(FEATURES, [])
        geojson[FEATURES] += file_features

    rendered_output: str = render_template(template_path, geojson)

    try:
        json_output: str = json.dumps(json.loads(rendered_output), indent=2)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_output)
            logging.info(f'GeoJSON saved to "{output_path}"')
        else:
            print(json_output)
    except json.JSONDecodeError:
        logging.exception(
            "JSON decoding failed. Rendered output may be invalid:\n%s",
            rendered_output,
        )
        sys.exit(1)
