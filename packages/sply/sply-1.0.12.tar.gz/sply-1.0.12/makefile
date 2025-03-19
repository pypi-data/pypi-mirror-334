all: install

dist:
	python -m build

install:
	pip install --force-reinstall --no-build-isolation --no-deps .

test:
	PYTHONPATH="." bin/sply_chat_interact.py $(test_args)

upload:
	twine upload dist/*

clean:
	rm -rf build sply.egg-info dist
