import bulc 

project = bulc.Project(from_file='project.yaml')

env = bulc.Environment(loader=bulc.FileSystemLoader('templates'), autoescape=bulc.select_autoescape()) 
template = env.get_template('Makefile.jinja')

print(template.render(project.targets[0].expand()))
