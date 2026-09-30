.PHONY: all install run run-all test demo docker-build docker-run clean

all: run

install:
	pip install -e .

run:
	python3 -m substrate_zero.cli

run-all:
	python3 -m substrate_zero.cli --all

test:
	python3 -m unittest discover tests -v

demo:
	python3 scripts/record_demo.py

docker-build:
	docker build -t bootlace-dev/substrate-zero:latest .

docker-run:
	docker run --rm -it bootlace-dev/substrate-zero:latest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f /tmp/dse_flawed /tmp/dse_patched
