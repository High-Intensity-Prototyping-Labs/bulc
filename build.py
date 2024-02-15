import bulgogi as bul 
import glob
from jinja2 import Environment, PackageLoader, select_autoescape
from pathlib import Path

class Target():
    def __init__(self, target):
        self.id = target.id
        self.name = target.name
        self.__deps = target.deps

    def raw_sources(self):
        return [ src.name for entry in self.__deps if entry.name == 'src' for src in entry.deps ]

    def raw_headers(self):
        return [ inc.name for entry in self.__deps if entry.name == 'inc' for inc in entry.deps ]

    def raw_private(self):
        return [ pri.name for entry in self.__deps if entry.name == 'pri' for pri in entry.deps ]

    def raw_depends(self):
        return [ dep.name for entry in self.__deps if entry.name == 'dep' for dep in entry.deps ]

    def sources(self):
        return [ src for raw_src in self.raw_sources() for src in glob.glob(raw_src, recursive=True) ]

    def headers(self):
        return [ inc for raw_inc in self.raw_headers() for inc in glob.glob(raw_inc, recursive=True) ]

    def private(self):
        return [ pri for raw_pri in self.raw_private() for pri in glob.glob(raw_pri, recursive=True) ]

    def depends(self):
        return self.raw_depends()

    def includes(self):
        """Return the list of unique include directories inferred from self.headers()"""
        return set([ str(Path(inc).parent) for inc in self.headers() ])

    def expose(self):
        """Return the dictionary form of the target to pass to template renderer"""
        return {
            "name": self.name,
            "sources": self.sources(),
            "headers": self.headers(),
            "private": self.private(),
            "depends": self.depends(),
            "includes": self.includes(),
        }

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

core = bul.Core('project.yaml')

target = Target(core.targets()[0])

# TODO: Make this work with the example project.yaml start to finish

env = Environment(
    loader=PackageLoader("build"),
    autoescape=select_autoescape(),
)

template = env.get_template("Makefile.jinja")

print(template.render(target.expose()))
