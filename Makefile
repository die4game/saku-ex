#
# Makefile
# Copyright (C) 2005-2011 shinGETsu Project.
#
# $Id$
#

PREFIX = /usr/local
PACKAGE_DIR = ..
PACKAGE = sakuex-svn$(shell cat file/version.txt)

.PHONY: all install exe version check clean distclean package

all:
	python setup.py build

install:
	python setup.py install --prefix=$(PREFIX)

version:
	env LANG=C svn info | awk '/^Revision: / {print $$2}' > file/version.txt

check:
	sh tests/runtests.sh

clean:
	rm -f saku
	rm -Rf build dist root
	rm -Rf cache log run
	find . -name "*.py[co]" -print0 | xargs -0 rm -f

distclean: clean
	-svn cleanup
	find . \( -name "*~" -o -name "#*" -o -name ".#*" \) -print0 | \
	    xargs -0 rm -f

package: distclean version
	-rm -Rf $(PACKAGE_DIR)/$(PACKAGE).tar.gz $(PACKAGE_DIR)/$(PACKAGE)
	cp -a . $(PACKAGE_DIR)/$(PACKAGE)
	tar -zcf $(PACKAGE_DIR)/$(PACKAGE).tar.gz -C $(PACKAGE_DIR) $(PACKAGE)
	-rm -Rf $(PACKAGE_DIR)/$(PACKAGE)
