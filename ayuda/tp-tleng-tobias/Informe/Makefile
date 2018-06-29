
.PHONY: all dot clean

PDF=Informe.TP2.AyEDIII.2014.C2.pdf
TEXFILES=ej1.tex ej2.tex ej3.tex introduccion.tex apendice.tex caratula.tex

# IMAGES=$(patsubst  %, image/%, ${IMAGE})

all: $(PDF)

$(PDF):
	texi2pdf informe.tex -o $(PDF)

informe.tex: $(TEXFILES)

clean:
	rm -f $(PDF) *.aux *.log *.toc informe.out informe.blg informe.bbl
