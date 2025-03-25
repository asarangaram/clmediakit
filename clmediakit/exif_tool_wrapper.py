import json
import os
import subprocess


class MetadataExtractor:
    def __init__(self):
        if not self.is_exiftool_available():
            raise RuntimeError("ExifTool is not installed or not found in PATH.")

    def is_exiftool_available(self):
        try:
            subprocess.run(
                ["exiftool", "-ver"], check=True, capture_output=True, text=True
            )
            return True
        except FileNotFoundError:
            return False
        except subprocess.CalledProcessError:
            return False

    def extract_metadata(self, filepath, tags=None):
        if not os.path.exists(filepath):
            print(f"Error: File not found - {filepath}")
            return {}

        if not tags:
            print(f"Error: tags not provided.")
            return {}

        # Format tags to be case-insensitive and match from any group
        tag_args = [f"-{tag}" for tag in tags]

        try:
            result = subprocess.run(
                ["exiftool", "-j"] + tag_args + [filepath],  # -j: JSON output
                capture_output=True,
                text=True,
                check=True,
            )
            metadata = json.loads(result.stdout)
            if not metadata:
                print("Warning: No metadata found.")
                return {}
            return metadata[0]  # ExifTool returns a list; we take the first result

        except subprocess.CalledProcessError as e:
            print(f"Error running ExifTool: {e}")
            return {}

        except json.JSONDecodeError:
            print("Error: Failed to parse ExifTool JSON output.")
            return {}
