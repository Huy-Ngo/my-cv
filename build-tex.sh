python3 generate_tex.py
lualatex huy-cv.tex
kill -SIGHUP "$(pgrep mupdf)"
