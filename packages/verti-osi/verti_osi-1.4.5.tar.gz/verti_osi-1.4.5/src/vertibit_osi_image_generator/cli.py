import typer
# from .language_scanner import main_language_scanner
# from .file_configuration import extract_images
# from .docker_file_generator import main_docker_file_generator
# from .generate_docker_image import build_docker_image
import os

from vertibit_osi_image_generator.main.docker_file_generation import main_docker_file_generator
from vertibit_osi_image_generator.shared_aux.language_package_managers import extract_images
from vertibit_osi_image_generator.shared_aux.language_package_manager_scanner import main_language_scanner
from vertibit_osi_image_generator.image_build.generate_docker_image import build_docker_image

app = typer.Typer()


@app.command()
def create(file: str = typer.Option(..., help="The repository branch to be used."), repository_url: str = typer.Option(..., help="The remote repository url"), env_vars: str = typer.Option([], help="The applications ENV vars."), build_commands: str = typer.Option([], help="The build commands to be run."), pre_build_commands: str = typer.Option([], help="The pre-build commands to be run."), root_directory: str = typer.Option('.', help="The projects root directory"), source_directory: str = typer.Option('.', help="The projects source code directory."), image_name: str = typer.Option(..., help="The name for the generated image."), daemon: str = typer.Option('docker', help="The daemon to be used/provided."), output: str = typer.Option('', help="The generated image output type.(supports tar, registry pushing, and standard image generation)"), delete_generated_dockerfile: str = typer.Option('False', help="Delete the generated dockerfile."), run_generated_image: str = typer.Option('False', help="Run the generated docker image after build.")):
    """
    Generate a container image.
    """
    language_info = main_language_scanner(root_directory)
    images = extract_images(language_info["language"])

    docker_file_content = main_docker_file_generator(
        language_info=language_info, images=images, source_directory=source_directory, root_directory=root_directory)

    typer.echo(f"Identified language: {language_info['language']}")
    typer.echo(f"Identified language images: {images}")

    # Ensure the 'tmp' directory exists
    os.makedirs("tmp", exist_ok=True)

    # Save to a file
    with open("tmp/Dockerfile", "w") as f:
        f.write(docker_file_content)

    build_docker_image(daemon=daemon, image_name=image_name, container_file='tmp/Dockerfile',
                       build_context=root_directory, output=output, delete_generated_dockerfile=delete_generated_dockerfile, run_generated_image=run_generated_image)


if __name__ == "__main__":
    app()
