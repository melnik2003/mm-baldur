from codecs import ignore_errors
from pathlib import Path
import sys

from handler_factory import HandlerFactory
from tools import clean_dir, copy_file
from logging_tools import get_logger


logger = get_logger()

class FileManager:
    def __init__(self, base_config: dict, ops_config: dict) -> None:
        # Extracting params from config
        main: dict = base_config['main']
        self.input_dir = Path(main['input_dir_path'])
        self.output_dir = Path(main['output_dir_path'])
        self.clean_output_dir_flag: bool = main['clean_output_dir']
        self.recursive_flag: bool = main['recursive']
        self.overwrite_flag: bool = main['overwrite_files']
        self.copy_other_flag: bool = main['copy_other_files']
        self.ignore_errors: bool = main['ignore_errors']
        self.media_exts = {k: v for k, v in base_config.items() if k != 'main'}
        self.media_ops = {k: v for k, v in ops_config.items()}

        self.total_files = 0
        self.files_processed = 0
        self.current_file_number = 0
        self.prefix = ""

    def run(self):
        if self.clean_output_dir_flag:
            clean_dir(self.output_dir)

        files = self._get_input_files()

        if not files:
            logger.warning('No files to process in the input directory.')
            return

        self.total_files = len(files)

        for file in files:
            self.current_file_number += 1
            self.prefix = f'[{self.current_file_number}/{self.total_files}]'
            try:
                self._manage_file(file)
            except Exception as e:
                logger.error(f'{self.prefix} Failed to process {file}: {e}')
                if self.ignore_errors: pass
                else: raise

        logger.info(f"{self.files_processed}/{self.total_files} files processed")

    def _get_input_files(self) -> list[Path]:
        if self.recursive_flag:
            files = self.input_dir.rglob('*')
        else:
            files = self.input_dir.glob('*')

        files = [f for f in files if f.is_file()]
        
        return files

    def _manage_file(self, file: Path) -> None:
        relative_path = file.relative_to(self.input_dir)
        target_path = self.output_dir / relative_path

        if not target_path.parent.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)

        if target_path.exists() and not self.overwrite_flag:
            logger.info(f"Skipping file (already exists): {target_path}")
            return

        extension = file.suffix[1:].lower()

        for media_type, params in self.media_exts.items():
            if extension in params['input_exts']:
                output_ext = params['output_ext']
                if output_ext == 'native':
                    output_ext = extension
                target_path = target_path.with_suffix(f".{output_ext}")
                self._delegate_media_file(file, target_path, media_type)
                return

        logger.info(f"{self.prefix} Skipping file: {file}")

        if self.copy_other_flag:
            copy_file(file, target_path)

    def _delegate_media_file(self, file: Path, target_path: Path, media_type: str) -> None:
        try:
            handler = HandlerFactory.get_handler(media_type)
        except ValueError as e:
            logger.error(f'Failed to get handler for {media_type}: {e}')
            return

        operations = self.media_ops.get(media_type, {})

        logger.info(f"{self.prefix} Processing file: {file} -> {target_path}")

        success = handler.run(file, target_path, operations.copy())

        if success:
            self.files_processed += 1
