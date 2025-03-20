import os
from pydub import AudioSegment
from manim import Scene, Animation, Mobject
from manim_recorder.multimedia import get_duration


class SoundTracker:
    """Tracks the progress of a sound in a scene."""

    def __init__(self, scene: Scene, data: dict, sound_file: str, **kwargs):
        """Initializes the SoundTracker.

        Args:
            scene (Scene): The scene to which the sound belongs.
            data (dict): Contains sound data, including the audio file name.
            audio_cache_dir (str): Directory where audio files are cached.
        """
        self.scene = scene
        self.data = data
        self.sound_file = sound_file
        self.__dict__.update(kwargs)
        
        self.duration = (
            self._get_audio_duration(self.sound_file) if self.sound_file else 1
        )
        

        last_t = scene.renderer.time or 0
        self.start_t = last_t
        self.end_t = last_t + self.duration

    def _get_audio_duration(self, audio_file) -> float:
        """Retrieves the audio duration or returns 1.0 if not found."""
        
        if isinstance(audio_file, AudioSegment):
            return len(audio_file)/1000.0
        elif os.path.exists(audio_file):
            return get_duration(audio_file)
        return 1

    def get_remaining_duration(self, buff: float = 0.0) -> float:
        """Returns the remaining duration of the sound, adjusted by an optional buffer."""
        current_time = self.scene.renderer.time or 0
        return max(self.end_t - current_time + buff, 0)

