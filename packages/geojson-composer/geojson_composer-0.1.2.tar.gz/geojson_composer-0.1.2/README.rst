##########################
GeoJSON Composer
##########################

*********
Overview
*********

This project is a `GeoJSON <https://en.wikipedia.org/wiki/GeoJSON>`_ template renderer that processes GeoJSON files and applies `Jinja2 <https://github.com/pallets/jinja>`_ templates to generate customized output. It supports:

* Processing single or multiple GeoJSON files

* Grouping features dynamically

* Custom Jinja2 filters for feature property updates

* Command-line interface (CLI) support

Installation
*********

Prerequisites
=============

1. Python 3.x

2. pip package manager

Install Dependencies
=============

To install production dependencies::

 make install

To install development dependencies (for testing and linting)::

 make install-dev

Usage
*********

Running the Script::

 python main.py <input_path> <template_path> --output <output_file>

Arguments:

*input_path*: Path to a GeoJSON file or a directory containing multiple GeoJSON files:

*template_path*: Path to the Jinja2 template file.

*--output <output_file>* (optional): Path to save the rendered output. If omitted, output is printed to stdout.

Example Command:::

 python main.py geojson_data/ templates/output.jinja --output result.geojson

Development
*********

Running Tests::

 make test

Running Tests with Coverage::

 make test-coverage

Linting Code::

 make lint

License
*********

This project is licensed under the MIT License. Contact the author https://github.com/krvss for more information.

