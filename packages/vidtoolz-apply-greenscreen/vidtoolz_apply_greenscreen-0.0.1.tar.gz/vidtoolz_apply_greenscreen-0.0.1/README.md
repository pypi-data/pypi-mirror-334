# vidtoolz-apply-greenscreen

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-apply-greenscreen.svg)](https://pypi.org/project/vidtoolz-apply-greenscreen/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-apply-greenscreen?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-apply-greenscreen/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-apply-greenscreen/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-apply-greenscreen/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-apply-greenscreen/blob/main/LICENSE)

Apply greenscreen video on top of a video

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-apply-greenscreen
```
## Usage

type ``vid greenscreen --help`` to get help

```bash
usage: vid greenscreen [-h] [-o OUTPUT]
                       [-p {top-left,top-right,bottom-left,bottom-right,center,bottom}]
                       [-s START_TIME]
                       main_video greenscreen_video

Apply greenscreen video on top of a video

positional arguments:
  main_video            Path to the main video file.
  greenscreen_video     Path to the green screen video file.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output video file name (default: output.mp4)
  -p {top-left,top-right,bottom-left,bottom-right,center,bottom}, --position {top-left,top-right,bottom-left,bottom-right,center,bottom}
                        Position of the green screen video (default: bottom)
  -s START_TIME, --start-time START_TIME
                        Start time in seconds of the overlay. Default 1

```

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-apply-greenscreen
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```
