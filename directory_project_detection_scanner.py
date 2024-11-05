import os

def detect_project_type(directory):
    # Define file indicators for Python and Java projects
    python_indicators = {'requirements.txt', 'setup.py', '__init__.py'}
    java_indicators = {'pom.xml', 'build.gradle'}

    # Track presence of indicators
    is_python = False
    is_java = False

    # Walk through the directory and check for indicators
    for root, dirs, files in os.walk(directory):
        # Check if any Python-specific files exist
        if any(file in files for file in python_indicators) or any(file.endswith('.py') for file in files):
            is_python = True

        # Check if any Java-specific files exist
        if any(file in files for file in java_indicators) or any(file.endswith('.java') for file in files):
            is_java = True

        # If both indicators are found, classify as both and stop further search
        if is_python and is_java:
            return "Mixed"

    # Determine and return project type
    if is_python:
        return "Python"
    elif is_java:
        return "Java"
    else:
        return "Unknown"

def classify_repositories(base_directory):
    results = {}

    # Iterate over each directory in the base directory
    for entry in os.listdir(base_directory):
        repo_path = os.path.join(base_directory, entry)
        if os.path.isdir(repo_path):  # Only process directories
            project_type = detect_project_type(repo_path)
            results[entry] = project_type

    return results

# Example usage
base_directory = '/path/to/your/repositories'
project_classifications = classify_repositories(base_directory)

# Display results
for repo, project_type in project_classifications.items():
    print(f"Repository: {repo}, Project Type: {project_type}")
