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
