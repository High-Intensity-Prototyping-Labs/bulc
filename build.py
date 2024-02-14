import bulgogi as bul 

class Target():
    def __init__(self, target):
        self.id = target.id
        self.name = target.name
        self.deps = target.deps

    def sources(self):
        return [ src.name for entry in self.deps if entry.name == 'src' for src in entry.deps ]

    def headers(self):
        return [ inc.name for entry in self.deps if entry.name == 'inc' for inc in entry.deps ]

    def private(self):
        return [ pri.name for entry in self.deps if entry.name == 'pri' for pri in entry.deps ]

    def depends(self):
        return [ dep.name for entry in self.deps if entry.name == 'dep' for dep in entry.deps ]

core = bul.Core('project.yaml')

target1 = Target(core.targets()[0])
print(target1.sources())
print(target1.headers())
print(target1.private())
print(target1.depends())
