#!/usr/bin/python3

import sys
import json
import csv
import argparse
from PIL import Image


def genbg(config, design, outpng):
    field = Image.new(
        "RGBA",
        (config["x"] + config["width"], config["y"] + config["height"]),
        config["basecolor"],
    )

    for key, value in config["layer"].items():
        if not value:
            continue

        if value.startswith("#"):
            size = (config["gridsize"],) * 2
            patch = Image.new("RGBA", size, value)
        else:
            patch = Image.open(value)
            size = (patch.width, patch.height)

        dest = [
            list(map(lambda p: p * config["gridsize"], (x, y)))
            for y, row in enumerate(design)
            for x, cell in enumerate(row)
            if cell == key
        ]
        for p in dest:
            field.paste(
                patch.crop(box=(0, 0, size[0], size[1])),
                box=(p[0], p[1], p[0] + size[0], p[1] + size[1]),
                mask=patch,
            )

    field.crop(
        box=(
            config["x"],
            config["y"],
            config["x"] + config["width"],
            config["y"] + config["height"],
        )
    ).save(outpng)


if __name__ == "__main__":
    ARGPARSE = argparse.ArgumentParser(description="Generate GB background image.")
    ARGPARSE.add_argument(
        "csv", type=str, default=None, help="Path to field design file."
    )
    ARGPARSE.add_argument(
        "json", type=str, default=None, help="Path to configuration file."
    )
    ARGPARSE.add_argument(
        "-o",
        "--output",
        type=str,
        default="background.png",
        help="Output png filename.",
    )
    ARGS = ARGPARSE.parse_args()

    with open(ARGS.json, "r") as jf:
        jsonData = json.load(jf)

    with open(ARGS.csv, "r") as cf:
        csvData = [row for row in csv.reader(cf) if row]

    sys.exit(
        genbg(jsonData, csvData, ARGS.output)
    ) if jsonData and csvData else sys.exit(1)
