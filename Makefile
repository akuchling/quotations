

include $(HOME)/files/www/scripts/make.rules

$(SOURCES:%.ht=%.html): links.h 

PYTHON = python
SITE = quotations.amk.ca

XMLSOURCES = $(filter-out sig-quotes.xml,$(shell echo *.xml))
HTML_FILES = $(XMLSOURCES:%.xml=%.ht) 
HTML_DIRS = $(XMLSOURCES:%.xml=%/links.h) 
FORTUNE_FILES =	$(XMLSOURCES:%.xml=%.ft) 
TEXT_FILES =	$(XMLSOURCES:%.xml=%.txt) 
TARGETS += $(HTML_FILES) $(FORTUNE_FILES) $(TEXT_FILES) sig-quotes

.SUFFIXES:	.xml .ft .txt

all: $(HTML_DIRS) $(FORTUNE_FILES) $(TEXT_FILES)

%.ft : %.xml
	qtformat --fortune $< >$@

%.txt : %.xml
	qtformat --text $< >$@

sig-quotes: robertson-davies.xml doctor-who.xml sig-quotes.xml \
            hp-lovecraft.xml comics.xml peter-greenaway.xml python-quotes.xml \
	    sherlock-holmes.xml neil-gaiman.xml shakespeare.xml
	qtformat --randomize --fortune --max 2 \
	robertson-davies.xml sig-quotes.xml comics.xml \
	peter-greenaway.xml python-quotes.xml doctor-who.xml \
	sherlock-holmes.xml neil-gaiman.xml hp-lovecraft.xml \
        shakespeare.xml \
	>sig-quotes

clobber: clean
	rm -f $(HTML_FILES) $(FORTUNE_FILES) $(TEXT_FILES) *~

cryptography/links.h : cryptography.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py cryptography
comics/links.h : comics.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py comics
doctor-who/links.h : doctor-who.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py doctor-who
housing-bubble/links.h : housing-bubble.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py housing-bubble
hp-lovecraft/links.h : hp-lovecraft.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py hp-lovecraft
neil-gaiman/links.h : neil-gaiman.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py neil-gaiman
peter-greenaway/links.h : peter-greenaway.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py peter-greenaway
python-quotes/links.h : python-quotes.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py python-quotes
quotations/links.h : quotations.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py quotations
robertson-davies/links.h : robertson-davies.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py robertson-davies
shakespeare/links.h : shakespeare.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py shakespeare
sherlock-holmes/links.h : sherlock-holmes.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py sherlock-holmes
tom-baker/links.h : tom-baker.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py tom-baker
wedding/links.h : wedding.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py wedding
