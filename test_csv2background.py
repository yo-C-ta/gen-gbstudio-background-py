import pytest
import csv2background


def test_load_field_grid():
    field_grid = csv2background.FieldGrid()
    field_grid.load_field_grid('sample/field.csv')
    assert field_grid.width == 32
    assert field_grid.height == 32
    for row in field_grid.rows():
        assert len(row) == 32


def test_config_has_default_values():
    config = csv2background.Configurations()
    assert config['gridsize'] == csv2background.Configurations.GRIDSIZE
    assert config['basecolor'] == csv2background.Configurations.BASECOLOR


def test_load_config():
    config = csv2background.Configurations()
    config.load_config('sample/config.json')
    margins = config['margins']
    assert margins['top'] == 0
    assert margins['bottom'] == 0
    assert margins['left'] == 16
    assert margins['right'] == 0
    layout = config['layout']
    assert layout['1'] == ''
    assert layout['2'] == '#86c06c'
    assert layout['3'] == ''
    assert layout['4'] == ''
    assert layout['5'] == ''
    assert layout['6'] == ''
    assert layout['7'] == ''
    assert layout['8'] == ''
    assert layout['9'] == './sample/tiles/tree.png'
