import os
import requests
import importlib.util
from urllib.parse import urlparse

def import_gist(url, name=None):
    """
    Downloads a Python script from a GitHub Gist and imports it as a module.

    Parameters:
    url (str): The raw URL of the Gist.
    name (str, optional): The name to assign to the module.
                          If None, it defaults to the filename in the URL.

    Returns:
    module: The imported module.
    """
    
    # Extract filename from the URL if name is not provided
    original_filename = os.path.basename(urlparse(url).path)
    
    if not original_filename.endswith('.py'):
        raise ValueError("The Gist must be a Python (.py) file")

    if name:        
        # Ensure name does not contain .py
        name = name[:-3] if name.endswith('.py') else name
    else:
        name = original_filename[:-3] # Default to filename without .py

    filename = f'{name}.py' # Ensure saved file follows name

    # Download the file if it doesn't exist
    if not os.path.exists(filename):
        response = requests.get(url)
        response.raise_for_status() # Ensure the request was successful
        with open(filename, 'w') as f:
            f.write(response.text)

    # Load module dynamically
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module # Return the imported module