from enum import Enum, auto
import bulgogi as bul 
import glob
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from pathlib import Path

class TargetType(Enum):
    EXE = auto()
    LIB = auto()

class Target():
    def __init__(self, target):
        self.id = target.id
        self.name = target.name
        self.deps = target.deps
        self.type = TargetType.EXE
        # These deps are 'src', 'inc', 'pri' and 'dep'
        
    def raw_sources(self):
        return [ src for entry in self.deps if entry.name == 'src' for src in entry.deps ]
    
    def raw_headers(self):
        return [ inc for entry in self.deps if entry.name == 'inc' for inc in entry.deps ]
    
    def raw_private(self):
        return [ pri for entry in self.deps if entry.name == 'pri' for pri in entry.deps ]
    
    def raw_depends(self):
        return [ dep for entry in self.deps if entry.name == 'dep' for dep in entry.deps ]

    def sources(self):
        """Matches `raw_sources` file patterns (using glob) in the filesystem when called"""
        return [ src for raw_src in self.raw_sources() for src in glob.glob(raw_src.name, recursive=True) ]

    def headers(self):
        """Matches `raw_headers` file patterns (using glob) in the filesystem when called"""
        return [ inc for raw_inc in self.raw_headers() for inc in glob.glob(raw_inc.name, recursive=True) ]

    def private(self):
        """Matches `raw_private` file patterns (using glob) in the filesystem when called"""
        return [ pri for raw_pri in self.raw_private() for pri in glob.glob(raw_pri.name, recursive=True) ]

    def depends(self):
        """Return value of `raw_depends`"""
        return [ raw_depends.name for raw_depends in self.raw_depends() ]

    def includes(self):
        """Return the list of unique include directories inferred from self.headers()"""
        return set([ str(Path(inc).parent) for inc in self.headers() ])

    def expand(self):
        """Return the dictionary form of the target to pass to template renderer"""
        return {
            "name": self.name,
            "type": self.type.name,
            "sources": self.sources(),
            "headers": self.headers(),
            "private": self.private(),
            "depends": self.depends(),
            "includes": self.includes(),
        }

class Project(Target):
    def __init__(self, from_file):
        self.core = bul.Core(from_file=from_file)
        super().__init__(self.core.raw_targets()[0])
        self.targets = [ Target(t) for t in self.deps ]
        self.update_targets()

    def raw_sources(self):
        return [ src for dep in self.targets for src in dep.raw_sources() ]

    def raw_headers(self):
        return [ inc for dep in self.targets for inc in dep.raw_headers() ]

    def raw_private(self):
        return [ pri for dep in self.targets for pri in dep.raw_private() ]

    def raw_depends(self):
        return [ lib for dep in self.targets for lib in dep.raw_depends() ]

    # FIXME: This func could conflate targets sharing names but not IDs
    def type_of(self, search_target):
        """Return the specified target type"""
        for target in self.targets:
            if target.id == search_target.id:
                continue 
            if search_target.name in target.depends():
                return 'bul.LIB'
        return 'bul.EXE'

    def update_targets(self):
        other_targets = []
        for target_x in self.targets:
            for target_y in self.targets:
                if target_x.id == target_y.id:
                    continue 
                for dep_y in target_y.deps:
                    print('dep_y = ' + dep_y.name)
                    if dep_y.id == target_x.id:
                        target_x.type = TargetType.LIB
                    
    def expand(self):
        return {
            "targets": [ target.expand() for target in self.targets ]
        }

# TODO: Store `Target`s in `self.deps` in `Target` instead of `bul_target_s deps` type
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
