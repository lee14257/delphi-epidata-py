.DEFAULT_GOAL:=start

build:
	docker build -t streamlit-template -f devops/Dockerfile .

# Starts a docker image with a full preconfigured R environment
start_dev: build
	docker run -it --rm \
		-p 8090:8090 \
		-e STREAMLIT_FILE_WATCHER_TYPE=auto \
		-e STREAMLIT_SERVER_PORT=8090 \
		-v ${PWD}/app:/app/

run: build
	docker run --rm -p 80:80 streamlit-template

start:
	streamlit run app/__main__.py

lint:
	pylint app
	mypy --ignore-missing-imports app
	black --config pyproject.toml --check app

format:
	black --config pyproject.toml app