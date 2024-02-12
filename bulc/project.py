import bulgogi as bul
from target import Target

class Project:
    """Project-based build file tracking."""

    def __init__(self, filename):
        """Initialize Project for bulc."""
        self.core = bul.Core(filename)

    def targets(self):
        """Return list of Project targets."""
        targets = []
        for t in self.core.targets():
            target = Target(t.id, t.name)

            for dep in t.deps:
                [target.add_src(src.name) for src in dep.deps if dep.name == 'src']
                [target.add_inc(inc.name) for inc in dep.deps if dep.name == 'inc']
                [target.add_pri(pri.name) for pri in dep.deps if dep.name == 'pri']
                [target.add_dep(dep) for dep in dep.deps if dep.name == 'dep']

            targets.append(target)

        return targets
