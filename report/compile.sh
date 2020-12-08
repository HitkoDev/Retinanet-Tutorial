docker run --rm -i -t -v "$PWD":/tmp -w /tmp blang/latex:ubuntu pdflatex NovakMarko2
docker run --rm -i -t -v "$PWD":/tmp -w /tmp blang/latex:ubuntu bibtex NovakMarko2
docker run --rm -i -t -v "$PWD":/tmp -w /tmp blang/latex:ubuntu pdflatex NovakMarko2
docker run --rm -i -t -v "$PWD":/tmp -w /tmp blang/latex:ubuntu pdflatex NovakMarko2
