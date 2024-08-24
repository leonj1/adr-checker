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
		echo "Usage: make run REPO=<repository_path> [GITLAB_ACCESS_TOKEN=<your_token>]"; \
		echo "Example: make run REPO=group/project GITLAB_ACCESS_TOKEN=your_token_here"; \
		exit 1; \
	fi
	@if [ -z "$(GITLAB_ACCESS_TOKEN)" ]; then \
		echo "Warning: GITLAB_ACCESS_TOKEN is not set. Using the default (empty) token."; \
	fi
	docker run --rm --name $(CONTAINER_NAME) \
		$(IMAGE_NAME) $(REPO) --access_token=$(GITLAB_ACCESS_TOKEN) --project=$(REPO)

# Clean up: stop and remove the container, then remove the image
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true
