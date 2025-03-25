import os
import time
import unittest
from clmediakit import CLMetaData
from clmediakit import MetadataExtractor


class TestCLMetaData(unittest.TestCase):

    def test_metadata_extraction(self):
        # Get directory path from environment variable
        directory_path = "./media"  # os.getenv("MEDIA_DIRECTORY_PATH")
        self.assertIsNotNone(directory_path, "MEDIA_DIRECTORY_PATH is not set")
        self.assertTrue(os.path.isdir(directory_path), "Directory does not exist")
        print(f"Processing { directory_path }")
        extractor = MetadataExtractor()
        hasTitle = False
        for root, _, files in os.walk(directory_path):
            for file_name in files:
                if not file_name.startswith("."):
                    file_path = os.path.join(root, file_name)

                    with self.subTest(file=file_path):

                        # Extract metadata
                        metadata = CLMetaData.from_media(file_path, extractor=extractor)

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
                            self.assertTrue(
                                hasattr(metadata, "Duration")
                            )  # Example field

                        # Print performance
                        if not hasTitle:
                            print(f"{metadata.keys()}")
                            hasTitle = True
                        print(f"{metadata.values()}")


if __name__ == "__main__":
    unittest.main()
