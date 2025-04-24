from PIL import Image
from typing import Union


class ImageResizer:
    def __init__(self, image: Image, params: dict):
        self.image = image
        self.params = params

        self.target_width = params.get('width')
        self.target_height = params.get('height')
        self.target_size = (self.target_width, self.target_height)
        self.method = params.get('method')
        self.resample_str: str = params.get('resample')
        self.resample: int = Image.Resampling.LANCZOS
        self.offset: tuple[float, float] = params.get('offset') or (0.5, 0.5)
        # Tuple (x, y) where x and y are between 0 and 1 representing the position of the resized image.
        # For example, (0.5, 0.5) centers the image, (0, 0) aligns the image to the top-left corner,
        # and (1, 1) aligns the image to the bottom-right corner.
        self.color: Union[str, tuple[int, int, int]] = params.get('color') or (0, 0, 0)
        # Background color for padding. Can be a string (e.g., 'black') or an RGB tuple (e.g., (0, 0, 0))

    def prevalidate(self):
        if not isinstance(self.image, Image.Image):
            raise TypeError(f'ITE: image for ImageResizer must be an instance of Image.Image class')
        if self.image is None:
            raise ValueError(f'ITE: There is no input image for ImageResizer')
        if self.target_width is None:
            raise ValueError(f'ITE: Unable to get target width for ImageResizer')
        if self.target_height is None:
            raise ValueError(f'ITE: Unable to get target height for ImageResizer')

    def run(self) -> Image.Image:
        self.prevalidate()

        if self.resample_str is not None:
            self.convert_resample()

        match self.method:
            case None: self.resize_default()
            case 'stretch': self.resize_stretch()
            case 'fit': self.resize_fit()
            case 'fill': self.resize_fill()
            case 'fit_expand': self.resize_fit_expand()
            case _: raise ValueError(f'Unknown resize method {self.method}')

        return self.image

    def convert_resample(self):
        resampling_map = {
            'nearest': Image.Resampling.NEAREST,
            'bilinear': Image.Resampling.BILINEAR,
            'bicubic': Image.Resampling.BICUBIC,
            'lanczos': Image.Resampling.LANCZOS,
            'box': Image.Resampling.BOX,
            'hamming': Image.Resampling.HAMMING
        }

        self.resample = resampling_map.get(f'{self.resample_str}')
        if self.resample is None:
            raise ValueError(f'Unknown resampling method: {self.resample_str}')

        '''
        # Alternative:

        match self.resample.lower():
            case 'nearest': self.resample = Image.Resampling.NEAREST
            case 'bilinear': self.resample = Image.Resampling.BILINEAR
            case 'bicubic': self.resample = Image.Resampling.BICUBIC
            case 'lanczos': self.resample = Image.Resampling.LANCZOS
            case 'box': self.resample = Image.Resampling.BOX
            case 'hamming': self.resample = Image.Resampling.HAMMING
            case _: raise ValueError(f'Unknown resampling method: {self.resample}')
        '''

    def resize_default(self):
        self.resize_stretch()

    def resize_stretch(self):
        """
        Stretch the image to the given width and height, ignoring the original aspect ratio.
        """
        self.image = self.image.resize(self.target_size, self.resample)

    def resize_fit(self):
        """
        Resize the image to fit within the given width and height while maintaining aspect ratio
        """
        tw = self.target_width
        th = self.target_height

        aspect_ratio = self.get_aspect_ratio()
        target_aspect_ratio = tw / th

        if aspect_ratio > target_aspect_ratio:
            # Width is the limiting factor
            new_width = tw
            new_height = int(tw / aspect_ratio)
        else:
            # Height is the limiting factor
            new_width = int(th * aspect_ratio)
            new_height = th

        # Resize image while preserving aspect ratio
        self.image = self.image.resize((new_width, new_height), self.resample)

    def resize_fill(self):
        """
        Resize the image to fit within the given width and height while maintaining aspect ratio,
        then crop the image according to the provided offset.
        """
        tw = self.target_width
        th = self.target_height

        aspect_ratio = self.get_aspect_ratio()
        target_aspect_ratio = tw / th

        if aspect_ratio > target_aspect_ratio:
            # Height is the limiting factor
            new_width = int(th * aspect_ratio)
            new_height = th
        else:
            # Width is the limiting factor
            new_width = tw
            new_height = int(tw / aspect_ratio)

        # Resize image while preserving aspect ratio
        resized_image = self.image.resize((new_width, new_height), self.resample)

        # Calculate cropping box
        left = (new_width - tw) * self.offset[0]
        top = (new_height - th) * self.offset[1]
        right = left + tw
        bottom = top + th

        # Crop the resized image
        cropped_image = resized_image.crop((left, top, right, bottom))
        self.image = cropped_image

    def resize_fit_expand(self):
        """
        Resize the image to fit within the given width and height while maintaining aspect ratio,
        then add letterboxing or pillarboxing as necessary to fit the target dimensions.
        """
        tw = self.target_width
        th = self.target_height

        aspect_ratio = self.get_aspect_ratio()
        target_aspect_ratio = tw / th

        if aspect_ratio > target_aspect_ratio:
            # Width is the limiting factor
            new_width = tw
            new_height = int(tw / aspect_ratio)
        else:
            # Height is the limiting factor
            new_width = int(th * aspect_ratio)
            new_height = th

        # Resize image while preserving aspect ratio
        resized_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        resized_image = resized_image.convert("RGB")

        # Create a new canvas with the target dimensions and the specified color
        canvas = Image.new("RGB", (tw, th), self.color)

        # Calculate position to paste the resized image on the canvas
        paste_x = (tw - new_width) * self.offset[0]
        paste_y = (th - new_height) * self.offset[1]

        # Paste the resized image onto the canvas
        canvas.paste(resized_image, (int(paste_x), int(paste_y)))
        self.image = canvas

    def get_aspect_ratio(self) -> float:
        """Return the aspect ratio of the image as a tuple (width, height)."""
        width, height = self.image.size
        aspect_ratio = width / height
        return aspect_ratio


class ColorModeConverter:
    def __init__(self, image: Image.Image, color_mode: str):
        self.image = image
        self.color_mode = color_mode

    def prevalidate(self):
        if not isinstance(self.image, Image.Image):
            raise TypeError(f'ITE: image for ColorModeConverter must be an instance of Image.Image class')
        if self.image is None:
            raise ValueError(f'ITE: There is no input image for ColorModeConverter')
        if not isinstance(self.color_mode, str):
            raise ValueError(f'ITE: color_mode for ColorModeConverter must be a string var')
        if self.color_mode is None:
            raise ValueError(f'ITE: Unable to get color_mode for ColorModeConverter')

    def run(self):
        self.prevalidate()

        match self.color_mode.lower():
            case 'greyscale': self.image = self.image.convert('L')
            case 'black-and-white': self.image = self.image.convert('1')
            case 'rgb': self.image = self.image.convert('RGB')
            case 'rgba': self.image = self.image.convert('RGBA')
            case 'ycbcr': self.image = self.image.convert('YCbCr')
            case 'cmyk': self.image = self.image.convert('CMYK')
            case 'lab': self.image = self.image.convert('LAB')
            case 'hsv': self.image = self.image.convert('HSV')
            case _: raise ValueError(f'Unknown color_mode {self.color_mode}')

        return self.image