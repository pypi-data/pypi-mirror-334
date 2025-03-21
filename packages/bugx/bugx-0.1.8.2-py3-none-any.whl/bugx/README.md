# `Bugx`

**Usage**:

```console
$ Bugx [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-v, --version`: Prints the Version and Changelog.
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.




**Commands**:

* `select`: Prompts the users to select the Bugreports.
* `watch`: Looks for newly added Bugreports

## `Bugx select`

Bugx will prompts the user to select the files using Right/Left arrow to select/unselect, Up/Down to navigate. Press ENTER after selecting the files.


  
Examples:

    $ bugx select --display
    $ bugx select -d
    
    $ bugx select --all
    $ bugx select -a
    
Recommended to use :  **bugx select -d**

**Usage**:

```console
$ Bugx select [OPTIONS]
```

**Options**:

* `-a, --all`: Parses all Bugreports.
* `-d, --display`: Displays the output in the terminal.
* `-v, --version`: Show version information
* `--help`: Show this message and exit.



## `Bugx watch`

Bugx automatically looks for new bugreports in both Downloads &amp; Documents folders.
If a new bugreport added/downloaded/dropped into any of the two folders it will be automatically processed.


  
Examples:

    $ bugx watch --display
    $ bugx watch -d

Recommended to use :  **bugx watch -d**

**Usage**:

```console
$ Bugx watch [OPTIONS]
```

**Options**:

* `-d, --display`: Displays the output in the terminal.
* `-v, --version`: Show version information
* `--help`: Show this message and exit.

