# s3pathx

A lightweight, Pythonic S3 utility class with a `pathlib`-style API for effortless S3 file operations — upload, download, rename, list, delete — and temporary local caching with context manager support.

## 🚀 Features

- ✅ Pathlib-style method names: `ls`, `unlink_all`, `mv_to_s3`, `open`, `rename`
- ✅ Context Manager support — auto-cleans local cache directory
- ✅ Read S3 objects directly as text or bytes: `read_text()` / `read_bytes()`
- ✅ Easily integrates with S3-compatible storage: AWS S3, Cloudflare R2, MinIO, etc.
- ✅ Clean, minimal design suitable for data pipelines and tools

> ✅ Currently tested and verified with **Cloudflare R2**
> 📌 MinIO testing is planned in upcoming versions

## 📦 Installation

```bash
pip install s3pathx
```

## 🔧 Quick Example

```python
from s3pathx import S3Path

with S3Path(
    bucket_name="your-bucket",
    prefix="tmp/",
    access_key="your-access-key",
    secret_key="your-secret-key",
    endpoint_url="https://your-s3-compatible-endpoint"
) as s3:
    # Upload a local file to S3
    s3.mv_to_s3("local.txt")

    # Read text content directly from S3
    content = s3.read_text("local.txt")
    print(content)

    # Rename a file in S3
    s3.rename("local.txt", "renamed.txt")

    # Download S3 file locally and access via Path
    path = s3.open("renamed.txt")
    print(path.read_text())

    # Delete all `.txt` files in the S3 prefix
    s3.unlink_all([".txt"])
```

## 🗂 Methods Overview

| Method | Description |
|--------|-------------|
| `ls(suffix_filter)` | List all files in the prefix (optionally filtered by suffix) |
| `mv_to_s3(local_path)` | Upload a file to S3 |
| `mv_from_s3(s3_filename, local_path)` | Download a file from S3 |
| `read_text(s3_filename)` | Read file content from S3 (as string) |
| `read_bytes(s3_filename)` | Read file content from S3 (as bytes) |
| `open(s3_filename)` | Download file to temp dir and return a `Path` object |
| `unlink_all(suffix_filter)` | Delete files by suffix |
| `rename(old, new)` | Rename S3 object (copy + delete) |

## ☁️ S3-Compatible Support

`s3pathx` supports all S3-compatible object storage:

- Amazon S3
- Cloudflare R2 ✅ tested
- MinIO ⏳ planned testing
- Wasabi
- DigitalOcean Spaces
- Self-hosted S3

## 🔐 Security

- Uses `__token__` + `PYPI_API_TOKEN` for secure publishing
- Supports GitHub Actions + Environments for CI/CD

## 🧪 Testing

You can use `pytest` or `moto` for mocking S3 in unit tests.

## 📄 License

MIT License © 2025 Hotwa

