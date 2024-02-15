import bulgogi as bul 
import glob
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

class Target():
    def __init__(self, target):
        self.id = target.id
        self.name = target.name
        self.__deps = target.deps
        self.raw_sources = [ src.name for entry in self.__deps if entry.name == 'src' for src in entry.deps ]
        self.raw_headers = [ inc.name for entry in self.__deps if entry.name == 'inc' for inc in entry.deps ]
        self.raw_private = [ pri.name for entry in self.__deps if entry.name == 'pri' for pri in entry.deps ]
        self.raw_depends = [ dep.name for entry in self.__deps if entry.name == 'dep' for dep in entry.deps ]

    def sources(self):
        """Matches `raw_sources` file patterns (using glob) in the filesystem when called"""
        return [ src for raw_src in self.raw_sources for src in glob.glob(raw_src, recursive=True) ]

    def headers(self):
        """Matches `raw_headers` file patterns (using glob) in the filesystem when called"""
        return [ inc for raw_inc in self.raw_headers for inc in glob.glob(raw_inc, recursive=True) ]

    def private(self):
        """Matches `raw_private` file patterns (using glob) in the filesystem when called"""
        return [ pri for raw_pri in self.raw_private for pri in glob.glob(raw_pri, recursive=True) ]

    def depends(self):
        """Return value of `raw_depends`"""
        return self.raw_depends

    def includes(self):
        """Return the list of unique include directories inferred from self.headers()"""
        return set([ str(Path(inc).parent) for inc in self.headers() ])

    def expand(self):
        """Return the dictionary form of the target to pass to template renderer"""
        return {
            "name": self.name,
            "sources": self.sources(),
            "headers": self.headers(),
            "private": self.private(),
            "depends": self.depends(),
            "includes": self.includes(),
        }

class Project:
    def __init__(self, from_file='project.yaml'):
        self.core = bul.Core(from_file)
        self.targets = [Target(t) for t in self.core.targets() ]
        self.depends = set([ lib for target in self.targets for lib in target.depends() ])
        self.includes = set([ inc_dir for target in self.targets for inc_dir in target.includes() ])

    def expand(self):
        """Return the dictionary form of the project to pass to template renderer"""
        return {
            "targets": [target.name for target in self.targets],
            "depends": self.depends,
            "includes": self.includes,
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
