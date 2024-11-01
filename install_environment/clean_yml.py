from pathlib import Path
import subprocess

def export_conda_environments(file_path:Path, file_pip_path:Path):
    try:
        # Run the conda export command in a bash shell
        result = subprocess.run(
            f'bash -c "source ~/.bashrc && conda env export --file {file_path} --from-history"',
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Environment exported successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")
    try:
        # Run the conda export command in a bash shell
        result = subprocess.run(
            f'bash -c "source ~/.bashrc && conda env export --file {file_pip_path}"',
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("Environment exported successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.stderr}")

def clean_environment_yml(file_path:Path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        with open(file_path, 'w') as file:
            for line in lines:
                if not (line.startswith('name:') or line.startswith('prefix:')):
                    file.write(line)
    except FileNotFoundError:
        print(f"File {file_path} not found. Please ensure the export was successful.")

# Export the environment and clean the yml file
file_path = Path(__file__).parent / "environment.yml"
file_path_pip = file_path.parent / "environment_with_pip.yml"
export_conda_environments(file_path, file_path_pip)
clean_environment_yml(file_path)

import yaml

# Load the content of the first environment file
with open(file_path, 'r') as file:
    env1 = yaml.safe_load(file)

# Load the content of the second environment file
with open(file_path_pip, 'r') as file:
    env2 = yaml.safe_load(file)

# Merge the pip dependencies from the second file into the first file
if 'dependencies' in env1 and 'dependencies' in env2:
    for dep in env2['dependencies']:
        if isinstance(dep, dict) and 'pip' in dep:
            for pip_dep in dep['pip']:
                # Check if pip dependencies already exist in the first file
                if not any(pip_dep in d.get('pip', []) for d in env1['dependencies'] if isinstance(d, dict)):
                    # Add pip dependencies to the first file
                    for d in env1['dependencies']:
                        if isinstance(d, dict) and 'pip' in d:
                            d['pip'].append(pip_dep)
                            break
                    else:
                        env1['dependencies'].append({'pip': [pip_dep]})

# Save the merged environment to a new file
file_path_merged = file_path.parent / "environment_merged.yml"
with open(file_path_merged, 'w') as file:
    yaml.safe_dump(env1, file)

print(f"The pip dependencies have been successfully merged into '{file_path_merged}'.")
