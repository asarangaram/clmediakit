from datetime import datetime
import subprocess
import time

from imagehash import dhash as ImageHash
from videohash import VideoHash
import hashlib
from PIL import Image

from .exif_tool_wrapper import MetadataExtractor


class CLMetaData:
    """
    A class to represent and extract metadata from media files (images and videos).
    """

    chunk_size = 8192

    def __init__(
        self,
        filepath,
        CreateDate=None,
        FileSize=None,
        ImageHeight=None,
        ImageWidth=None,
        Duration=None,
        MIMEType=None,
        dHash=None,
        md5=None,
    ):
        """
        Initialize CLMetaData with optional metadata attributes.

        Args:
            CreateDate (str): Creation date of the media.
            FileSize (int): Size of the file in bytes.
            ImageHeight (int): Height of the image in pixels.
            ImageWidth (int): Width of the image in pixels.
            Duration (float): Duration of the video in seconds.
            MIMEType (str): MIME type of the media.
            dHash (str): Difference hash of the media.
            md5 (str): MD5 hash of the media.
        """
        self.filepath = filepath
        self.CreateDate = CreateDate
        self.FileSize = FileSize
        self.ImageHeight = ImageHeight
        self.ImageWidth = ImageWidth
        self.Duration = Duration
        self.MIMEType = MIMEType
        self.dHash = dHash
        self.md5 = md5

    def __repr__(self):
        return f"CLMetaData({self.__dict__})"

    def __str__(self):
        str = "{ "
        for key, value in self.__dict__.items():
            if value is not None:
                str += f"{key}: {value}, "
        str += "}"
        return str

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    def values(self):
        res = ", ".join(
            str(value) if value is not None else "None"
            for value in self.__dict__.values()
        )
        return res

    def keys(self):
        res = ", ".join(
            str(value) if value is not None else "None"
            for value in self.__dict__.keys()
        )
        return res

    @classmethod
    def from_media(cls, filepath, extractor=None):
        """
        Create a CLMetaData instance by extracting metadata from a media file.

        Args:
            filepath (str): Path to the media file.
            extractor (MetadataExtractor, optional): Metadata extractor instance.

        Returns:
            CLMetaData: An instance of CLMetaData with extracted metadata.
        """
        start_time = time.time()
        if extractor is None:
            extractor = MetadataExtractor()
        metadata = extractor.extract_metadata(
            filepath,
            tags=[
                "CreateDate",
                "FileSize",
                "ImageHeight",
                "ImageWidth",
                "Duration",
                "MIMEType",
            ],
        )
        CreateDate = metadata.get("CreateDate")
        if CreateDate is not None:
            try:
                CreateDate = datetime.strptime(CreateDate, "%Y:%m:%d %H:%M:%S")
            except ValueError:
                CreateDate = None
        cl_metadata = CLMetaData(
            filepath,
            CreateDate=CreateDate,
            FileSize=metadata.get("FileSize"),
            ImageHeight=metadata.get("ImageHeight"),
            ImageWidth=metadata.get("ImageWidth"),
            Duration=metadata.get("Duration"),
            MIMEType=metadata.get("MIMEType"),
        )
        if cl_metadata.MIMEType is not None:
            cl_metadata.dHash = cl_metadata.compute_dhash(filepath)
            cl_metadata.md5 = cl_metadata.compute_md5(filepath)
        end_time = time.time()
        cl_metadata.elapsed_time_ms = (end_time - start_time) * 1000
        return cl_metadata

    def is_video(self):
        """
        Check if the media is a video.

        Returns:
            bool: True if the media is a video, False otherwise.
        """
        return self.MIMEType is not None and self.MIMEType.startswith("video")

    def is_image(self):
        """
        Check if the media is an image.

        Returns:
            bool: True if the media is an image, False otherwise.
        """
        return self.MIMEType is not None and self.MIMEType.startswith("image")

    def compute_dhash(self, filepath):
        """
        Compute the difference hash (dHash) of the media.

        Returns:
            str: The computed dHash, or None if the media type is unsupported.
        """
        if self.is_video():
            return VideoHash(path=filepath).hash
        elif self.is_image():
            return bin(int(str(ImageHash(Image.open(filepath))), 16))
        else:
            return None

    def compute_md5(self, filepath):
        """
        Compute the MD5 hash of the media.

        Returns:
            str: The computed MD5 hash, or None if the media type is unsupported.
        """
        if self.is_video():
            cmd = [
                "ffmpeg",
                "-i",
                filepath,
                "-an",
                "-map",
                "0:v",
                "-c:v",
                "copy",
                "-f",
                "rawvideo",
                "-",
            ]
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
            )
            md5_hash = hashlib.md5()

            while True:
                chunk = process.stdout.read(self.chunk_size)
                if not chunk:
                    break
                md5_hash.update(chunk)
            process.stdout.close()
            exit_code = process.wait()
            if exit_code != 0:
                raise RuntimeError(f"ffmpeg failed with exit code {exit_code}")
            return md5_hash.hexdigest()
        elif self.is_image():
            img = Image.open(filepath).convert("RGB")
            md5_hash = hashlib.md5()
            raw_data = img.tobytes()
            for i in range(0, len(raw_data), self.chunk_size):
                md5_hash.update(raw_data[i : i + self.chunk_size])
            return md5_hash.hexdigest()
        else:
            md5_hash = hashlib.md5()
            with open(filepath, "rb") as f:
                while chunk := f.read(8192):  # 8KB = 8192 bytes
                    md5_hash.update(chunk)
            return md5_hash.hexdigest()
