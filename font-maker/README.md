# Font Maker


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