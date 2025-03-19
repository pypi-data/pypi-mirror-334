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
