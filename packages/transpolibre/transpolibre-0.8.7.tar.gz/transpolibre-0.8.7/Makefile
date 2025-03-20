# Makefile

SPHINXOPTS      ?=
SPHINXBUILD     ?= sphinx-build
SOURCEDIR       = docs/_source
BUILDDIR	= docs/_build
AUTOBUILDOPTS   = --host 127.0.0.1 --port 8000 --ignore "*.swp" --ignore "*.swx"
GETTEXT_BUILD   = gettext_build
UPDATE_LOCALE   = sphinx-intl update -p $(BUILDDIR)/locale/gettext -d $(SOURCEDIR)/locale -l
PO_FILES	= $(wildcard docs/_source/locale/*/LC_MESSAGES/*.po)
MSGATTRIB       = msgattrib
# LibreTranslate
# LANGUAGES       = ar az bn ca cs da de el en eo es et eu fa fr ga gl he hi hu id it ja ko lt lv ms nb nl pl pt ro ru sk sl sq sv th tl tr uk ur zh
# GemmaX2-28-9B-v0.1
# LANGUAGES       = ar bn cs de en es fa fr he hi id it ja km ko lo ms my nl pl pt ru th tl tr ur vi zh
# Combined
LANGUAGES       = ar bn de en es fr hi id it ja ko pl pt ru tr zh
VERSION = $(shell python3 -m setuptools_scm)

.PHONY: check help html livehtml clean_sphinx clean gettext_build update_locale build_html all copy clean_po latex pdf ebook prepress

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  clean                Remove all build files and directories (including translations)"
	@echo "  all                  Clean and make all targets"
	@echo "  gettext_build        Build localisation strings for translation"
	@echo "  update_locale        Update localisation"
	@echo "  update_locale_<lang> Update localisation for <lang>"
	@echo "  html                 Build the HTML documentation for all languages"
	@echo "  html_<lang>          Build HTML documentation for <lang>"
	@echo "  latex                Build the documentation using LaTeX for all languages"
	@echo "  latex_<lang>         Build the documentation using LaTeX for <lang>"
	@echo "  pdf                  Build the PDF documentation using LaTeX for all languages"
	@echo "  pdf_<lang>           Build the PDF documentation using LaTeX for <lang>"
	@echo "  ebook                Reduce size of PDF for eBook"
	@echo "  prepress             Reduce size of PDF for prepess"
	@echo "  index                Copy static docs/index.html to docs/_build/html/index.html"
	@echo "  translations         Translate from English"

all: clean gettext_build update_locale app_gettext_build app_msginit app_translate html index latex pdf ebook prepress

check:
	@for po in $(PO_FILES); do \
		echo "Checking $$po..."; \
		msgfmt --check --output-file=- "$$po" || exit 1; \
	done

index:
	mkdir -p docs/_build/html
	cp -p docs/index.html docs/_build/html/index.html

clean:
	for file in $(PO_FILES); do \
	    $(MSGATTRIB) --no-obsolete -o $$file $$file; \
	done
	cd docs && make clean
	find $(SOURCEDIR) -type f -name "*.mo" -delete
	rm -rf $(BUILDDIR)/*

gettext_build:
	$(SPHINXBUILD) -b gettext -c $(SOURCEDIR) -d $(BUILDDIR)/doctrees/$(GETTEXT_BUILD) $(SOURCEDIR) $(BUILDDIR)/locale/gettext

update_locale:
	@pids="" ; \
	for lang in $(LANGUAGES); do \
	    ( echo "Updating locale for $$lang..." ; $(UPDATE_LOCALE) $$lang ) & pids="$$pids $$!" ; \
	done ; \
	for pid in $$pids; do \
	    wait $$pid ; \
	done

update_locale_%:
	$(UPDATE_LOCALE) $*

html: index
	@for lang in $(LANGUAGES); do \
	    echo "Building HTML documentation for $$lang..."; \
	    $(SPHINXBUILD) -b html -d $(BUILDDIR)/doctrees -D language=$$lang $(SOURCEDIR) $(BUILDDIR)/html/$$lang; \
	done

html_%: gettext_build
	$(SPHINXBUILD) -b html -d $(BUILDDIR)/doctrees -D language=$* -c $(SOURCEDIR) $(SOURCEDIR) $(BUILDDIR)/html/$*/

latex:
	@for lang in $(filter-out ar fr he ja zh,$(LANGUAGES)); do \
		echo "Building LaTeX documentation for $$lang..."; \
		$(SPHINXBUILD) -b latex -d $(BUILDDIR)/doctrees -D language=$$lang -Dlatex_engine=xelatex $(SOURCEDIR) $(BUILDDIR)/latex/$$lang; \
	done

latex_%:
	$(SPHINXBUILD) -b latex -d $(BUILDDIR)/doctrees -D language=$* -Dlatex_engine=xelatex $(SOURCEDIR) $(BUILDDIR)/latex/$*/; \


pdf: latex
	@for lang in $(filter-out ar fr he ja zh,$(LANGUAGES)); do \
		echo "Building PDF documentation for $$lang..."; \
		$(SPHINXBUILD) -b latex -d $(BUILDDIR)/doctrees/$$lang -D language=$$lang $(SOURCEDIR) $(BUILDDIR)/latex/$$lang; \
		make -C $(BUILDDIR)/latex/$$lang; \
		mv docs/_build/latex/$$lang/transpolibre.pdf docs/_build/latex/$$lang/transpolibre-$(VERSION)-$$lang.pdf; \
	done

pdf_%: latex_%
	$(SPHINXBUILD) -b latex -d $(BUILDDIR)/doctrees/$* -D language=$* $(SOURCEDIR) $(BUILDDIR)/latex/$*/; \
	make -C $(BUILDDIR)/latex/$*; \
	mv docs/_build/latex/$*/transpolibre.pdf docs/_build/latex/$*/transpolibre-$(VERSION)-$*.pdf;

ebook: latex pdf
	@for lang in $(filter-out ar fr he ja zh,$(LANGUAGES)); do \
		gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -q \
			-o docs/_build/latex/$$lang/transpolibre-$(VERSION)-ebook-$$lang.pdf \
			docs/_build/latex/$$lang/transpolibre-$(VERSION)-$$lang.pdf; \
	done

prepress: latex pdf
	@for lang in $(filter-out ar fr he ja zh,$(LANGUAGES)); do \
		gs -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress -q \
			-o docs/_build/latex/$$lang/transpolibre-$(VERSION)-prepress-$$lang.pdf \
			docs/_build/latex/$$lang/transpolibre-$(VERSION)-$$lang.pdf; \
	done

translations: gettext_build update_locale
	@for lang in $(filter-out en,$(LANGUAGES)); do \
		for po in docs/_source/locale/$$lang/LC_MESSAGES/*.po; do \
			transpolibre -v -e local -s en -t $$lang -f "$$po"; \
		done; \
	done

translations_%:
	echo "Translating to $*..."
	for po in $(wildcard docs/_source/locale/$*/LC_MESSAGES/*.po); do \
		transpolibre -v -e local -s en -t $* -f "$$po"; \
	done

app_gettext_build:
	mkdir -p locale
	xgettext --from-code=UTF-8 -o locale/transpolibre.pot $(shell find src/ -name "*.py")
	sed -i -e 's/charset=CHARSET/charset=UTF-8/g' locale/transpolibre.pot


app_msginit:
	@for lang in $(filter-out en,$(LANGUAGES)); do \
		mkdir -p locale/$$lang/LC_MESSAGES && \
		if [ ! -f locale/$$lang/LC_MESSAGES/transpolibre.po ]; then \
			msginit --input=locale/transpolibre.pot --output-file=locale/$$lang/LC_MESSAGES/transpolibre.po --locale=$$lang.UTF-8 --no-translator; \
		fi; \
	done

app_translate:
	@for lang in $(filter-out en,$(LANGUAGES)); do \
		msgmerge --update locale/$$lang/LC_MESSAGES/transpolibre.po locale/transpolibre.pot; \
		transpolibre -v -e local -s en -t $$lang -f locale/$$lang/LC_MESSAGES/transpolibre.po; \
		msgfmt -o locale/$$lang/LC_MESSAGES/transpolibre.mo locale/$$lang/LC_MESSAGES/transpolibre.po; \
	done

