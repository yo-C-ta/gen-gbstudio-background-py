# Generate GBStudio background field images

This script generates a background field image according to a csv formatted field design file and config.json.

## Usage

```bash
% pip install pillow
% python3 csv2background.py -h
```

## config.json

see [sample](./sample/config.json)

| key       | what                        | opt             |
| --------- | --------------------------- | --------------- |
| margins   | clipping margin             | M               |
| layout    | meta data for field design  | M               |
| gridsize  | image pixels per csv cell   | O (def 8)       |
| basecolor | basecolor to fill the field | O (def #e0f8cf) |

## Tests

### Behave

```bash
% pip install behave
% behave
```
