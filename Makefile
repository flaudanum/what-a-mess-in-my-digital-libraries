


all: clean config


.PHONY: clean
clean:
	rm -f ./scripts/whamdil

.PHONY: config
config:
	bash ./scripts/config.sh
