from base_classes import MediaHandler
from image_handler import ImageHandler
from audio_handler import AudioHandler
from video_handler import VideoHandler

class HandlerFactory:
    @staticmethod
    def get_handler(media_type: str) -> MediaHandler:
        match media_type:
            case 'image': return ImageHandler()
            case 'audio': return AudioHandler()
            case 'video': return VideoHandler()
            case _:
                raise ValueError(f"Unsupported media type: {media_type}")