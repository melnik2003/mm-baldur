import copy

from cerberus_validations import validate_file, validate_dir, validate_new_dir


class _Constants:
    """Class for storing program constants. Encapsulates data to prevent accidental modifications."""

    def __init__(self):
        self._default_log_level: str = 'info'
        self._default_config_file: str = 'config.yaml'
        self._image_size_range: tuple = (1, 9999)

        self._supported_types: dict = {}
        self._default_base_config_params: dict = {}
        self._cli_params_schema: dict = {}
        self._base_config_schema: dict = {}
        self._ops_config_schema: dict = {}
        self._test_params: dict = {}

        self.init_dicts()

    def init_dicts(self):
        """Initializes dictionaries with data. Separated for better readability."""
        self._supported_types = {
            'image': ['blp', 'bmp', 'dib', 'icns', 'ico', 'msp', 'sgi', 'jpg', 'jpeg', 'png', ],
            'audio': ['mp3', 'flac', 'ogg']
            # Video types are in development
        }

        self._default_base_config_params = {
            'main': {
                'input_dir_path': 'input',
                'output_dir_path': 'output',
                'clean_output_dir': True,
                'recursive': True,
                'overwrite_files': True,
                'copy_other_files': True,
                'inore_errors': True
            },
            'image': {
                'input_exts': 'all',
                'output_ext': 'native'
            }
        }

        self._cli_params_schema = {
            'log_level': {'type': 'string', 'required': True, 'allowed': ['debug', 'info', 'warning', 'error']},
            'config_file': {'type': 'string', 'required': True, 'check_with': validate_file},
        }

        self._base_config_schema = {
            'main': {
                'type': 'dict',
                'allow_unknown': False,
                'schema': {
                    'input_dir_path': {'type': 'string', 'check_with': validate_dir},
                    'output_dir_path': {'type': 'string', 'check_with': validate_new_dir},
                    'clean_output_dir': {'type': 'boolean'},
                    'recursive': {'type': 'boolean'},
                    'overwrite_files': {'type': 'boolean'},
                    'copy_other_files': {'type': 'boolean'},
                    'ignore_errors': {'type': 'boolean'}
                }
            },
            'image': {
                'type': 'dict',
                'allow_unknown': True,
                'schema': {
                    'input_exts': {'anyof': [
                        {'type': 'list', 'allowed': self.supported_types['image']},
                        {'type': 'string', 'allowed': ['all']}
                    ]},
                    'output_ext': {'type': 'string', 'allowed': self.supported_types['image'] + ['native']}
                }
            }
        }

        self._ops_config_schema = {
            'image': {
                'type': 'dict',
                'allow_unknown': False,
                'schema': {
                    'rotate': {'type': 'integer', 'min': 0, 'max': 360},
                    'resize': {
                        'schema': {
                            'width': {'type': 'integer', 'min': 1, 'max': 9999, 'required': True},
                            'height': {'type': 'integer', 'min': 1, 'max': 9999, 'required': True},
                            'method': {'type': 'string', 'required': False,
                                       'allowed': ['default']},
                            'resampling': {'type': 'string', 'required': False,
                                           'allowed': ['nearest', 'bilinear', 'bicubic', 'lanczos', 'box', 'hamming']}
                        }
                    },
                    'color_mode': {'type': 'string', 'required': True,
                                   'allowed': ['greyscale', 'black_and_white', 'cmyk', 'rgb', 'web_palette', 'adaptive_palette']}
                }
            }
        }


        self._test_params = {
            'main': {
                'input_dir_path': 'asdsadsa',
                'output_dir_path': 'output',
                'copy_other_files': True
            },
            'image': {
                'input_exts': 'all',
                'output_ext': 'native'
            }
        }

    @property
    def default_log_level(self):
        return self._default_log_level

    @property
    def default_config_file(self):
        return self._default_config_file

    @property
    def image_size_range(self):
        return self._image_size_range

    @property
    def supported_types(self):
        return copy.deepcopy(self._supported_types)

    @property
    def default_base_config_params(self):
        return copy.deepcopy(self._default_base_config_params)

    @property
    def cli_params_schema(self):
        return copy.deepcopy(self._cli_params_schema)

    @property
    def base_config_schema(self):
        return copy.deepcopy(self._base_config_schema)

    @property
    def ops_config_schema(self):
        return copy.deepcopy(self._ops_config_schema)

    @property
    def test_params(self):
        return copy.deepcopy(self._test_params)


CONST = _Constants()