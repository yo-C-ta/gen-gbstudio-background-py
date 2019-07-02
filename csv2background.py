#!/usr/bin/python3

import sys
import json
import csv
import argparse
from PIL import Image


class FieldGrid:

    def __init__(self):
        self.grid = []
        self.width = 0
        self.height = 0

    def load_field_grid(self, grid_filename):
        with open(grid_filename, 'r') as gf:
            self.grid = [row for row in csv.reader(gf) if row]
            self.height = len(self.grid)
            if self.height:
                self.width = len(self.grid[0])
            for row in self.grid:
                if len(row) != self.width:
                    print('CSV format error')
                    self.grid = None
                    break

    def rows(self):
        return self.grid


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

    def __getitem__(self, key):
        return self.config[key]


def genbg(config, field_grid, outpng):
    gridsize = config['gridsize']
    width = gridsize * field_grid.width
    height = gridsize * field_grid.height
    field = Image.new('RGBA', (width, height), config['basecolor'])

    tiles = {
        key: (
            Image.new('RGBA', (gridsize,) * 2, value)
            if value.startswith('#')
            else Image.open(value).convert('RGBA')
        )
        for key, value in config['layout'].items()
        if value
    }

    for y, row in enumerate(field_grid.rows()):
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
            config['margins']['left'],
            config['margins']['top'],
            width - config['margins']['right'],
            height - config['margins']['bottom'],
        )
    ).save(outpng)


if __name__ == '__main__':
    ARGPARSE = argparse.ArgumentParser(
        description='Generate GB background image.')
    ARGPARSE.add_argument(
        'csv', type=str, default=None, help='Path to field grid file.'
    )
    ARGPARSE.add_argument(
        'json', type=str, default=None, help='Path to configuration file.'
    )
    ARGPARSE.add_argument(
        '-o',
        '--output',
        type=str,
        default='background.png',
        help='Output png filename.',
    )
    ARGS = ARGPARSE.parse_args()
    field_grid = FieldGrid()
    field_grid.load_field_grid(ARGS.csv)
    config = Configurations()
    config.load_config(ARGS.json)
    sys.exit(
        genbg(config, field_grid, ARGS.output)
    ) if config and field_grid else sys.exit(1)
