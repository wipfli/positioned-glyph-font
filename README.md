# Positioned Glyph Font

The assumption of a one-to-one mapping between glyphs and Unicode codepoints that usually exists in MapLibre font files is given up in a positioned glyph font. Instead, codepoints are used as indices of positioned glyphs.

Read more about how traditional MapLibre text rendering works here: https://github.com/wipfli/about-text-rendering-in-maplibre

## Demo

A positioned glyph font demo for Nepali written in the Devanagari script and based on the Protomaps basemap is available at:

https://wipfli.github.io/positioned-glyph-font/examples/protomaps/

This demo uses the positioned-glyph-font-devanagari [branch](https://github.com/wipfli/basemaps/tree/positioned-glyph-font-devanagari) which has some modification to the basemaps Planetiler profile.

If you find bugs in the demo, please open an [Issue](https://github.com/wipfli/positioned-glyph-font/issues).

## Steps


Download Devanagari corpus from https://github.com/wipfli/word-corpus to the `corpus` folder.

There is a docker image with the dependencies for Raqm, Harfbuzz, and font-maker.

```bash
docker build -t positioned-glyph-font .
```

```bash
docker run --rm -it -v "$(pwd)":/root/ positioned-glyph-font
```

Build raqm with:

```bash
./compile_raqm.sh
```

Build the parameter space files with:

```bash
python3 build_parameter_space.py
```

Analyze and downsample the parameter space files with:

```bash
python3 analyze_parameter_space.py
```

Generate encoding with:

```bash
python3 generate_encoding.py
```

Create font pbf files with:

```bash
cd font-maker
docker run --rm -it -v "$(pwd)":/root/ positioned-glyph-font
./run.sh
```

Run the encoding http server with:

```bash
python3 server.py
```
