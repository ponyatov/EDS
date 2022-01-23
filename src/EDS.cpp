/// @file
#include "EDS.hpp"

int argc = 0;
char** argv = nullptr;
int main(int _argc, char* _argv[]) {
    argc = _argc;
    argv = _argv;
    // pmem allocator init

    // interpreter stage
    for (auto src = 1; src < argc; src++) {
        yyin = fopen(argv[src], "r");
        assert(yyin);
        yyparse();
        fclose(yyin);
        if (compile) compile->push(ret);
    }

    // Qt GUI
    return 0;
    // return App(argc, argv).exec();
}

App::App(int argc, char* argv[]) : Meta(argv[0]) {
    app = new QApplication(argc, argv);
    label = new QLabel(D.dump());
    label->resize(320, 240);
    label->setWindowTitle(value);
}

App::~App() {
    // delete label;
    // delete app;
}

int App::exec() {
    label->show();
    return app->exec();
}

#define YYERR "#" << yylineno << ":" << msg << "[" << yytext << "]\n"
void yyerror(string msg) {
    cout << YYERR;
    cerr << YYERR;
    exit(-1);
}

Object::Object(QString V) { value = V; }

QString Object::dump(int depth, QString prefix) {
    QString rets;
    QTextStream ret(&rets);
    // head
    ret << pad(depth) << head(prefix);
    // slot{]s
    for (const auto& i : slot)
        ret << i.second->dump(depth + 1, i.first + " = ");
    // nest[]ed
    for (const auto& j : nest) ret << j->dump(depth + 1, "");
    // subtree
    return rets;
}

QString Object::head(QString prefix) {
    QString rets;
    QTextStream ret(&rets);
    ret << prefix << '<' << tag() << ':' << val() << '>';
    return rets;
}

QString Object::tag() {
    QString ret(
        abi::__cxa_demangle(typeid(*this).name(), nullptr, nullptr, nullptr));
    return ret.toLower();
}

QString Object::val() { return value; }

QString Object::pad(int depth) {
    return QString('\n') + QString('\t').repeated(depth);
}

Object* Object::setitem(QString key, Object* that) {
    slot[key] = that;
    return this;
}

Object* Object::push(Object* that) {
    nest.push_back(that);
    return this;
}

Object* Object::pop() {
    Object* ret = nest[nest.size() - 1];
    nest.pop_back();
    return ret;
}

Stack D("data");
Map W("words");

Object* compile = nullptr;

void colon() {
    QString name = D.pop()->val();
    if (compile) semicolon();  // autoclose definition
    compile = new Word(name);
    W.setitem(name, compile);
}

void semicolon() {
    assert(compile);
    compile->push(ret);
    compile = nullptr;
}

Cmd* nop = new Cmd("nop");
Cmd* halt = new Cmd("halt");
Cmd* ret = new Cmd("ret");

void q() { cout << qPrintable(D.dump()) << qPrintable(W.dump()) << "\n\n"; }
