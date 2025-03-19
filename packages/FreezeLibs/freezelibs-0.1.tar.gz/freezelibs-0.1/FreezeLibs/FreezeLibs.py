import os
import ast
import argparse
from typing import Set, Dict
import importlib.metadata

__version__ = "1.0.0"

# Mapping of import names to their corresponding PyPI package names
IMPORT_TO_INSTALL_MAPPING = {
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "yaml": "PyYAML",
    "sklearn": "scikit-learn",
    "bs4": "beautifulsoup4",
    "dateutil": "python-dateutil",
}

class FreezeLibs:
    def __init__(self):
        self.imported_libs: Set[str] = set()

    def extract_imports(self, file_path: str) -> Set[str]:
        """Extract imported libraries from a Python file."""
        with open(file_path, "r") as file:
            tree = ast.parse(file.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imported_libs.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    self.imported_libs.add(node.module.split(".")[0])

        return self.imported_libs

    def get_lib_version(self, lib_name: str) -> str:
        """Get the version of an installed library."""
        try:
            return importlib.metadata.version(lib_name)
        except importlib.metadata.PackageNotFoundError:
            return "unknown"

    def get_install_name(self, import_name: str) -> str:
        """Get the PyPI package name for a given import name."""
        return IMPORT_TO_INSTALL_MAPPING.get(import_name, import_name)

    def save_imports(self, file_path: str, with_versions: bool = False):
        """Save imported libraries to a requirements file."""
        imports = self.extract_imports(file_path)
        with open("requirements.txt", "w") as req_file:
            for lib in sorted(imports):
                install_name = self.get_install_name(lib)
                if with_versions:
                    version = self.get_lib_version(install_name)
                    req_file.write(f"{install_name}=={version}\n")
                else:
                    req_file.write(f"{install_name}\n")

    def process_directory(self, directory: str, with_versions: bool = False):
        """Process all Python files in a directory and save their imports."""
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    self.extract_imports(os.path.join(root, file))

        with open("requirements.txt", "w") as req_file:
            for lib in sorted(self.imported_libs):
                install_name = self.get_install_name(lib)
                if with_versions:
                    version = self.get_lib_version(install_name)
                    req_file.write(f"{install_name}=={version}\n")
                else:
                    req_file.write(f"{install_name}\n")

def main():
    parser = argparse.ArgumentParser(description="FreezeLibs: Extract and save Python library imports.")
    parser.add_argument("-F", "--file", help="Extract imports from a single Python file (without versions).")
    parser.add_argument("-P", "--project", help="Extract imports from all Python files in a directory (without versions).")
    parser.add_argument("-FW", "--file-with-versions", help="Extract imports from a single Python file (with versions).")
    parser.add_argument("-PW", "--project-with-versions", help="Extract imports from all Python files in a directory (with versions).")
    parser.add_argument("-V", "--version", action="version", version=f"FreezeLibs {__version__}", help="Show version and exit.")

    args = parser.parse_args()

    freeze_libs = FreezeLibs()

    if args.file:
        freeze_libs.save_imports(args.file, with_versions=False)
        print(f"Imported libraries saved to requirements.txt (without versions).")
    elif args.project:
        freeze_libs.process_directory(args.project, with_versions=False)
        print(f"Imported libraries saved to requirements.txt (without versions).")
    elif args.file_with_versions:
        freeze_libs.save_imports(args.file_with_versions, with_versions=True)
        print(f"Imported libraries saved to requirements.txt (with versions).")
    elif args.project_with_versions:
        freeze_libs.process_directory(args.project_with_versions, with_versions=True)
        print(f"Imported libraries saved to requirements.txt (with versions).")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()