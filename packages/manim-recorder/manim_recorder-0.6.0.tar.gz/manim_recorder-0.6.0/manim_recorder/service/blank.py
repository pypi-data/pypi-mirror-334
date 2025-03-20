from pathlib import Path
from pydub import AudioSegment
import srt
import os
import datetime
from manim_recorder.service import AudioService, logger
from manim_recorder.multimedia import remove_silence


class BlankService(AudioService):
    """
    Service for generating silent audio segments based on input text.

    Attributes:
        blank_duration (int): Duration of silence in seconds.
        sound_extension (str): File extension for audio files.
        language (str): Language code for wpm settings.
        wpm (int): Words per minute rate for audio duration calculation.
    """

    def __init__(
        self,
        global_speed: float = 1.00,
        cache_dir: Path = None,
        language: str = "en",
        wpm: int = 130,
        blank_duration: int = None,
        sound_extension: str = "wav",
        audio_src: str = None,
        audio_srt: str = None,
        remove_silence: bool = False,
        silence_thresh_db: int = -14,
        min_silence_len: int = 1000,
        **kwargs,
    ):
        """Initialize the audio service with specified parameters.

        Args:
            global_speed (float): Playback speed multiplier (default is 1.00).
            cache_dir (Path): Directory for cached audio files (default is None).
            language (str): Language code for wpm settings (default is "en").
            wpm (int): Words per minute rate for audio duration calculation (default is 130).
            blank_duration (int): Duration of silence in seconds (default is None).
            sound_extension (str): File extension for audio files (default is "wav").
            audio_src (audio): None
            audio_srt (str): None
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(global_speed=global_speed, cache_dir=cache_dir, **kwargs)
        self.blank_duration = blank_duration
        self.sound_extension = sound_extension
        self.language = language
        self.audio_src = None
        self.audio_srt = None
        self.remove_silence = remove_silence
        self.silence_thresh_db = silence_thresh_db
        self.min_silence_len = min_silence_len
        if audio_src:
            audio_src = Path(audio_src)
            if audio_src.is_file():
                logger.info("Load Audio File : %s", audio_src)
                self.audio_src = audio_src

            if audio_srt is None:
                audio_srt = Path(audio_src).with_suffix(".srt")

        if audio_srt:
            if os.path.exists(audio_srt) and os.path.isfile(audio_srt):
                logger.info("Load Audio Subtitle : %s", audio_srt)
                with open(audio_srt) as srt_caption:
                    self.audio_srt = list(srt.parse(srt_caption.read()))

        self.wpm = self.wpm_values(wpm, language)

    def wpm_values(self, wpm, language="en"):
        """Get words per minute value based on the specified language."""
        wpm = {
            "en": 130,
            "es": 155,
            "fr": 140,
            "de": 140,
            "it": 155,
            "zh": 135,
            "hi": 140,
            "ja": 135,
            "ru": 140,
            "ar": 135,
            "pt": 140,
            "ko": 140,
        }.get(language, wpm)
        return wpm if wpm is not None else 155

    def generate_from_text(
        self,
        text: str,
        cache_dir: str = None,
        path: str = None,
        voice_id: int = None,
        mobject: str | None = None,
        **kwargs,
    ) -> dict:
        """Generate a silent audio file from the provided text."""
        if cache_dir is None:
            cache_dir = self.sounds_dir

        input_data = {"id": voice_id, "input_text": text}
        cached_result = self.get_cached_result(
            input_data, cache_dir, voice_id=voice_id, **kwargs
        )
        if cached_result is not None:
            return cached_result

        audio_path = (
            self.get_audio_basename(**kwargs) + f".{self.sound_extension}"
            if path is None
            else path
        )

        duration = None
        if self.search_caption(text, self.sounds_dir / audio_path):
            logger.info("Use Audio File : %s", self.audio_src)
        else:
            duration = self.text2audio(text) or 1
            silent_audio = AudioSegment.silent(duration=duration * 1000)
            silent_audio.export(
                self.sounds_dir / audio_path, format=self.sound_extension
            )
        
        return {"input_data": input_data, "original_audio": audio_path}

    def text2audio(self, txt: str):
        """Calculate audio duration based on input text."""
        if self.blank_duration is not None:
            return self.blank_duration
        if txt is None:
            return 1.0
        if self.wpm <= 0:
            raise ValueError("Words per minute must be greater than 0.")
        return (self.words_count(txt) / self.wpm) * 60

    def words_count(self, txt: str):
        """Count the number of words in the provided text."""
        return len(txt.split())

    def audio_cut_with_caption(self, duration: list, audio_file_path: Path):
        audio = AudioSegment.from_file(self.audio_src)
        cut_audio = audio[duration[0] : duration[1]]
        if self.remove_silence:
            cut_audio = remove_silence(
                cut_audio, self.silence_thresh_db, self.min_silence_len
            )
        cut_audio.export(audio_file_path, format="wav")
        return True

    def search_caption(self, text: str, audio_file_path: Path):
        if self.audio_src is None and self.audio_srt is None:
            return False
        for srt_caption in self.audio_srt:
            if srt_caption.content.strip().lower() == text.strip().lower():
                start = srt_caption.start.total_seconds() * 1000
                end = srt_caption.end.total_seconds() * 1000
                return self.audio_cut_with_caption([start, end], audio_file_path)
        return False
