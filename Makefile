all:
	@python3 -W ignore src/main.py

setup:
	pip install -r requirements.txt
	mkdir build
