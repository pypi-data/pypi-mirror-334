.PHONY: default

default:
	rm -rf dist
	python -m build
	python -m twine upload dist/*
	pip install --upgrade catscript
