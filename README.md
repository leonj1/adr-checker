# GitLab Merge Request Lister

This project provides a Python script to list open merge requests for a specified GitLab project, along with information about team members who have given thumbs up to each merge request.

## Features

- Fetches open merge requests from a specified GitLab project
- Displays thumbs up information for each merge request
- Color-coded output for easy visualization:
  - Green: Team members who have given a thumbs up
  - Red: Team members who haven't given a thumbs up
  - Grey: Users who have given a thumbs up but are not in the team members list

## Prerequisites

- Python 3.9 or higher
- Docker (optional, for running in a container)

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/your-username/gitlab-mr-lister.git
   cd gitlab-mr-lister
   ```

2. Install the required Python package:
   ```
   pip install requests
   ```

3. Create a `members.txt` file in the project root directory and list your team members' names, one per line.

4. Obtain a GitLab personal access token with API access.

## Usage

### Running with Python

```
python list_gitlab_mrs.py <project_path> --access_token <your_gitlab_token>
```

Replace `<project_path>` with your GitLab project path (e.g., 'username/project' or 'group/subgroup/project') and `<your_gitlab_token>` with your GitLab personal access token.

### Running with Docker

1. Build the Docker image:
   ```
   make build
   ```

2. Run the container:
   ```
   make run REPO=<project_path> GITLAB_ACCESS_TOKEN=<your_gitlab_token>
   ```

   Replace `<project_path>` and `<your_gitlab_token>` as described above.

## Configuration

- `members.txt`: Add or remove team member names to customize the output.
- `list_gitlab_mrs.py`: Modify the script to add more features or change the output format.

## Cleaning Up

To remove the Docker container and image:

```
make clean
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
