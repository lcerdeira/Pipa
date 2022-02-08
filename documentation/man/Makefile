top_srcdir = /Users/igomedeiros/Projects/pipa/Pipa/pipa_090421/modules/hmmer-3.3.2/.
srcdir     = /Users/igomedeiros/Projects/pipa/Pipa/pipa_090421/modules/hmmer-3.3.2/./documentation/man
VPATH      = /Users/igomedeiros/Projects/pipa/Pipa/pipa_090421/modules/hmmer-3.3.2/./documentation/man 
SHELL      = /bin/sh

# Installation targets
#
prefix      = /Users/igomedeiros/Projects/pipa/Pipa/pipa_090421/modules/hmmer-3.3.2
exec_prefix = ${prefix}
datarootdir = ${prefix}/share
bindir      = ${exec_prefix}/bin
libdir      = ${exec_prefix}/lib
includedir  = ${prefix}/include
mandir      = ${datarootdir}/man
docdir      = ${datarootdir}/doc/${PACKAGE_TARNAME}
pdfdir      = ${docdir}
mandir      = ${datarootdir}/man
man1dir     = ${mandir}/man1
man1ext     = .1

INSTALL     = /usr/bin/install -c

MANS =  hmmer\
	hmmalign\
	hmmbuild\
	hmmc2\
	hmmconvert\
	hmmemit\
	hmmfetch\
	hmmlogo\
	hmmpgmd\
	hmmpgmd_shard\
	hmmpress\
	hmmscan\
	hmmsearch\
	hmmsim\
	hmmstat\
	jackhmmer\
	makehmmerdb\
	phmmer\
	nhmmer\
	nhmmscan\
	alimask

.PHONY:  install uninstall clean distclean

install:
	for file in ${MANS}; do \
	   ${INSTALL} -m 0664 $$file.man ${DESTDIR}${man1dir}/$${file}${man1ext} ;\
	done

uninstall:
	for file in ${MANS}; do \
	   rm ${DESTDIR}${man1dir}/$${file}${man1ext} ;\
	done

clean:
	-rm -f *~ 
ifndef V
	@echo '     ' CLEAN man
endif

distclean:
	-rm -f *~ 
	-rm -f *.man
	-rm -f Makefile

