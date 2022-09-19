# OVHcloud pelican theme

The theme is based on [pelican theme documentation](https://docs.getpelican.com/en/3.7.1/themes.html).


## Structure

### static

Contains static files (css / js). It also contains header / footer content exported from ovhcloud.com.

**header / footer folders**

The following folders are header / footer related : 
* 7af16cdb
* img
* modules
* sites

**fonts/**

Contains needed web fonts.

**css/**

Contains CSS stylesheets. 
Pure CSS stylesheets, no pre-processor.

**js/**

Contains JS files.
No javascript package manager / bundler is used yet.


### templates

Each content type has a dedicated template.

**header / footer folders**

There are header (menus) / footer related html files in the corresponding directories. There is one file per language.

**macros/**

Jinja [macros](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros). They are functions to be used in templates.

**components/**

*Logically* grouped templated referring to specific front parts of the application, hence *components*.