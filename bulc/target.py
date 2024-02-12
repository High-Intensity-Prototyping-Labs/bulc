class Target:
    """Atomic Build Unit."""

    def __init__(self, id, name):
        """Initialize Target for bulc."""
        self.id = id
        self.name = name
        self.src = []
        self.inc = []
        self.pri = []
        self.dep = []

    def to_string(self):
        """Convert Target to string."""
        src_str = ''
        inc_str = ''
        pri_str = ''
        dep_str = ''

        if len(self.src) > 0:
            src_str = '''src: {'''
            for src in self.src:
                src_str += '''
                ''' + src
            src_str += '''
        }'''
        else:
            src_str = 'src: None'

        if len(self.inc) > 0:
            inc_str = '''inc: {'''
            for inc in self.inc:
                inc_str += '''
                ''' + inc
            inc_str += '''
        }'''
        else:
            inc_str = 'inc: None'

        if len(self.pri) > 0:
            pri_str = '''pri: {'''
            for pri in self.pri:
                pri_str += '''
                ''' + pri
            pri_str += '''
        }'''
        else:
            pri_str = 'pri: None'

        if len(self.dep) > 0:
            dep_str = '''dep: {'''
            for dep in self.dep:
                dep_str += '''
                ''' + dep.name
            dep_str += '''
        }'''
        else:
            dep_str = 'dep: None'

        return '''Target {
        id: ''' + str(self.id) + '''
        name: ''' + self.name + '''
        ''' + src_str + '''
        ''' + inc_str + '''
        ''' + pri_str + '''
        ''' + dep_str + '''
}'''

    def add_src(self, src):
        """Add source file pattern to the target."""
        self.src.append(src)

    def add_inc(self, inc):
        """Add header file pattern to the target."""
        self.inc.append(inc)

    def add_pri(self, pri):
        """Add private header file pattern to the target."""
        self.pri.append(pri)

    def add_dep(self, dep):
        """Add target reference as dependency to the target."""
        self.dep.append(dep)
