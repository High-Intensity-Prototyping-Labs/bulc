import bulgogi as bul
from . import Project

p = Project('project.yaml')

for t in p.targets():
    print(t.to_string())
