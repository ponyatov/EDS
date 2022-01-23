/// @file
#include "EDS.hpp"

int main(int argc, char* argv[]) {
    // pmem allocator init

    // interpreter stage
    for (auto src = 1; src < argc; src++) {
        yyin = fopen(argv[src], "r");
        assert(yyin);
        yyparse();
        fclose(yyin);
    }

    // Qt GUI
    return App(argc, argv).exec();
}

App::App(int argc, char* argv[]) : Meta(argv[0]) {
    app = new QApplication(argc, argv);
    label = new QLabel(D.dump());
    label->resize(320, 240);
    label->setWindowTitle(value);
}

App::~App() {
    delete label;
    delete app;
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

Object::~Object() {}

QString Object::dump(int depth, QString prefix) {
    QString rets;
    QTextStream ret(&rets);
    ret << pad(depth) << head(prefix);
    return rets;
}

QString Object::head(QString prefix) {
    QString rets;
    QTextStream ret(&rets);
    ret << prefix << '<' << tag() << ':' << val() << '>';
    return rets;
}

QString Object::tag() { return "object"; }
QString Object::val() { return value; }

QString Object::pad(int depth) {
    return QString('\n') + QString('\t').repeated(depth);
}

Stack D("data");
