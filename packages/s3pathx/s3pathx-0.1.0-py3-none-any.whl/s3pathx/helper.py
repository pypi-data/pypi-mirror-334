from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory
import boto3


@dataclass
class S3Path:
    bucket_name: str
    prefix: str
    access_key: str
    secret_key: str
    endpoint_url: str
    auto_clean: bool = True

    temp_dir_obj: TemporaryDirectory = field(init=False)
    local_cache_dir: Path = field(init=False)

    def __post_init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url
        )
        if not self.prefix.endswith("/"):
            self.prefix += "/"
        self.temp_dir_obj = TemporaryDirectory()
        self.local_cache_dir = Path(self.temp_dir_obj.name)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.auto_clean:
            self.temp_dir_obj.cleanup()
            print(f"🧹 Temp directory cleaned up: {self.local_cache_dir}")

    def ls(self, suffix_filter=None):
        response = self.client.list_objects_v2(Bucket=self.bucket_name, Prefix=self.prefix)
        files = []
        for obj in response.get("Contents", []):
            key = obj["Key"]
            if suffix_filter:
                if any(key.endswith(suffix) for suffix in suffix_filter):
                    files.append(key)
            else:
                files.append(key)
        return files

    def mv_to_s3(self, local_path: str | Path, s3_filename: str = None):
        local_path = Path(local_path)
        if not s3_filename:
            s3_filename = local_path.name
        s3_key = str(Path(self.prefix) / s3_filename)
        self.client.upload_file(str(local_path), self.bucket_name, s3_key)
        print(f"✅ Uploaded to S3: {local_path} → s3://{self.bucket_name}/{s3_key}")

    def mv_from_s3(self, s3_filename: str, local_path: str | Path = None):
        s3_key = str(Path(self.prefix) / s3_filename)
        if not local_path:
            local_path = self.local_cache_dir / s3_filename
        else:
            local_path = Path(local_path)
        local_path.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(self.bucket_name, s3_key, str(local_path))
        print(f"✅ Downloaded from S3: s3://{self.bucket_name}/{s3_key} → {local_path}")
        return local_path

    def read_text(self, s3_filename: str, encoding='utf-8') -> str:
        s3_key = str(Path(self.prefix) / s3_filename)
        obj = self.client.get_object(Bucket=self.bucket_name, Key=s3_key)
        content = obj['Body'].read()
        return content.decode(encoding)

    def read_bytes(self, s3_filename: str) -> bytes:
        s3_key = str(Path(self.prefix) / s3_filename)
        obj = self.client.get_object(Bucket=self.bucket_name, Key=s3_key)
        return obj['Body'].read()

    def open(self, s3_filename: str) -> Path:
        return self.mv_from_s3(s3_filename)

    def unlink_all(self, suffix_filter=None):
        files_to_delete = self.ls(suffix_filter=suffix_filter)
        if not files_to_delete:
            print("ℹ️ No matching files to delete.")
            return
        delete_objs = [{"Key": key} for key in files_to_delete]
        self.client.delete_objects(Bucket=self.bucket_name, Delete={"Objects": delete_objs})
        print("✅ Deleted:")
        for obj in delete_objs:
            print(f"  - {obj['Key']}")

    def rename(self, old_filename: str, new_filename: str):
        old_key = str(Path(self.prefix) / old_filename)
        new_key = str(Path(self.prefix) / new_filename)
        copy_source = {'Bucket': self.bucket_name, 'Key': old_key}
        self.client.copy(copy_source, self.bucket_name, new_key)
        self.client.delete_object(Bucket=self.bucket_name, Key=old_key)
        print(f"✅ Renamed: {old_key} → {new_key}")
