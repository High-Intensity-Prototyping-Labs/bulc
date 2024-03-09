<img src="/img/bulc_basedon_bulgogi.png" width="500" />

# bulc
Build file generator for CMake.

## bulgogi
Bulc is based on [bulgogi](https://github.com/High-Intensity-Prototyping-Labs/bulgogi), a YAML parser for build configurations.

## Synopsis
See [SYNOPSIS.md](/SYNOPSIS.md).

## Installation
Bulc can be installed from pypi using pip:

```
$ pip install bulc
```

### Dependencies
Its dependencies are currently:

- bulgogi-py (`pip install bulgogi`)
- jinja2 (`pip install jinja2`)

These will automatically be fetched when bulc is installed with pip.

## Usage
Once installed, the `bulc` CLI tool should be available on your system or venv path.

```
$ bulc file.yml template.jinja > file.out
```

- `file.yml`: the YAML-defined template configuration.
- `template.jinja`: the jinja template file to feed `file.yaml` into.
- `file.out`: the output file to produce from the template.

### GNU Make Example
Suppose a `project.yaml` file defined the targets to be built and `Makefile.jinja` defined the Makefile template to use.

```
$ bulc project.yaml Makefile.jinja > Makefile
```

Once generated, using the build file would simply be a matter of running:

```
$ make
```

## License
<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/High-Intensity-Prototyping-Labs/bulc">bulc</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://github.com/amellalalex">Alex Amellal</a> is licensed under <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY 4.0<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"></a></p>
<img src="https://flagcdn.com/w20/se.png" srcset="https://flagcdn.com/w40/se.png 2x" width="20" alt="Sweden">
