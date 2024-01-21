# Font Maker


## Container

```
git submodule update --init
```

Build docker image:

```
docker build -t font-maker-image .
```

Run container:

```
docker run --rm -it -v "$(pwd)":/root/ font-maker-image
```

## Raqm

In container, run:

```
cd raqm/
./run.sh
```

This assumes that `raqm/labels_requiring_encoding.json` is a json list of strings with containing the labels. It produces `raqm/encoded_labels.json` for you to use in the tileset and `encoding.hpp` for the font tool.

## Font Tool

In container, run:

```
./run.sh
```

Creates a precomposed font in `output_dir/` for the encoding used in `raqm/encoded_labels.json`.

