

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

clobber: clean
	rm -f $(HTML_FILES) $(FORTUNE_FILES) $(TEXT_FILES) *~

# Copy files to the live site
copy:
	rsync -av  --exclude-from=$$HOME/files/www/scripts/rsync-excludes \
               $$HOME/files/www/sites/quotations.amk.ca/ akuchling@wasp.dreamhost.com:~/quotations.amk.ca/

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
python-quotes/links.h : python-quotes.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py python-quotes
quotations/links.h : quotations.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py quotations
shakespeare/links.h : shakespeare.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py shakespeare
sherlock-holmes/links.h : sherlock-holmes.xml
	qtformat --html --split 8 $< | \
		$(PYTHON) make-ht.py sherlock-holmes

