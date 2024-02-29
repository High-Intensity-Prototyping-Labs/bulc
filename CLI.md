# Bulc CLI Synopsis
Target version 0.1.0.

# The config folder
The config folder stores user-defined and community templates as well as config files for the utility.

On UNIX-like systems, the config folder is stored in the user's config directory.
```
~/.config/bulc
/home/$(whoami)/.config/bulc
```

On Windows, the config folder is stored in the user's APPDATA directory.
```
%APPDATA%\HIPL/bulc
C:\Users\%USERPROFILE%\AppData\Roaming\HIPL\bulc
```
Both paths are valid / equivalent to each other.

## Templates Folder
Templates are stored in the `templates` directory in the config folder.

In UNIX-like systems:
```
~/.config/bulc/templates
/home/$(whoami)/.config/bulc/templates
```

In Windows:
```
%APPDATA%\HIPL\bulc\templates
C:\Users\%USERPROFILE%\AppData\Roaming\HIPL\bulc\templates
```

# Usage
The `bulc` CLI was optimized for repetitive, one-time uses on a developer's system. As such it attempts to make the best use of default behaviour modes, short command entries and implicit arguments.

## Deploying Templates
Bulc templates can be deployed by calling the template's name in the `bulc` comand.
```
$ bulc my_template
```

This example assumes `my_template` to be a Makefile template.

### Templates with configs
If a template requires configuration info, like build targets and source files, it can be fed `.yml` files. 
```
$ bulc project.yml my_template
```

### Saving deployments to file (manual)
When deployed, templates can be saved to file in two ways.
```
$ bulc project.yml my_template -o Makefile
```

The first method involves the `-o` argument which tells bulc the name of the output file.

```
$ bulc project.yaml my_template > Makefile
```

The second involves directly redirecting the output to file.

### Saving deployments to file (automatic)
If preferred, output files can automatically be saved / named based on the template configuration.
```
$ bulc my_template -O
```

This is done with the `-O` flag, similar to `curl`'s automatic file output flag.

_Note_: Although this takes one step of familiarity / thinking out of the process, it is not recommended as the template's default behaviour may not be compatible with your project out-of-the-box.

## Adding Templates
Customizing and sharing user-defined templates is an important hallmark of bulc's envisioned usage.

### Adding Custom Templates
Adding your own hand-made templates can be added in one of two ways.
```
$ tree templates/

templates
    \_ .
    \_ ..
    \_ my_template.jinja
```

The first method involves adding the specific template file.
```
$ bulc add templates/my_template.jinja

Added 'my_template'
```
This will automatically add the `my_template.jinja` file to the user's `$BULC_CONFIG/templates` folder. It can later be deployed as `my_template`.

The second method involves adding the entire `templates` directory.
```
$ bulc add templates/

Found 'templates/my_template.jinja'
Added 'my_template'
```
Not only will the `my_template.jinja` file be added but so too would any other template files present in the `templates/` directory.

### Adding Community Templates
Community templates can be added by using the short-hand `user/repository` notation for Github.
```
$ bulc add 'amellalalex/templates'

Found 'amellalalex/templates'
Cloning 'templates' into ~/.config/bulc/templates/amellalalex/templates...
Found 'amellalalex/templates/Makefile.jinja'
Added 'amellalalex/Makefile'
```
To avoid name collisions, community templates are always stored in a directory named after the repository's username.
```
...
Cloning 'templates' into ~/.config/bulc/templates/amellalalex/templates...
...
```
These templates can later be deployed as `'amellalalex/[TEMPLATE NAME]'`.

## Template Aliases
Usernames, repositories and template names can get quite long. A small set of handy templates do not need to be cumbersome to invoke.

```
$ bulc alias 'amellalalex/Makefile' Makefile
```

This has aliased the community template `'amellalalex/Makefile'` to the local short-hand `Makefile`.

Any local or community templates previously named or aliased to `Make` will be overridden.

## Removing Templates
Removing templates (custom or community alike) requires a call to bulc's remove directive.

### Individual Templates
```
$ bulc remove my_template

Removed 'my_template'
```
In community template cases, the repository username must also be specified as it normally would:
```
$ bulc remove 'amellalalex/Makefile'

Removed 'amellalalex/Makefile'
```

### Template Folders
Entire template folders can be removed by specifiying the folder's name (assumed to be under the user's `$BULC_CONFIG/templates` directory).
```
$ bulc remove 'amellalalex'

Found 'amellalalex/templates/Makefile.jinja'
Removed 'amellalalex/Makefile'
```
This would continue until all of the templates have been removed from the matching directory.

### Default Aliases
An important set of aliases used by the bulc CLI are reserved/specially designed default aliases.

- _Default Generic Template_
- _Default Local Template_

When set, the aliased templates (custom or community alike) will be deployed in specific **Default Behaviours**.
```
$ bulc alias 'amellalalex/Makefile' DefaultGenericTemplate
```
Calls to deploy this template hereafter can be done simply by calling `bulc` in an unconfigured directory.
```
$ bulc > Makefile
```
See **Default Behaviours** for more information.

## Default Behaviours
Default behaviours are intended to be quick short-hands for frequently used commands.
```
$ bulc > Makefile
```

Without any context or user configuration, it has little meaning on their own. It is recommended for users who are familiar with the tool and their workflows already.

### Default Behaviour 1: No args, No `.yml` file.
When `bulc` is called in a directory with no arguments or valid `.yml` file at the document root, it will output the _Default Generic Template_ to `stdout`.

```
$ tree .

my_project
    \_ .
    \_ ..

$ bulc

< ... Default Generic Template Dump ... >
```

Dumping build files into `stdout` does not do much good on its own. Instead we can redirect it to a file, assuming the user's _Default Generic Template_ is a Makefile.
```
$ bulc > Makefile
```

This is most useful in small, monolithic projects which glob all of the source files in a `src` directory into one executable target.

**Don't like Make?** See _Changing Defaults_ to set your own.

### Default Behaviour 2: No args, Detected `.yml` file.
This instance is identical to _Default Behaviour 1_ with the caveat that it will deploy the user's _Default Local Template_ using the detected `.yml` file in-directory as input.
```
$ tree .

my_project
    \_ .
    \_ ..
    \_ project.yml

$ bulc 

< ... Default Local Template Dump ... >
```

As before, the output can be redirected to a file. 
```
$ bulc > Makefile
```

This behaviour primarily differs from _Default Behaviour 1_ in that the generated build file is fed the target configurations found in the `.yml` file.
