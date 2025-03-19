def retrieve_language_base_images():
    return [
        {
            "language": "Python",
            "images": {
                "dev-base": "cgr.dev/chainguard/python:latest-dev",
                "prod-base": "cgr.dev/chainguard/python:latest"
            },
            "base-and-runtime": {
                "cgr": {
                    "dev-base": "cgr.dev/chainguard/python:latest-dev",
                    "prod-base": "cgr.dev/chainguard/python:latest"
                },
                "normal": {
                    "dev-base": "python:latest",
                    "prod-base": "python:slim"
                }
            }
        },
        {
            "language": "NodeJs",
            "images": {
                "dev-base": "cgr.dev/chainguard/node:latest-dev",
                "prod-base": "cgr.dev/chainguard/node:latest"
            },
            "base-and-runtime": {
                "cgr": {
                    "dev-base": "cgr.dev/chainguard/node:latest-dev",
                    "prod-base": "cgr.dev/chainguard/node:latest"
                },
                "normal": {
                    "dev-base": "node:lts",
                    "prod-base": "node:lts-slim"
                }
            }
        },
        {
            "language": "Maven",
            "images": {
                "dev-base": "cgr.dev/chainguard/maven:latest-dev",
                "prod-base": "cgr.dev/chainguard/maven:latest"
            },
            "base-and-runtime": {
                "cgr": {
                    "dev-base": "cgr.dev/chainguard/maven:latest-dev",
                    "prod-base": "cgr.dev/chainguard/maven:latest"
                },
                "normal": {
                    "dev-base": "",
                    "prod-base": ""
                }
            }
        },
        {
            "language": "Gradle",
            "images": {
                "dev-base": "",
                "prod-base": "cgr.dev/chainguard/gradle:latest"
            },
            "base-and-runtime": {
                "cgr": {
                    "dev-base": "",
                    "prod-base": "cgr.dev/chainguard/gradle:latest"
                },
                "normal": {
                    "dev-base": "",
                    "prod-base": ""
                }
            }
        },
        {
            "language": "dotnet",
            "images": {
                "dev-base": "",
                "prod-base": ""
            },
            "base-and-runtime": {
                "cgr": {
                    "dev-base": "",
                    "prod-base": ""
                },
                "normal": {
                    "dev-base": "",
                    "prod-base": ""
                }
            }
        },
    ]


def extract_images(language: str):
    language_base_images = retrieve_language_base_images()
    images = get_images_by_language(language_base_images, language)

    return images


def get_images_by_language(elements, language, image_type: str = 'normal'):
    """
    Extracts the 'images' object for a specific language from a list of elements.

    Parameters:
        elements (list): List of dictionaries containing 'language' and 'images'.
        language (str): The language to filter by.

    Returns:
        dict: The 'images' object for the matching language, or None if not found.
    """
    for element in elements:
        if element.get("language").lower() == language.lower():
            if image_type.lower() == 'cgr':
                return element.get("base-and-runtime", {}).get("cgr", {})
            else:
                return element.get("base-and-runtime", {}).get("normal", {})
    return None

def get_language_package_managers():
    return [
        {
            "language": "Python",
            "package_manager_file": {
                "file_name": "requirements",
                "extension": "txt"
            },
            "main_modules": {
                "filenames": ['app', 'server', 'main', 'manage'],
                "extension": 'py'
            },
            "start_scripts": [],
            "lock_files": [],
        },
        {

            "language": "NodeJs",
            "package_manager_file": {
                "file_name": "package",
                "extension": "json"
            },
            "main_modules": {
                "filenames": ['app', 'server', 'index', 'main'],
                "extension": 'js'
            },
            "start_scripts": ["start", "start:prod"],
            "lock_files": [
                {"filename": 'package-lock', "extension": 'json',
                    "package_manager": "npm"},
                {"filename": 'yarn', "extension": 'lock', "package_manager": "yarn"},
            ]
        },
        {

            "language": "Maven",
            "package_manager_file": {
                "file_name": "",
                "extension": ""
            },
            "main_modules": {
            },
            "start_scripts": [],
            "lock_files": [],
        },
        {

            "language": "Gradle",
            "package_manager_file": {
                "file_name": "",
                "extension": ""
            },
            "main_modules": {
            },
            "start_scripts": [],
            "lock_files": [],
        }
    ]
