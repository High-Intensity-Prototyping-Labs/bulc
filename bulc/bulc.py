import bulgogi as bul


from project import Project

p = Project('project.yaml')

for t in p.targets():
    print(t.to_string())
