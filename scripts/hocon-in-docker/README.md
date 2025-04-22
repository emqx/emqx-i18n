# HOCON in docker

This docker image includes Erlang runtime and precompiled HOCON, and jsone.

## Build

```
make
```

## Run

### Print HOCON as JSON

```
docker run --rm -it -v $(pwd)/my.hocon:/tmp/input hocon do to-json /tmp/input
```

Or fetch hocon from a URL:

```
docker run --rm -it hocon do to-json "https://raw.githubusercontent.com/emqx/emqx-i18n/main/desc.zh.hocon"
```

### Flatten a HOCON file

```
docker run --rm -it hocon do flatten "https://raw.githubusercontent.com/emqx/emqx-i18n/main/desc.zh.hocon"
```
