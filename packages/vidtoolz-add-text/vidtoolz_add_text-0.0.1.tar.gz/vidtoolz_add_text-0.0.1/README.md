# vidtoolz-add-text

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-add-text.svg)](https://pypi.org/project/vidtoolz-add-text/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-add-text?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-add-text/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-add-text/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-add-text/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-add-text/blob/main/LICENSE)

Add text to a video file

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-add-text
```
## Usage

type ``vid addtext --help`` to get help

```bash
usage: vid addtext [-h] [-o OUTPUT]
                   [-p {top-left,top-right,bottom-left,bottom-right,center,bottom}]
                   [-st START_TIME] [-et END_TIME] [-f FONTSIZE]
                   main_video text

Add text to a video file

positional arguments:
  main_video            Path to the main video file.
  text                  Text to write

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output video file name (default: output.mp4)
  -p {top-left,top-right,bottom-left,bottom-right,center,bottom}, --position {top-left,top-right,bottom-left,bottom-right,center,bottom}
                        Position of the text (default: bottom)
  -st START_TIME, --start-time START_TIME
                        Start time when text should appear
  -et END_TIME, --end-time END_TIME
                        End time when text should disappear
  -f FONTSIZE, --fontsize FONTSIZE
                        Fontsize default:50

```


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-add-text
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
