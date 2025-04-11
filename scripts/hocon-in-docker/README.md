# HOCON in docker

This docker image includes Erlang runtime and precompiled HOCON, and jsone.

## Build

```
make
```

## Run

### Print HOCON as JSON

```
docker run --rm -it -v (pwd)/my.hocon:/tmp/input hocon:0.45.1 do to-json /tmp/input
```

Or fetch hocon from a URL:

```
docker run --rm -it hocon:0.45.1 do to-json "https://raw.githubusercontent.com/emqx/emqx-i18n/main/desc.zh.hocon"
```

### Dump paths of a HOCON file

```
docker run --rm -it hocon:0.45.1 do dump-paths "https://raw.githubusercontent.com/emqx/emqx-i18n/main/desc.zh.hocon"
```
