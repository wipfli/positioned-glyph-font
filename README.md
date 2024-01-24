# Positioned Glyph Font

## Steps


Download Devanagari corpus from https://github.com/wipfli/word-corpus to the `corpus` folder.

```bash
docker build -t positioned-glyph-font .
```

```bash
docker run --rm -it -v "$(pwd)":/root/ positioned-glyph-font
```

Run all following commands inside the docker container.

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
