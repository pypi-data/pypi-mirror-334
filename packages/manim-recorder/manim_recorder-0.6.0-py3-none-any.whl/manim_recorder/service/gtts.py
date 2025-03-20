from pathlib import Path
from manim import logger
import sys
from manim_recorder.service import AudioService
from gtts import gTTS, gTTSError


class GTTSService(AudioService):
    def __init__(self, lang="en", tld="com", **kwargs):
        AudioService.__init__(self, **kwargs)
        self.lang = lang
        self.tld = tld

    def generate_from_text(
        self,
        text: str,
        cache_dir: str = None,
        path: str = None,
        voice_id: int = -1,
        sound_recording_skip: bool = True,
        mobject=None,
        animations_hashes=None,
        num_plays=None,
        disable_caching=False,
        **kwargs,
    ):
        if cache_dir is None:
            cache_dir = self.sounds_dir

        input_data = {"id": voice_id, "input_text": text}
        cached_result = self.get_cached_result(
            input_data, cache_dir, voice_id=voice_id, **kwargs
        )
        if cached_result is not None:
            return cached_result

        audio_path = (
            self.get_audio_basename(**kwargs) + ".mp3" if path is None else path
        )
        kwargs["lang"] = kwargs.get("lang", self.lang)
        kwargs["tld"] = kwargs.get("tld", self.tld)
        try:
            tts = gTTS(text, **kwargs)
        except gTTSError as e:
            logger.error(e)
            raise Exception(
                "Failed to initialize gTTS. "
                f"Are you sure the arguments are correct? lang = {kwargs['lang']} and tld = {kwargs['tld']}. "
                "See the documentation for more information."
            )

        try:
            tts.save(str(Path(cache_dir) / audio_path))
        except gTTSError as e:
            logger.error(e)
            raise Exception(
                "gTTS gave an error. You are either not connected to the internet, or there is a problem with the Google Translate API."
            )

        json_dict = {"input_data": input_data, "original_audio": audio_path}

        return json_dict
