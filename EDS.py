########################### Executable Data Structures / method & metaplatform /
########### (c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 All rights reserved
####################################### github: https://github.com/ponyatov/EDS/



import os,sys

def comment(text,width=80):
    pfx = '#' * (width - len(text) - 1)
    print(pfx + ' ' + text) ; sys.exit(-1)
# comment('metaprogramming')#,40)



######################################################### base object graph node

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.val  = V
        self.slot = {}
        self.nest = []

    ################################### dump

    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix=''):
        tree = self.pad(depth) + self.head(prefix)
        if not depth: Object.dumped = []
        if self in Object.dumped: return tree + ' _/'
        else: Object.dumped.append(self)
        for i in self.slot:
            tree += self.slot[i].dump(depth+1, prefix = '%s = ' % i)
        idx = 0
        for j in self.nest:
            tree += j.dump(depth+1, prefix='%s = ' % idx) ; idx += 1
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self.type,self._val(),id(self))
    def pad(self,depth):
        return '\n' + '\t' * depth
    def _val(self): return str(self.val)

    ############################## operators

    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        if callable(that): return self.__setitem__(key,Command(that))
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        return self.__setitem__(that.type,that)
    def __rshift__(self,that):
        if callable(that): return self.__rshift__(Command(that))
        return self.__setitem__(that.val,that)
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

    ############################## stack ops

    def pop(self): return self.nest.pop(-1)
    def top(self): return self.nest[-1]
    def pip(self): return self.nest.pop(-2)
    def tip(self): return self.nest[-2]
    def dot(self): self.nest = [] ; return self


################################################################ primitive types

class Primitive(Object):
    def eval(self,env): return env // self

class Symbol(Primitive): pass
class String(Primitive): pass
class Number(Primitive): pass
class Integer(Number): pass
class Hex(Integer): pass
class Bin(Integer): pass


#################################################### active (executable) objects

class Active(Object): pass

class Command(Active):
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        self.fn = F
    def eval(self,env):
        self.fn(env)

class VM(Active): pass

############################################################# global environment

vm = VM('metaL') ; vm << vm


########################################################################## debug

def BYE(env): sys.exit(0)

def Q(env): print(env)
vm['?'] = Q

def QQ(env): print(env) ; BYE(env)
vm['??'] = QQ


################################################################## manipulations

def EQ(env): addr = env.pop().val ; env[addr] = env.pop()
vm['='] = EQ

def PUSH(env): that = env.pop() ; env.top() // that
vm['//'] = PUSH

def DOT(env): env.dot()
vm['.'] = DOT

def DUP(env): env // env.top()
vm >> DUP

def DROP(env): env.pop()
vm >> DROP

def SWAP(env): env // env.pip()
vm >> SWAP

def OVER(env): env // env.tip()
vm >> OVER

def PRESS(env): env.pip()
vm >> PRESS


############################################################################ I/O

class IO(Object): pass
class Dir(IO): pass
class File(IO): pass

######################################################################## Network

class Net(IO): pass
class Socket(Net): pass
class IP(Net,Primitive): pass
class Port(Net): pass
def port(env): env // Port(env.pop().val)
vm >> port

class Email(Net,Primitive): pass
class URL(Net,Primitive): pass

########################################################## PLY: no-syntax parser

import ply.lex as lex

tokens = ['symbol','string','number','integer','hex','bin','ip','email','url','png']

t_ignore         = ' \t\r\n'
t_ignore_comment = r'\#.*'

states = (('str','exclusive'),)

t_str_ignore = ''

def t_str(t):
    r'\'[\r\n]?'
    t.lexer.push_state('str')
    t.lexer.string = ''
def t_str_str(t):
    r'[\r\n]?\''
    t.lexer.pop_state()
    return String(t.lexer.string)
def t_str_tab(t):
    r'\\t'
    t.lexer.string += '\t'
def t_str_lf(t):
    r'\\n'
    t.lexer.string += '\n'
def t_str_eol(t):
    r'\n'
    t.lexer.string += t.value
def t_str_char(t):
    r'.'
    t.lexer.string += t.value

def t_ip(t):
    r'([0-9]{1,3}\.){3}[0-9]{1,3}'
    return IP(t.value)
def t_email(t):
    r'[a-zA-Z0-9_]+ @ ([a-zA-Z0-9_]+\.){1,}[a-z]{2,3}'
    return Email(t.value)
def t_url(t):
    r'https?://[^ \t\r\n]+'
    return URL(t.value)
def t_png(t):
    r'[a-zA-Z0-9_]+\.png'
    return PNG(t.value)

def t_exp(t):
    r'[+\-]?[0-9]+(\.[0-9]*)?[eE][+\-]?[0-9]+'
    return Number(t.value)
def t_number(t):
    r'[+\-]?[0-9]+\.[0-9]*'
    return Number(t.value)

def t_hex(t):
    r'0x[0-9A-Fa-f]+'
    return Hex(t.value)
def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)
def t_integer(t):
    r'[+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'[`]|[^ \t\r\n\#]+'
    return Symbol(t.value)

def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()


#################################################################### interpreter

def WORD(env):
    token = lexer.token()
    if token: env // token
    return token
vm['`'] = WORD

def FIND(env):
    token = env.pop()
    try: env // env[token.val] ; return True
    except KeyError: env // token ; return False

def EVAL(env): env.pop().eval(env)

def INTERP(env):
    lexer.input(env.pop().val)
    while True:
        if not WORD(env): break
        if isinstance(env.top(),Symbol):
            if not FIND(env): raise SyntaxError(env.top())
        EVAL(env)
    print(env)



################################################################ metaprogramming

class Meta(Object): pass
class Class(Meta):
    def __init__(self,C):
        Meta.__init__(self,C.__name__)
        self.cons = C
    def eval(self,env):
        env // self.cons(env.pop().val)

#################################################################### documenting

class Doc(Object): pass

class Color(Doc): pass
def color(env): env // Color(env.pop().val)
vm >> color

class Font(Doc): pass
# def font(env): env // Font(env.pop().val)
vm >> Class(Font)

class Size(Doc): pass

def mm(env): env // Size('%smm' % env.pop().val)
vm >> mm

class PNG(Doc,File,Primitive): pass


###################################################################### eLearning



################################################################## Web interface

class Web(Net):
    def eval(self,env):
        print(env)

        from flask      import Flask,Response,render_template
        from flask_wtf  import FlaskForm
        from wtforms    import TextAreaField,SubmitField

        app = Flask(self.val)
        app.config['SECRET_KEY'] = os.urandom(32)

        class CLI(FlaskForm):
            pad = TextAreaField('pad',render_kw={'rows':5,'autofocus':'true'})
            go = SubmitField('go')

        @app.route('/', methods=['GET', 'POST'])
        def index():
            form = CLI()
            if form.validate_on_submit():
                env // String(form.pad.data) ; INTERP(env)
            return render_template('index.html',env=env,form=form)

        @app.route('/css.css')
        def css(): return Response(render_template('css.css',env=env),mimetype='text/css')

        @app.route('/<path>.png')
        def logo(path): return app.send_static_file('%s.png'%path)

        app.run(host=env['IP'].val, port=env['PORT'].val, debug=True, extra_files=list(sys.argv[1:]))

vm['WEB'] = Web(vm.head())


#################################################################### system init

if __name__ == '__main__':
    print(vm)
    for infile in sys.argv[1:]:
        with open(infile) as src:
            vm // String(src.read()) ; INTERP(vm)
