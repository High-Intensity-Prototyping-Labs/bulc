from enum import Enum, auto
import bulgogi as bul 
import glob
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from pathlib import Path

class TargetType(Enum):
    EXE = auto()
    LIB = auto()

class Core(bul.Core):
    """Bulc Wrapper for the bul.Core object."""

    def __init__(self, from_file):
        super().__init__(from_file)

    def __init_targets__(self, c_targets):
        init_targets = [ Target(c_target) for c_target in c_targets ]

        for target in init_targets:
            target.srcs = [ init_targets[src.id] for entry in target.c_deps if entry.name == 'src' for src in entry.deps ]
            target.incs = [ init_targets[inc.id] for entry in target.c_deps if entry.name == 'inc' for inc in entry.deps ]
            target.deps = [ init_targets[dep.id] for entry in target.c_deps if entry.name == 'dep' for dep in entry.deps ]
            target.pris = [ init_targets[pri.id] for entry in target.c_deps if entry.name == 'pri' for pri in entry.deps ]

            # Update based on deps
            for dep in target.deps:
                dep.type = TargetType.LIB

        return init_targets

    def raw_c_targets(self):
        return super().raw_targets()

    def raw_targets(self):
        return self.__init_targets__(super().raw_targets())

    def targets(self):
        raw_targets = self.raw_targets()
        return [ raw_targets[c_dep.id] for c_dep in raw_targets[0].c_deps ]

class Target():
    def __init__(self, target):
        self.id = target.id     # Position of this target in the pool
        self.name = target.name
        self.c_deps = target.deps
        # These deps are 'src', 'inc', 'pri' and 'dep'
        self.srcs = []
        self.incs = []
        self.deps = []
        self.pris = []
        self.type = TargetType.EXE
        self.build = self.name + '.out'
        # TODO: Detect if artifacts in the project.yaml pollute build name (aka clean name)
        
    def sources(self):
        """Matches `raw_sources` file patterns (using glob) in the filesystem when called"""
        return [ glob_src for src in self.srcs for glob_src in glob.glob(src.name, recursive=True) ]

    def includes(self):
        """Matches `raw_headers` file patterns (using glob) in the filesystem when called"""
        return [ glob_inc for inc in self.incs for glob_inc in glob.glob(inc.name, recursive=True) ]

    def private(self):
        """Matches `raw_private` file patterns (using glob) in the filesystem when called"""
        return [ glob_pri for pri in self.pris for glob_pri in glob.glob(pri.name, recursive=True) ]

    def depends(self):
        """Return build names of target dependencies (libraries)"""
        return [ raw_depends.name for raw_depends in self.deps ]

    def include_dirs(self):
        """Return the list of unique include directories inferred from self.headers()"""
        return set([ str(Path(inc).parent) for inc in self.includes() ])

    def expand(self):
        """Return the dictionary form of the target to pass to template renderer"""
        return {
            "name": self.name,
            "type": self.type.name,
            "build": self.build,
            "sources": self.sources(),
            "includes": self.includes(),
            "private": self.private(),
            "depends": self.depends(),
            "include_dirs": self.include_dirs(),
        }

class Project(Target):
    def __init__(self, from_file):
        self.core = Core(from_file)

        super().__init__(self.core.raw_c_targets()[0])
        self.targets = self.core.targets()

    def raw_sources(self):
        return [ src for dep in self.targets for src in dep.raw_sources() ]

    def raw_headers(self):
        return [ inc for dep in self.targets for inc in dep.raw_headers() ]

    def raw_private(self):
        return [ pri for dep in self.targets for pri in dep.raw_private() ]

    def raw_depends(self):
        return [ lib for dep in self.targets for lib in dep.raw_depends() ]

    def expand(self):
        return {
            "targets": [ target.expand() for target in self.targets ]
        }

# TODO: Implement a strategy to de-duplicate sources/headers/private in an elegant way (non-redundant)

def print_target(target):
    print(target.raw_sources())
    print(target.raw_headers())
    print(target.raw_private())
    print(target.raw_depends())
    
    print('')
    
    print(target.sources())
    print(target.headers())
    print(target.private())
    print(target.depends())
    print(target.includes())
    
    print('')
