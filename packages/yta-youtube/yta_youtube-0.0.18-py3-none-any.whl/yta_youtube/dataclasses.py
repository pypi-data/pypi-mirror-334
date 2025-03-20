from yta_youtube.enums import AudioFormatQuality, VideoFormatQuality, AudioFormatExtension, VideoFormatExtension, YoutubeVideoLanguage
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.number import NumberValidator
from dataclasses import dataclass


@dataclass
class YoutubeVideoScene:
    """
    Class to represent a youtube video scene, perfect
    to contain the data of the most viewed moments.
    """

    start_time: float
    """
    The time moment in which the video scene starts.
    """
    end_time: float
    """
    The time moment in which the video scene ends.
    """
    rating: float
    """
    The rating, from 0 to 1, of how viewed has been
    the scene.
    """

    @property
    def mid_time(self) -> float:
        """
        The time moment in the middle of the scene, after
        the 'start_time' and before the 'end_time'. This
        value is useful if we need to extract a part of
        this scene but not the whole scene.
        """
        return (self.start_time + self.end_time) / 2

    def __init__(
        self,
        start_time: float,
        end_time: float,
        rating: float
    ):
        if not NumberValidator.is_positive_number(start_time):
            raise Exception('The "start_time" parameter provided is not a positive number.')
        
        if not NumberValidator.is_positive_number(end_time):
            raise Exception('The "end_time" parameter provided is not a positive number.')
        
        if not NumberValidator.is_number_between(rating, 0.0, 1.0):
            raise Exception('The "rating" value must be between [0.0, 1.0]')

        if start_time > end_time:
            raise Exception('The "start_time" cannot be after the "end_time".')
        
        self.start_time = start_time
        self.end_time = end_time
        self.rating = rating

@dataclass
class YoutubeVideoChapter:
    """
    Class to represent a chapter in a youtube video.
    A chapter is an introduction to the video content
    in different time moments.

    The different video chapters are defined by the
    author of the video and are not always available
    in a youtube video.
    """

    start_time: float
    """
    The time moment in which the video chapter starts.
    """
    end_time: float
    """
    The time moment in which the video chapter ends.
    """
    title: str
    """
    The title of the video chapter.
    """

    @property
    def mid_time(self) -> float:
        """
        The time moment in the middle of the scene, after
        the 'start_time' and before the 'end_time'. This
        value is useful if we need to extract a part of
        this scene but not the whole scene.
        """
        return (self.start_time + self.end_time) / 2

    def __init__(
        self,
        start_time: float,
        end_time: float,
        title: str
    ):
        if not NumberValidator.is_positive_number(start_time):
            raise Exception('The "start_time" parameter provided is not a positive number.')
        
        if not NumberValidator.is_positive_number(end_time):
            raise Exception('The "end_time" parameter provided is not a positive number.')
        
        if not PythonValidator.is_string(title):
            raise Exception('The "title" parameter provided is not a valid string.')

        if start_time > end_time:
            raise Exception('The "start_time" cannot be after the "end_time".')
        
        self.start_time = start_time
        self.end_time = end_time
        self.title = title

@dataclass
class YoutubeVideoAudioFormat:
    """
    Class to represent an audio format of a youtube
    video.
    """

    id: str
    """
    The identifier of the audio format. This is the
    value we must use to download the corresponding
    format using the yt-dlp library.
    """
    url: str
    """
    The url to download the associated audio file.
    """
    quality: AudioFormatQuality
    """
    The quality of the associated audio file.
    """
    file_size: int
    """
    The size of the associated audio file.
    """
    language: YoutubeVideoLanguage
    """
    The language in which the audio file is built.
    """
    extension: AudioFormatExtension
    """
    The extension of the associated audio file.

    TODO: Is this the same value as 'audio_extension' (?)
    """
    audio_extension: str
    """
    The extension of the associated audio file.

    TODO: Is this the same value as 'extension' (?)
    TODO: Please, use AudioExtension enum
    """
    abr: str
    """
    The audio bit rate value.

    TODO: I don't know if string or what
    TODO: This can be 'none'
    """

    def __init__(
        self,
        id: str,
        url: str,
        quality: AudioFormatQuality,
        file_size: int,
        language: YoutubeVideoLanguage,
        extension: AudioFormatExtension,
        audio_extension: AudioFormatExtension,
        abr: str
    ):
        language = YoutubeVideoLanguage.to_enum(language)
        quality = AudioFormatQuality.to_enum(quality)
        extension = AudioFormatExtension.to_enum(extension)
        audio_extension = AudioFormatExtension.to_enum(audio_extension)

        self.id = id
        self.url = url
        self.quality = quality
        self.file_size = file_size
        self.language = language
        self.extension = extension
        self.audio_extension = audio_extension
        self.abr = abr

@dataclass
class YoutubeVideoVideoFormat:
    """
    Class to represent a video format of a youtube
    video.
    """

    id: str
    """
    The identifier of the video format. This is the
    value we must use to download the corresponding
    format using the yt-dlp library.
    """
    url: str
    """
    The url to download the associated video file.
    """
    quality: VideoFormatQuality
    """
    The quality of the associated video file.
    """
    file_size: int
    """
    The size of the associated video file.
    """
    width: int
    """
    The width of the associated video file.
    """
    height: int
    """
    The height of the associated video file.
    """
    extension: VideoFormatExtension
    """
    The extension of the associated video file.

    TODO: Is this the same value as 'video_extension' (?)
    """
    video_extension: str
    """
    The extension of the associated video file.

    TODO: Is this the same value as 'extension' (?)
    TODO: Please, use VideoExtension enum
    """
    fps: float
    """
    The number of frames per second of the associated
    video file.

    TODO: Maybe this is int and not float
    """
    aspect_ratio: float
    """
    The aspect ratio of the associated video file, 
    which is the proportional relationship between
    the width of a video image compared to its
    height.
    """
    vbr: float
    """
    The video bit rate value.

    TODO: I don't know if it can be string ('none')
    """

    def __init__(
        self,
        id: str,
        url: str,
        quality: VideoFormatQuality,
        file_size: int,
        width: int,
        height: int,
        extension: VideoFormatExtension,
        video_extension: VideoFormatExtension,
        fps: float,
        aspect_ratio: float,
        vbr: float
    ):
        quality = VideoFormatQuality.to_enum(quality)
        extension = VideoFormatExtension.to_enum(extension)
        video_extension = VideoFormatExtension.to_enum(video_extension)

        self.id = id
        self.url = url
        self.quality = quality
        self.file_size = file_size
        self.width = width
        self.height = height
        self.extension = extension
        self.video_extension = video_extension
        self.fps = fps
        self.aspect_ratio = aspect_ratio
        self.vbr = vbr

@dataclass
class YoutubeVideoReturn:
    """
    @dataclass
    Class to represent a youtube video (or only its
    audio) that has been downloaded and to return the
    information about that video (including its id
    for non-repeating purposes) and the filename with
    which the video has been downloaded.
    """

    youtube_video: 'YoutubeVideo'
    """
    The video that has been downloaded. Remember that
    the download could have been only the audio, but
    here it is the information about the whole video.
    """
    output_filename: str
    """
    The local filename with which the video has been
    downloaded and stored locally.
    """

    def __init__(
        self,
        youtube_video: 'YoutubeVideo',
        output_filename: str
    ):
        self.youtube_video = youtube_video
        self.output_filename = output_filename
    
    @property
    def id(self):
        """
        The id of the youtube video that has been
        downloaded.
        """
        return self.youtube_video.id