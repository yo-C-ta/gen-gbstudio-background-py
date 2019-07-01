#!/usr/bin/python3

import sys
import json
import csv
import argparse
from PIL import Image


class Configurations:

    GRIDSIZE = 8
    BASECOLOR = '#e0f8cf'

    def __init__(self):
        self.config = {}
        self._initialize()

    def _initialize(self):
        self.config['gridsize'] = Configurations.GRIDSIZE
        self.config['basecolor'] = Configurations.BASECOLOR

    def load_config(self, config_filename):
        with open(config_filename, 'r') as cf:
            json_data = json.load(cf)
            self.config.update(json_data)
            print(self.config)

    def __getitem__(self, key):
        return self.config[key]


def genbg(config, design, outpng):
    gridsize = config['gridsize']
    width = gridsize * len(design[0])
    height = gridsize * len(design)
    field = Image.new('RGBA', (width, height), config['basecolor'])

    tiles = {
        key: (
            Image.new("RGBA", (gridsize,) * 2, value)
            if value.startswith("#")
            else Image.open(value)
        )
        for key, value in config["layout"].items()
        if value
    }

    for y, row in enumerate(design):
        for x, cell in enumerate(row):
            if cell in tiles and tiles[cell]:
                tile = tiles[cell]
                field.paste(
                    tile.crop(box=(0, 0, tile.width, tile.height)),
                    box=(
                        x * gridsize,
                        y * gridsize,
                        x * gridsize + tile.width,
                        y * gridsize + tile.height,
                    ),
                    mask=tile,
                )

    field.crop(
        box=(
            config["margins"]["left"],
            config["margins"]["top"],
            width - config["margins"]["right"],
            height - config["margins"]["bottom"],
        )
    ).save(outpng)


def load_grid(grid_filename):
    with open(grid_filename, 'r') as gf:
        csv_data = [row for row in csv.reader(gf) if row]
        row_size = len(csv_data[0])
        for row in csv_data:
            if len(row) != row_size:
                print('CSV format error')
                csv_data = None
                break
    return csv_data


def load_config(config_filename):
    with open(config_filename, 'r') as cf:
        json_data = json.load(cf)
    return json_data


if __name__ == "__main__":
    ARGPARSE = argparse.ArgumentParser(
        description="Generate GB background image.")
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
    csvData = load_grid(ARGS.csv)
    config = Configurations()
    config.load_config(ARGS.json)
    sys.exit(
        genbg(config, csvData, ARGS.output)
    ) if config and csvData else sys.exit(1)
