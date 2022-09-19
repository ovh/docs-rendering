# Getting started with docs-rendering

## Project structure

**config/**

Contains Yaml configuration files, example usage : *translations*.

**docker/**

Contains docker related scripts, like entrypoints, image building script, entrypoint, ...

**extra/**

Contains extra files used in pelican generation (favicon, robots.txt).

**plugins/**

Contains pelican plugins. **Contrib** directory contains third-party plugins managed as git submodules.

**screenshots/**

Contains documentation screenshots.

**themes/**

Contains OVHcloud pelican theme.

**pelicanconf.py**

Managed pelican base configuration. It should be enough to get you started, but you can override it localy if needed.

**requirements.txt**

`pip` python's package manager requirements file. It is used to specify versions of dependencies.


## Getting it up and running

### The docker way

Pre-requisites : 
* docker
* git
* a code editor

Clone the repository
```sh
git clone --recurse-submodules https://github.com/ovh/docs-rendering.git
```

Clone docs content repository
```sh
git clone https://github.com/ovh/docs.git
```

Go in the `docs-rendering` folder
```sh
cd docs-rendering
```

Build the docker image
```sh
./docker/build.sh
```

> The above command creates a docker image named *ovh-docs-dev-env*

Run the container with the helper script
```sh
./docker/run-container.sh -f $PWD/../docs -p 80
```

The above command does : 
* `./docker/run-container.sh` -> run the previously build docker image and mount some docker volumes
* `-f [...]` -> specify the path to documentation content markdown files
* `-p 80` -> expose the `80` port so you can access it like so : `http://localhost:80`

> Replace localhost with the hostname of the machine hosting your docker container

You should now be able to edit pelican theme / plugins and refresh your browser to see the changes.

> Note that the more content pages you have, the more time it will take to apply your changes


### Run it locally without docker

You will need : 
* git
* python
* a code editor

Clone the repository
```sh
git clone --recurse-submodules https://github.com/ovh/docs-rendering.git
```

Clone docs content repository
```sh
git clone https://github.com/ovh/docs.git
```

Go in the `docs-rendering` folder
```sh
cd docs-rendering
```

Install the dependencies
```sh
pip install -r requirements.txt
```

Run the pelican engine
```sh
$PELICAN --debug --fatal errors -r $PWD/../docs/pages
```

The above command does : 
* `--debug` -> show all messages
* `--fatal errors` -> exit for errors are encountered
* `-r` -> autoreload
* `$PWD/../docs/pages` -> path to content markdown files

Once the generation is finished, it should have created an output directory containing the static site.

To access it you can use the `pelican.server` python module using : `python -m pelican.server`.

So to expose the output directory, you would need to :
* open a new terminal
* run `cd output`
* run `python -m pelican.server 8080`
* open your browser at http://localhost:8080
