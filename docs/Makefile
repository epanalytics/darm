HTML_TGTS = armv7.html thumb.html thumb2_16.html thumb2.html

.PHONY: default clean

default: $(HTML_TGTS)

%.html:
	PYTHONPATH=.. python ./docs.py

clean:
	rm -rf $(HTML_TGTS)
