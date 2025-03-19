def generate_nodejs_dockerfile(
    dev_base_image: str,
    prod_base_image: str,
    package_manager_dir: str = None,
    entry_point: list = None,
    dev_working_dir: str = "/dev-app",
    installation_working_dir: str = "/prod-app",
    prod_working_dir: str = "/app",
    developent_env: str = "development",
    production_env: str = "production",
    install_command: str = "npm install",
    source_dir: str = "src",
    environment_variables: list = [
        {"name": "PORT", "value": "8000", "type": "runtime"}],
    group_id: int = 1001,
    user_id: int = 1001
) -> str:
    """
    Generates a Dockerfile as a string based on the provided parameters.

    Parameters:
        base_image (str): The base image for the Dockerfile (e.g., "python:3.9-slim").
        working_dir (str): The working directory inside the container (default: "/app").
        environment_vars (dict): A dictionary of environment variables (default: None).
        install_commands (list): A list of shell commands to install dependencies (default: None).
        copy_commands (list): A list of (source, destination) tuples for files to copy (default: None).
        entrypoint (list): A list of entrypoint commands (default: None).

    Returns:
        str: A string representation of the generated Dockerfile.
    """
    lines = []

    # Development stage
    lines.append(f"FROM {dev_base_image} as base")
    lines.append(f"WORKDIR {dev_working_dir}")

    # Set required env variables
    for env_var in environment_variables:
        if env_var['type'] == "config" or env_var['type'] == "runtime":
            lines.append(f"ENV {env_var['name']}={env_var['value']}")

    lines.append(f"ENV NODE_ENV={developent_env}")
    lines.append(f"COPY --chown=node:node {package_manager_dir} .")
    lines.append(f"COPY {source_dir} {source_dir}")
    lines.append(f"RUN {install_command}")

    # Section Spearator
    lines.append(f"####")

    # Installation stage
    lines.append(f"FROM base as prod-dependency-installations")
    lines.append(f"WORKDIR {installation_working_dir}")
    lines.append(f"ENV NODE_ENV={production_env}")

    # Set required env variables
    for env_var in environment_variables:
        if env_var['type'] == "config":
            lines.append(f"ENV {env_var['name']}={env_var['value']}")

    lines.append(f"COPY --chown=node:node {package_manager_dir} .")
    lines.append(f"RUN {install_command}")

    # Section Spearator
    lines.append(f"####")

    # Final stage
    lines.append(f"FROM {prod_base_image}")
    lines.append(f"WORKDIR {prod_working_dir}")

    # Set required env variables
    for env_var in environment_variables:
        if env_var['type'] == "runtime":
            lines.append(f"ENV {env_var['name']}={env_var['value']}")

    lines.append(
        f"COPY --from=prod-dependency-installations /prod-app/node_modules ./node_modules")

    # Creating new user and group
    group_name = "nodeappgroup"
    user_name = "nodeappuser"

    lines.append(f"ARG UID={user_id}")
    lines.append(f"ARG GID={group_id}")

    lines.append(f"RUN addgroup --gid $GID {group_name} && adduser --uid $UID --ingroup {
                 group_name} --system {user_name}")

    lines.append(
        f"COPY --chown={user_name}:{group_name} {package_manager_dir} .")
    lines.append(f"COPY --chown={user_name}:{group_name} {source_dir} {source_dir}")

    # Section Spearator
    lines.append(f"####")

    # Entrypoint
    lines.append(f'ENTRYPOINT {entry_point}')

    return "\n".join(lines)