all: requirements-frozen.txt

cvpartner: cvpartner-api.yml
	rm -rf cvpartner.tmp
	bin/openapi-generator-cli generate -i cvpartner-api.yml -g python --package-name scienta.cvpartner_api -o cvpartner.tmp
	rm -rf scienta/cvpartner_api
	cp -r cvpartner.tmp/scienta/cvpartner_api scienta/cvpartner_api
	rm -rf cvpartner.tmp

requirements-frozen.txt: requirements.txt
	bin/env/bin/pip freeze > $@
