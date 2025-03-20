from abc import ABC, abstractmethod

import os
import json
import sys
from pathlib import Path, PosixPath
import datetime
import shutil
from manim import config, logger, Scene
from manim_recorder.defaults import (
    DEFAULT_VOICEOVER_CACHE_DIR,
    DEFAULT_VOICEOVER_CACHE_JSON_FILENAME,
)
from pydub import AudioSegment
from manim_recorder.multimedia import adjust_speed, SoundSegment, Transcript
from manim_recorder.helper import append_to_json_file


class AudioService(ABC):
    """Abstract base class for a speech service."""

    def __init__(
        self,
        global_speed: float = 1.00,
        cache_dir: Path = None,
        text_check: bool = None,
        sound_recording_skip: bool = False,
        scene: Scene = None,
        cache_file_save: bool = True,
        **kwargs,
    ):
        """
        Args:
            global_speed (float, optional): The speed at which to play the audio.
                Defaults to 1.00.
            cache_dir (str, optional): The directory to save the audio
                files to. Defaults to ``voiceovers/``.
        """
        self.global_speed = global_speed
        self.text_check = text_check
        self.sound_recording_skip = sound_recording_skip
        self.transcript = Transcript()
        self.scene = scene
        self.audio_segment = SoundSegment()
        self.sounds_dir = self.set_sounds_dir(cache_dir, scene)

    def set_sounds_dir(self, cache_dir, scene, cache_dir_delete=False):
        if cache_dir is None and scene is None:
            cache_dir = PosixPath(config.media_dir).absolute() / "sounds"
        elif cache_dir is None and scene is not None:
            module_name = scene.renderer.file_writer.partial_movie_directory.parts[-4]
            cache_dir = Path(config.media_dir)
            if module_name != "videos":
                cache_dir = cache_dir / "sounds" / module_name
            else:
                cache_dir = cache_dir / "sounds"
            cache_dir = cache_dir / scene.renderer.file_writer.output_name
        elif os.path.exists(cache_dir) and os.path.isfile(cache_dir):
            shutil.rmtree(cache_dir)
        elif os.path.exists(cache_dir) and os.path.isdir(cache_dir):
            return cache_dir
        if os.path.exists(cache_dir) and cache_dir_delete:
            logger.info("Remove Sound File : %s", cache_dir)
            shutil.rmtree(cache_dir)

        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        self.sounds_dir = cache_dir
        if scene is not None and self.scene is None:
            self.scene = scene
        return cache_dir

    def _wrap_generate_from_text(self, text: str, path=None, **kwargs) -> dict:
        # Replace newlines with lines, reduce multiple consecutive spaces to single

        text = " ".join(text.split())
        dict_ = self.generate_from_text(
            text=text,
            cache_dir=None,
            path=path,
            sound_recording_skip=self.sound_recording_skip,
            **kwargs,
        )

        original_audio = dict_["original_audio"]

        # Audio callback
        self.audio_callback(original_audio, dict_, **kwargs)

        if self.global_speed != 1:
            logger.warn("Adjusted Audio Speed : %s", original_audio)
            split_path = os.path.splitext(original_audio)
            adjusted_path = split_path[0] + "_adjusted" + split_path[1]

            adjust_speed(
                Path(self.sounds_dir) / dict_["original_audio"],
                Path(self.sounds_dir) / adjusted_path,
                self.global_speed,
            )
            dict_["final_audio"] = adjusted_path
        else:
            dict_["final_audio"] = dict_["original_audio"]

        if not self.audio_segment.is_init_audio():
            self.audio_segment.init_audio()

        self.audio_segment.automatic_detect_audio_src(
            Path(self.sounds_dir) / dict_["final_audio"],
            time=self.scene.renderer.time + 0,
        )

        append_to_json_file(
            Path(self.sounds_dir) / DEFAULT_VOICEOVER_CACHE_JSON_FILENAME,
            dict_,
            **kwargs,
        )
        return dict_

    def get_audio_basename(self, **kwargs):
        sound_basename = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        if config.disable_caching:
            sound_basename = kwargs.setdefault("num_plays", sound_basename)
        return f"Voice_{sound_basename}"

    @abstractmethod
    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None
    ) -> dict:
        """Implement this method for each speech service. Refer to `AzureService` for an example.

        Args:
            text (str): The text to synthesize speech from.
            cache_dir (str, optional): The output directory to save the audio file and data to. Defaults to None.
            path (str, optional): The path to save the audio file to. Defaults to None.

        Returns:
            dict: Output data dictionary. TODO: Define the format.
        """
        raise NotImplementedError

    def get_cached_result(self, input_data, cache_dir, voice_id: int = -1, **kwargs):
        json_path = os.path.join(cache_dir, DEFAULT_VOICEOVER_CACHE_JSON_FILENAME)
        if os.path.exists(json_path):
            sounds_data = json.load(open(json_path, "r"))
            for sound_data in sounds_data:
                if sound_data["input_data"] == input_data and self.text_check:
                    return sound_data
                elif sound_data["input_data"]["id"] == voice_id:
                    return sound_data
            else:
                return None

            for entry in json_data:
                if entry["input_data"] == input_data:
                    return entry
        return None

    def audio_callback(self, audio_path: str, data: dict, **kwargs):
        """Callback function for when the audio file is ready.
        Override this method to do something with the audio file, e.g. noise reduction.

        Args:
            audio_path (str): The path to the audio file.
            data (dict): The data dictionary.
        """
        pass

    def transcript_append(self, text: str):
        self.transcript.append(text)

    def finish(self, scene: Scene, create_subcaption: bool):
        if isinstance(create_subcaption, bool):
            self.transcript.finish(scene, create_subcaption)
        self.audio_segment.finish(scene, suffix=".vo", extension="wav")
