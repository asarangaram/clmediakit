import os
import time
import unittest
from clmediakit.cl_metadata import CLMetaData


class TestCLMetaData(unittest.TestCase):

    def test_metadata_extraction(self):
        # Get directory path from environment variable
        directory_path = "./media"  # os.getenv("MEDIA_DIRECTORY_PATH")
        self.assertIsNotNone(directory_path, "MEDIA_DIRECTORY_PATH is not set")
        self.assertTrue(os.path.isdir(directory_path), "Directory does not exist")

        # Supported media file extensions
        supported_extensions = {".jpg", ".jpeg", ".png", ".mp4", ".mkv", ".avi"}

        for root, _, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                with self.subTest(file=file_path):
                    # Start timing
                    start_time = time.time()

                    # Extract metadata
                    metadata = CLMetaData.from_media(file_path)

                    # End timing
                    end_time = time.time()

                    # Calculate elapsed time in milliseconds
                    elapsed_time_ms = (end_time - start_time) * 1000

                    # Assertions to confirm output
                    self.assertIsNotNone(metadata)

                    self.assertTrue(hasattr(metadata, "MIMEType"))
                    self.assertTrue(hasattr(metadata, "FileSize"))
                    if metadata.is_image() or metadata.is_video():
                        self.assertTrue(hasattr(metadata, "dHash"))
                        self.assertTrue(hasattr(metadata, "md5"))
                        self.assertTrue(hasattr(metadata, "CreateDate"))
                        self.assertTrue(hasattr(metadata, "ImageHeight"))
                        self.assertTrue(hasattr(metadata, "ImageWidth"))
                    if metadata.is_video():
                        self.assertTrue(hasattr(metadata, "Duration"))  # Example field

                    # Print performance
                    print(
                        f"Metadata extraction for {file_path} took {elapsed_time_ms:.2f} ms"
                    )


if __name__ == "__main__":
    unittest.main()
