# CLMediaKit

CLMediaKit is a Python library designed for extracting metadata from media
files (images and videos), managing video hash indices, and querying similar
media using efficient indexing techniques.

## Features

- Extract metadata from media files using ExifTool.
- Compute difference hash (dHash) and MD5 hash for images and videos.
- Manage and query video hash indices using HNSW (Hierarchical Navigable
  Small World) indexing.

## Project Structure

```bash
clmediakit/
├── cl_metadata.py         # Handles metadata extraction and hashing for media files.
├── hnsw_index_db.py       # Manages HNSW index for storing and querying video hashes.
├── exif_tool_wrapper.py   # Wrapper for ExifTool to extract metadata from media files.
```

## Installation

1. Install the package using pip:

   ```bash
   pip install clmediakit
   ```

2. Ensure [ExifTool](https://exiftool.org/) is installed and available in your
   system's PATH.

## Usage

### Extract Metadata

Use the `CLMetaData` class to extract metadata from a media file:

```python
from clmediakit.cl_metadata import CLMetaData

metadata = CLMetaData.from_media("path/to/media/file")
print(metadata.CreateDate, metadata.FileSize, metadata.MIMEType)
```

### Manage Video Hash Index

Use the `HNSWIndexDB` class to add and query video hashes:

```python
from clmediakit.hnsw_index_db import HNSWIndexDB

index_db = HNSWIndexDB("path/to/index/file")
index_db.add(video_id=1, hash_val=[0.1, 0.2, 0.3])
ids, distances = index_db.query(hash_val=[0.1, 0.2, 0.3])
print(ids, distances)
```

### Extract Metadata with ExifTool

Use the `MetadataExtractor` class to extract specific metadata tags:

```python
from clmediakit.exif_tool_wrapper import MetadataExtractor

extractor = MetadataExtractor()
metadata = extractor.extract_metadata("path/to/media/file", 
                                      tags=["CreateDate", "FileSize"])
print(metadata)
```

## Requirements

- Python 3.7+
- [ExifTool](https://exiftool.org/)
- Required Python libraries (see `requirements.txt`)

## License

This project is licensed under the MIT License. See the `LICENSE` file for
details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for
any improvements or bug fixes.

## Acknowledgments

- [ExifTool](https://exiftool.org/) for metadata extraction.
- [HNSWLib](https://github.com/nmslib/hnswlib) for efficient indexing and
  querying.
