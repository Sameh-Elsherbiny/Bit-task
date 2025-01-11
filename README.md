# Bit-task

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Docker
- Docker Compose

## Installation

### Install Docker

1. **Update your package index:**

    ```sh
    sudo apt-get update
    ```

2. **Install packages to allow apt to use a repository over HTTPS:**

    ```sh
    sudo apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release
    ```

3. **Add Docker’s official GPG key:**

    ```sh
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    ```

4. **Set up the stable repository:**

    ```sh
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
      $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    ```

5. **Install Docker Engine:**

    ```sh
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

6. **Verify that Docker Engine is installed correctly:**

    ```sh
    sudo docker run hello-world
    ```

### Install Docker Compose

1. **Download the current stable release of Docker Compose:**

    ```sh
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

2. **Apply executable permissions to the binary:**

    ```sh
    sudo chmod +x /usr/local/bin/docker-compose
    ```

3. **Verify that Docker Compose is installed correctly:**

    ```sh
    docker-compose --version
    ```

## Build and Run Docker Compose Images

1. **Navigate to the project directory:**

    ```sh
    cd /path/to/your/project
    ```

2. **Build the Docker images:**

    ```sh
    docker-compose build
    ```

3. **Start the Docker containers:**

    ```sh
    docker-compose up
    ```

4. **To stop the Docker containers:**

    ```sh
    docker-compose down
    ```

## Troubleshooting

If you encounter any issues, you can use the following commands to help diagnose and resolve problems:

- **List all running containers:**

    ```sh
    docker ps
    ```

- **Stop a running container:**

    ```sh
    docker stop <container_id>
    ```

- **Remove a container:**

    ```sh
    docker rm <container_id>
    ```

- **View Docker logs:**

    ```sh
    docker logs <container_id>
    ```

- **Prune unused Docker objects:**

    ```sh
    docker system prune -a
    ```

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
