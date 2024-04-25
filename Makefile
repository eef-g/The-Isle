all:
	python3 src/main.py

setup:
	pip install -r requirements.txt
	mkdir build


test:
	python src/BSPTemp/main.py
