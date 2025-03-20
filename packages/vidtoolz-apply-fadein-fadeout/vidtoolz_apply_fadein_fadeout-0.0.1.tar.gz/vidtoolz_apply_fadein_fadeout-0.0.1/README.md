# vidtoolz-apply-fadein-fadeout

[![PyPI](https://img.shields.io/pypi/v/vidtoolz-apply-fadein-fadeout.svg)](https://pypi.org/project/vidtoolz-apply-fadein-fadeout/)
[![Changelog](https://img.shields.io/github/v/release/sukhbinder/vidtoolz-apply-fadein-fadeout?include_prereleases&label=changelog)](https://github.com/sukhbinder/vidtoolz-apply-fadein-fadeout/releases)
[![Tests](https://github.com/sukhbinder/vidtoolz-apply-fadein-fadeout/workflows/Test/badge.svg)](https://github.com/sukhbinder/vidtoolz-apply-fadein-fadeout/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sukhbinder/vidtoolz-apply-fadein-fadeout/blob/main/LICENSE)

Apply fadein-fadeout effects on videos 

## Installation

First install [vidtoolz](https://github.com/sukhbinder/vidtoolz).

```bash
pip install vidtoolz
```

Then install this plugin in the same environment as your vidtoolz application.

```bash
vidtoolz install vidtoolz-apply-fadein-fadeout
```
## Usage

type ``vid fadeinout --help`` to get help

```bash
usage: vid fadeinout [-h] [-d DURATION] [-o OUTPUT]
                     video {fadein,fadeout,both}

Apply fadein-fadeout effects on videos

positional arguments:
  video                 Path to the input video file.
  {fadein,fadeout,both}
                        Type of fade effect to apply.

optional arguments:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        Duration of the fade effect in seconds. (Default 1)
  -o OUTPUT, --output OUTPUT
                        Path for the output video file. Defaults to
                        'output_video.mp4'.

```


## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:
```bash
cd vidtoolz-apply-fadein-fadeout
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
