"""
\033[1m##################### Person Poster Maker 1.0.0 #####################\033[0m

\033[1m@author: \033[1;35mJianzheng Luo\033[m \033[1m[\033[1;34mhttps://github.com/JianzhengLuo\033[m\033[1m]
\033[1m@email: \033[1;34mjianzheng.luo.china@gmail.com\033[m
@license: MIT License [\033[34m./LICENSE\033[m\033[m]\033[m
"""

import os
from random import randint
import cv2
import shutil
import click
from time import time, sleep
from click import echo
from lib.utils import cut
from cairosvg import svg2pdf
from PyPDF2 import PdfMerger
from base64 import b64encode
from lib.landmarker import BodyRector

PAPER_SIZES = {
    "A0": (841, 1189), "A1": (594, 841), "A2": (420, 594), "A3": (297, 420), "A4": (210, 297), "A5": (148, 210), "A6": (105, 148), "A7": (74, 105), "A8": (52, 74), "A9": (37, 52), "A10": (26, 37),
    "B0": (1000, 1414), "B1": (707, 1000), "B2": (500, 707), "B3": (353, 500), "B4": (250, 353), "B5": (176, 250), "B6": (125, 176), "B7": (88, 125), "B8": (62, 88), "B9": (44, 62), "B10": (31, 44),
    "C0": (917, 1297), "C1": (648, 917), "C2": (458, 648), "C3": (324, 458), "C4": (229, 324), "C5": (162, 229), "C6": (114, 162), "C7": (81, 114), "DL": (110, 220), "C7/6": (81, 162)
}


@click.command
@click.argument("photos_path", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
@click.argument("template_file", type=click.Path(exists=True))
@click.option("-t", "--margin-top", show_default=True, prompt=True, prompt_required=False, default=0, help="Top margin between body's start and the picture's top. (px) ")
@click.option("-b", "--margin-bottom", show_default=True, default=0, nargs=1, help="Bottom margin between body's end and the picture's bottom. (px) ")
@click.option("-p", "--paper-type", type=click.Choice([i for i in PAPER_SIZES.keys()]), show_default=True, default="A4", help="Type of the paper. ")
def make(photos_path, output_file, template_file, margin_top, margin_bottom, paper_type):
    def zoom(image, paper):
        return cv2.resize(image, (int((size := PAPER_SIZES[paper])[0]*(scale := (1122/297))), int(size[1]*scale)))

    def succeeded():
        echo("\033[32msucceeded\033[m")
        sleep(randint(1, 5) * 0.1)

    echo(__doc__)

    echo(
        f"INFO: Creating temp dir \033[34m\"{(temp_path := f'./TEMP{int(time())}/')}\"\033[m ... ", nl=False)
    os.mkdir(temp_path)
    succeeded()

    echo("DEBUG: Initializing human body detector ... ", nl=False)
    rector = BodyRector()
    succeeded()

    echo(
        f"INFO: Reading template \033[34m\"{template_file}\"\033[m ... ", nl=False)
    with open(template_file, "r", encoding="utf-8") as tf:
        template = template_ = tf.read()
    succeeded()

    echo("DEBUG: Initializing PDF merger ... ", nl=False)
    merger = PdfMerger()
    succeeded()

    echo("")

    for image_name in [image_names for (_, _, image_names) in os.walk(photos_path)][0]:
        echo(
            f"INFO: Processing \033[34m\"{(image_path := f'{photos_path}{image_name}')}\"\033[m ... ")

        echo("\tINFO: Reading the image ... ", nl=False)
        image = cv2.imread(image_path)
        succeeded()

        echo("\tINFO: Detecting a human body ... ", nl=False)
        rect = rector.detect(
            image, (margin_top, margin_bottom), PAPER_SIZES[paper_type])
        succeeded()

        echo("\tINFO: Making a poster ... ")

        echo("\t\tINFO: Encoding the image to base64 ... ", nl=False)
        b64_image = b64encode(cv2.imencode((suffix := f".{image_name.split('.')[-1]}"),
                                           zoom(cut(image, rect), paper_type))[1].tobytes()).decode("utf-8")
        succeeded()

        echo("\t\tINFO: Making & converting the poster to PDF ... ", nl=False)
        svg2pdf(bytestring=template.format(encoder=suffix.strip("."), data=b64_image,
                                           name=(image_name.replace(suffix, ""))), write_to=(pdf_path := f"{temp_path}{image_name}.pdf"))
        succeeded()

        echo("\tINFO: Merge to PDF files ... ", nl=False)
        merger.append(pdf_path)
        succeeded()

        echo("\tDEBUG: Resetting the template ...  ", nl=False)
        template = template_
        succeeded()

    echo(f"INFO: Writing to \033[34m\"{output_file}\"\033[m ... ", nl=False)
    merger.write(output_file)
    succeeded()

    echo(f"DEBUG: Closing the merger({merger}) ... ", nl=False)
    merger.close()
    succeeded()

    echo(
        f"INFO: Removing the temp dir \033[34m\"{temp_path}\"\033[m ... ", nl=False)
    shutil.rmtree(temp_path)
    succeeded()

    echo("\n\033[1;32mFinished. \033[m\n")


if __name__ == "__main__":
    make()
