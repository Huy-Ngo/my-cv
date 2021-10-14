python3 generate_tex.py
lualatex huy-cv.tex
if [ -z "$(pgrep mupdf)" ]; then
  mupdf huy-cv.pdf
else
  kill -SIGHUP "$(pgrep mupdf)"
fi
