
SITEDIR = $(HOME)/source/repo/quotations.amk.ca

XMLSOURCES = $(filter-out sig-quotes.xml,$(shell echo *.xml))
HTML_FILES = $(XMLSOURCES:%.xml=%.ht)
FORTUNE_FILES =	$(XMLSOURCES:%.xml=%.ft)
TEXT_FILES =	$(XMLSOURCES:%.xml=%.txt)
TARGETS += $(HTML_FILES) $(FORTUNE_FILES) $(TEXT_FILES)
HTML_DIR = $(HOME)/source/repo/quotations.amk.ca/

.SUFFIXES:	.xml .ft .txt

all: $(FORTUNE_FILES) $(TEXT_FILES) html

%.ft : %.xml
	qtformat --fortune $< >$@

%.txt : %.xml
	qtformat --text $< >$@

html:
	qtformat --title="Comics" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/comics comics.xml
	qtformat --title="Classic Doctor Who" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/doctor-who doctor-who.xml
	qtformat --title="H.P. Lovecraft" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/hp-lovecraft hp-lovecraft.xml
	qtformat --title="Neil Gaiman" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/neil-gaiman neil-gaiman.xml
	qtformat --title="Python Programming" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/python-quotes python-quotes.xml
	qtformat --title="Commonplace Book" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/quotations quotations.xml
	qtformat --title="Shakespeare's Plays" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/shakespeare shakespeare.xml
	qtformat --title="Sherlock Holmes" --html-pages=/Users/akuchling/source/repo/quotations.amk.ca/sherlock-holmes sherlock-holmes.xml
