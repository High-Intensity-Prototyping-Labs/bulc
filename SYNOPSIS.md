# Synopsis
## Background
For better context, read [bulgogi's synopsis](https://github.com/High-Intensity-Prototyping-Labs/bulgogi/blob/master/SYNOPSIS.md).

## The `project.yaml`
Bulc expects every build project to have a `project.yaml` file at its root.

```
my_project 
    \_ project.yaml 
    \_ ...
```

It contains the project layout according to targets and dependencies.

```yaml 
--- # project.yaml 
- target1:
  - ...
- target2:
  - ...
---
```

## Patterns 
Those familiar with UNIX-style file path globs will immediately recognize them.

- `*` - Match anything excluding path separators (`/`).
- `*.c` - Match anything with the `.c` file extension.
- `**` - Match anything including path separators (`/`).
- `**.c` - Match anything with the `.c` file extension recursively.

A project containing the following layout:

```
my_project
    \_ src 
        \_ abc.c 
        \_ xyz.c
    \_ inc 
        \_ hjk.h 
        \_ lmn.h
```

Can be file-matched using the following patterns:

```
sources = 'my_project/src/*.c'
headers = 'my_project/inc/*.h'
```

## Target fields
For each target, bulgogi expects one or more of the following entries:

- A `src` entry containing lists of the source-file patterns (see `Globbing`).
- A `inc` entry containing lists of the header-file patterns (see `Globbing#Recursive`).
- A `pri` entry containing lists of private header-file patterns (see `Private Headers`).
- A `dep` entry containing lists of target-dependencies needed by the target.

```yaml 
--- # project.yaml 
- target1:
  - src:
    - ...
  - inc:
    - ...
  - pri:
    - ...
  - dep:
    - ...
---
```

### The `src` field 
Contains one or more source file patterns.

```yaml
--- # project.yaml 
- target1:
  - src:
    - 'my_project/src/*.c'
---
```

### The `inc` field 
Contains one or more header file patterns.

```yaml
--- # project.yaml 
- target1:
  - inc:
    - 'my_project/inc/*.h'
---
```

### The `pri` field 
Contains one or more prive header file patterns.

```yaml
--- # project.yaml 
- target1:
  - pri:
    - 'my_project/src/inc/*.h'
---
```

Note these headers will not be exposed to other targets during linkage.

### The `dep` field 
Refers to one or more project targets as dependencies.

```yaml
--- # project.yaml 
- target1:
  - ...

- target2:
  - dep:
    - target1
---
```

Note the lack of forward declarations.

### Default behaviour and assumptions
1. Given no entries for the target:
    - Bulgogi will first look for a root-level directory matching the target name.
    - If a matching directory is found, it will then proceed to look for `src` and `inc` directories.
    - If matching directories are found, it will automatically match the following source and header patterns:
        - `'src/*.c'`
        - `'src/inc/**.h'`
        - `'inc/**.h'`

2. Given only a `dep` target entry:
    - Bulc will assume this is an `INTERFACE` library (see [CMake `add_library#interface-libraries`](https://cmake.org/cmake/help/latest/command/add_library.html#interface-libraries)).
    - Any targets listed in `dep` must be discoverable in the global namespace of the project to be linked.
    - Otherwise, see (1) for what will happen to each unmatched entry in `dep`.

3. Given only a `src` target entry:
    - Bulc will find all matching source files in the provided pattern (see `Globbing`).

4. Given only a `inc` target entry:
    - Bulc will find all matching header files in the provided pattern (see `Globbing#Recursive`).
    - These will be registered as a header-only library (see [CMake `add_library#interface-libraries`](https://cmake.org/cmake/help/latest/command/add_library.html#interface-libraries)).
    - If no other targets depend on this one, no outputs will be produced.

5. Given only a `pri` target entry:
    - See (4) - with the caveat that any inclusion under another target's `dep` will not expose any of the headers.

6. Given a `dep` and a `src` target entry:
    - See (2) - with the following caveats:
        - If no other targets depend on this one, bulc will assume this to be an executable target.
        - If at least one other target depends on this one, bulc will assume this to be a standalone library.

7. Given a `dep` and a `inc` target entry:
    - See (4).
    - Bulc will find all matching header files in the provided `inc` pattern (see `Globbing#Recursive`).
    - Target which depend on this one will be exposed to all `dep` entry targets 

8. Given a `dep` and a `pri` target entry:
    - See (2) - any file patterns in `pri` are ignored.

9. Given a `dep`, `src` and `inc` target entry:
    - See (6) - matching header files in `inc` will be added to the public interface.

10. Given a `src` and `inc` target entry:
    - See (6).

NOTE: These properties are not inherent to bulgogi itself. They are requirements imposed by `bulc`.
