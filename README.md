# Person Poster Maker

## Background
Months ago, I saw my teacher is making person posters of the students those did good in the exam. He is dragging pictures and print the poster one by one, slowly. So I decided to make an easy tool for him.

## Install

### Create a Virtual Environment

```sh
pip3 install virtualenv -U
virtualenv "./venv"
```

### Install Requirements

```sh
pip3 install -r "./requirements.txt"
```

## Usage

```sh
(venv) .../PersonPosterMaker$ python3 "./__main__.py" --help
Usage: __main__.py [OPTIONS] PHOTOS_PATH OUTPUT_FILE TEMPLATE_FILE

Options:
  -t, --margin-top INTEGER        Top margin between body's start and the
                                  picture's top. (px)   [default: 0]
  -b, --margin-bottom INTEGER     Bottom margin between body's end and the
                                  picture's bottom. (px)   [default: 0]
  -p, --paper-type [A0|A1|A2|A3|A4|A5|A6|A7|A8|A9|A10|B0|B1|B2|B3|B4|B5|B6|B7|B8|B9|B10|C0|C1|C2|C3|C4|C5|C6|C7|DL|C7/6]
                                  Type of the paper.   [default: A4]
  --help                          Show this message and exit.
```