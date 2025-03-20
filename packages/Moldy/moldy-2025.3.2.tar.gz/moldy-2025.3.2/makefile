build:
	make clean
	.venv/bin/python -m build

clean:
	touch dist/fuck
	rm dist/*

upload:
	vinc
	make build
	.venv/bin/python -m twine upload --repository pypi dist/* $(flags)
