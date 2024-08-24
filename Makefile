# Variables
IMAGE_NAME = gitlab-mr-lister
CONTAINER_NAME = gitlab-mr-lister-container

# Phony targets
.PHONY: build run clean

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the container
run:
	@if [ -z "$(REPO)" ]; then \
		echo "Usage: make run REPO=<repository_path>"; \
		echo "Example: make run REPO=group/project"; \
		exit 1; \
	fi
	docker run --name $(CONTAINER_NAME) $(IMAGE_NAME) $(REPO)

# Clean up: stop and remove the container, then remove the image
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
