import bulc 

project = bulc.Project(from_file='project.yaml')

env = bulc.Environment(loader=bulc.FileSystemLoader('templates'), autoescape=bulc.select_autoescape()) 
# Makefile_target = env.get_template('Makefile.target.jinja')
Makefile_project = env.get_template('Makefile.project.jinja')

# print(Makefile_target.render({
#     "target": project.targets()[0].expand()
# }))

# print(project.expand())
print(Makefile_project.render({ "project": project.expand() }))
