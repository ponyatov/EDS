# \ var
MODULE   = $(notdir $(CURDIR))
OS       = $(shell uname -s)

# \ dir
CWD = $(CURDIR)
BIN = $(CWD)/bin
DOC = $(CWD)/doc
LIB = $(CWD)/lib
SRC = $(CWD)/src
TMP = $(CWD)/tmp

# \ version
VERSION  ?= 0.0.1

# \ tool
CURL  = curl -L -o
CXX  ?= g++

# \ src
C  += src/$(MODULE).cpp
CP += tmp/$(MODULE).parser.cpp tmp/$(MODULE).lexer.cpp
H  += src/$(MODULE).hpp
HP += tmp/$(MODULE).parser.hpp
S += $(C) $(H)

# \ cfg
CFLAGS = -pipe -O0 -g2 -I$(SRC) -I$(TMP)

.PHONY: all
all: bin/$(MODULE) lib/$(MODULE).f
	$^

tmp/format_cpp: $(C) $(H)
	clang-format-11 -i -style=file $? && touch $@

# \ rule
bin/$(MODULE): $(MODULE).mk $(C) $(CP) $(H) $(HP)
	make -f $<
	$(MAKE) tmp/format_cpp
$(MODULE).mk: $(MODULE).pro
	qmake $< -o $@ && touch $(H)

tmp/%.lexer.cpp: src/%.lex
	flex -o $@ $<
tmp/%.parser.cpp: src/%.yacc
	bison -o $@ $<

# \ doc
.PHONY: doxy
doxy: doxy.gen
	rm -rf docs ; doxygen $< 1> /dev/null

# \ install

.PHONY: install update
install update: $(OS)_update
	$(MAKE) gz

.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

.PHONY: gz
gz:

# \ merge
SHADOW ?= shadow
MERGE  = Makefile README.md apt.txt doxy.gen $(S)
MERGE += .vscode bin doc lib src tmp
MERGE += .clang-format $(MODULE).pro

.PHONY: dev shadow release
dev:
	git push -v
	git checkout dev
	git pull -v
	git checkout $(SHADOW) -- $(MERGE)
shadow:
	git push -v
	git checkout $(SHADOW)
	git pull -v
