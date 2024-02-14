import bulgogi as bul 
import glob

class Target():
    def __init__(self, target):
        self.id = target.id
        self.name = target.name
        self.deps = target.deps

    def raw_sources(self):
        return [ src.name for entry in self.deps if entry.name == 'src' for src in entry.deps ]

    def raw_headers(self):
        return [ inc.name for entry in self.deps if entry.name == 'inc' for inc in entry.deps ]

    def raw_private(self):
        return [ pri.name for entry in self.deps if entry.name == 'pri' for pri in entry.deps ]

    def raw_depends(self):
        return [ Target(raw_dep) for raw_dep in self.deps ]

    def sources(self):
        return [ src for raw_src in self.raw_sources() for src in glob.glob(raw_src, recursive=True) ]

    def headers(self):
        return [ inc for raw_inc in self.raw_headers() for inc in glob.glob(raw_inc, recursive=True) ]

    def private(self):
        return [ pri for raw_pri in self.raw_private() for pri in glob.glob(raw_pri, recursive=True) ]

    def depends(self):
        return [ dep.name for dep in self.raw_depends() ]

core = bul.Core('project.yaml')

target1 = Target(core.targets()[0])
print(target1.raw_sources())
print(target1.raw_headers())
print(target1.raw_private())
print(target1.raw_depends())

print('')

print(target1.sources())
print(target1.headers())
print(target1.private())
print(target1.depends())
print(target1.raw_depends())
