import bulc 

project = bulc.Project(from_file='project.yaml')

env = bulc.Environment(loader=bulc.FileSystemLoader('templates'), autoescape=bulc.select_autoescape()) 
# Makefile_target = env.get_template('Makefile.target.jinja')
# Makefile_project = env.get_template('Makefile.project.jinja')
Makefile = env.get_template('Makefile.jinja')

print(Makefile.render({"project": project}))
# for target in project.expand().get('targets', []):
#     print(target)
#     print()
