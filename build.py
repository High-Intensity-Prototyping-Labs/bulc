import bulgogi as bul 

class Target():
    def __init__(self, target):
        self.id = target.id
        self.name = target.name
        self.deps = target.deps

    def sources(self):
        return [ src.name for entry in self.deps if entry.name == 'src' for src in entry.deps ]

core = bul.Core('project.yaml')

target1 = Target(core.targets()[0])
print(target1.sources())
