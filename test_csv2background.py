import pytest
import csv2background


def test_load_grid():
    field = csv2background.load_grid('sample/field.csv')
    assert len(field) == 32
    for row in field:
        assert len(row) == 32


def assert_loaded_config(config):
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


def test_config_has_default_values():
    config = csv2background.Configurations()
    assert config['gridsize'] == csv2background.Configurations.GRIDSIZE
    assert config['basecolor'] == csv2background.Configurations.BASECOLOR


def test_load_config():
    config = csv2background.Configurations()
    config.load_config('sample/config.json')
    assert_loaded_config(config)
