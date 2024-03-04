from enum import Enum, auto
import bulgogi as bul 
import glob
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
from pathlib import Path
import re

def setup_env():
    return Environment(loader=FileSystemLoader('templates'), autoescape=select_autoescape()) 

def load_template(env, template_name):
    return env.get_template(template_name)

class TargetType(Enum):
    EXE = auto()
    LIB = auto()

def infer_type(name):
    """
    Infer TargetType based on the provided `name`.
    Defaults to `TargetType.EXE` when no explicit match.
    """

    libmatch = re.fullmatch(r'(^lib)([\w]+)(.a$)', name)
    exematch = re.fullmatch(r'([\w]+)(.out$)', name)

    if libmatch is not None:
        return TargetType.LIB 
    elif exematch is not None:
        return TargetType.EXE 
    else:
        return TargetType.EXE

class Core(bul.Core):
    """Bulc Wrapper for the bul.Core object."""

    def __init__(self, from_file):
        super().__init__(from_file)

    def __init_targets__(self, c_targets):
        init_targets = [ Target(c_target) for c_target in c_targets ]

        for target in init_targets:
            target.type = infer_type(target.name)

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
        self.type = TargetType.EXE
        self.srcs = []
        self.incs = []
        self.deps = []
        self.pris = []
        
    def sources(self, ignore_deps=True):
        """Matches `raw_sources` file patterns (using glob) in the filesystem when called"""
        if ignore_deps:
            return [ glob_src for src in self.srcs for glob_src in glob.glob(src.name, recursive=True) ]
        else:
            return list(set(self.sources(ignore_deps=True) + [ dep_src for dep in self.deps for dep_src in dep.sources(ignore_deps=False) ]))

    def includes(self, ignore_deps=True):
        """Matches `raw_headers` file patterns (using glob) in the filesystem when called"""
        if ignore_deps:
            return [ glob_inc for inc in self.incs for glob_inc in glob.glob(inc.name, recursive=True) ]
        else:
            return list(set(self.includes(ignore_deps=True) + [ dep_inc for dep in self.deps for dep_inc in dep.includes(ignore_deps=False) ]))

    def private(self, ignore_deps=True):
        """Matches `raw_private` file patterns (using glob) in the filesystem when called"""
        if ignore_deps:
            return [ glob_pri for pri in self.pris for glob_pri in glob.glob(pri.name, recursive=True) ]
        else:
            return list(set(self.private(ignore_deps=True) + [ dep_pri for dep in self.deps for dep_pri in dep.private(ignore_deps=False) ]))

    def depends(self, ignore_deps=True):
        """Return build names of target dependencies (libraries)"""
        if ignore_deps:
            return [ dep.name for dep in self.deps ]
        else:
            return list(set(self.depends(ignore_deps=True) + [ dep_dep for dep in self.deps for dep_dep in dep.depends(ignore_deps=False) ]))

    def include_dirs(self, ignore_deps=True):
        """Return the list of unique include directories inferred from self.headers()"""
        if ignore_deps:
            return list(set(
                [ str(Path(inc).parent) for inc in self.includes() ]
            ))
        else:
            return list(set(
                self.include_dirs(ignore_deps=True) +
                [ dep_inc_dir for dep in self.deps for dep_inc_dir in dep.include_dirs(ignore_deps=False) ]
            ))

    def clean_name(self):
        """
        Return the clean name version of `Target.name`.
        If regex pattern match fails, the target's original name is returned.
        """

        match = re.search(r'(^lib){0,1}([\w]+)(.a$|.out$){0,1}', self.name)
        if match is not None:
            return match.group(2)
        else:
            return self.name

    def build_name(self):
        """
        Return the target compile output name based on `Target.type`.
        Makes use of the `Target.clean_name()` to ensure artifacts do not compound.
        """

        if self.type == TargetType.EXE:
            return self.clean_name() + '.out'
        else:
            return 'lib' + self.clean_name() + '.a'

    def expand(self):
        """Return the dictionary form of the target to pass to template renderer"""
        return {
            "name": self.name,
            "type": self.type.name,
            "clean_name": self.clean_name(),
            "build_name": self.build_name(),
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
