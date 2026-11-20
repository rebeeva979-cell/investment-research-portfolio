PYTHON ?= python3
ONCHAIN := 04_ETHFI/onchain

.PHONY: all build refresh manifest manifest-check test site-check check clean

all: build check

build:
	cd $(ONCHAIN) && $(PYTHON) build_outputs.py
	cp $(ONCHAIN)/data/*.csv docs/data/
	cp $(ONCHAIN)/assets/*.svg docs/assets/

refresh:
	cd $(ONCHAIN) && $(PYTHON) fetch_onchain.py --refresh
	$(MAKE) build manifest

manifest:
	cd $(ONCHAIN) && $(PYTHON) manifest.py

manifest-check:
	cd $(ONCHAIN) && $(PYTHON) manifest.py --check

test:
	cd $(ONCHAIN) && $(PYTHON) -m unittest discover -s tests -v

site-check:
	$(PYTHON) $(ONCHAIN)/check_site.py

check: manifest-check test site-check

clean:
	rm -rf $(ONCHAIN)/__pycache__ $(ONCHAIN)/tests/__pycache__
