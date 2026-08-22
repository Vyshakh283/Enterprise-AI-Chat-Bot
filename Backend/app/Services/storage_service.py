from pathlib import Path
import shutil

from fastapi import UploadFile


class StorageService:

    def __init__(self):

        self.base_path = Path(
            "storage/documents"
        ).resolve()

        self.base_path.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _get_safe_path(
        self,
        storage_key: str,
    ) -> Path:

        file_path = (
            self.base_path / storage_key
        ).resolve()

        # Prevent ../ path traversal.
        if self.base_path not in file_path.parents:

            raise ValueError(
                "Invalid storage path"
            )

        return file_path

    def save_file(
        self,
        file: UploadFile,
        storage_key: str,
    ) -> str:


        if not file.filename:

            raise ValueError(
                "Uploaded file must have a filename"
            )

        file_path = self._get_safe_path(
            storage_key
        )

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        try:

            with file_path.open("wb") as buffer:

                shutil.copyfileobj(
                    file.file,
                    buffer,
                )

        except Exception:

            # Remove partially written file.
            if file_path.exists():

                try:
                    file_path.unlink()

                except OSError:
                    pass

            raise

        return str(file_path)

    def delete_file(
        self,
        storage_key: str,
    ) -> None:

        file_path = self._get_safe_path(
            storage_key
        )

        if file_path.exists():

            file_path.unlink()

        # Remove empty document directory.
        parent_directory = file_path.parent

        try:

            parent_directory.rmdir()

        except OSError:
            # Directory may not be empty.
            # This is not a failure.
            pass