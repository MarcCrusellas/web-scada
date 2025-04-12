install:
	pip install -r backend/requirements.txt

build:
	pyinstaller --onefile --hidden-import=win32timezone backend/service.spec

run:
	python backend/service.py standalone

clean:
	rm -rf backend/build backend/dist backend/*.spec backend/__pycache__
