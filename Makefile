.PHONY: book clean repro

BOOK_OUTPUTS = docs/build/libro-aventuras-de-conocimiento.pdf \
               docs/build/libro-aventuras-de-conocimiento.epub

book: $(BOOK_OUTPUTS)

$(BOOK_OUTPUTS): scripts/build_book.sh $(wildcard docs/*.md) \
                  docs/pandoc-common.yaml docs/pandoc-pdf.yaml docs/pandoc-epub.yaml \
                  docs/templates/book-metadata.yaml docs/templates/preamble.tex \
                  docs/styles/epub.css
	./scripts/build_book.sh

repro: book
	@echo "Recompilación completa usando scripts/build_book.sh"

clean:
	rm -rf docs/build
