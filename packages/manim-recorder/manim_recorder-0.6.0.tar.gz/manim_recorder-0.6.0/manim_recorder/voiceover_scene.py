"""
SoundScene Module

This module defines the SoundScene class, which extends the Scene class from the Manim library.
It provides functionality to add sound and voiceovers to scenes, along with managing subcaptions.
"""

import re
import os

from typing import override
from pathlib import Path
from math import ceil
from contextlib import contextmanager
from typing import Optional, Generator
from pydub import AudioSegment
from manim import Scene, config, Mobject, logger, Animation, Add
from manim.utils.exceptions import RerunSceneException, EndSceneEarlyException
from manim.utils.file_ops import open_media_file
from manim_recorder.service import AudioService
from manim_recorder.tracker import SoundTracker
from manim_recorder.sound_effects import SoundEffects
from manim_recorder.multimedia import chunks
from manim_recorder.helper import text_and_mobject
from manim.utils import caching


class SoundScene(Scene):
    """A scene class that can be used to add sound to a scene."""

    audio_service: AudioService
    sound_effects: SoundEffects
    current_tracker: Optional[SoundTracker]
    create_subcaption: bool
    voice_id: int = -1
    skip_sound_recording: bool
    sfx_debug: bool
    transcript: bool

    def set_audio_service(
        self,
        audio_service: AudioService,
        create_subcaption: Optional[bool] = True,
        cache_dir_delete: bool = False,
        skip: bool = False,
        debug: bool = False,
        transcript: bool | None = None,
        cache_file_save: bool = True,
        cache_file: Path = None,
        sfx_gain: int = None,
    ) -> None:
        """Sets the Audio service to be used for the sound. This method
        should be called before adding any sound to the scene.

        Args:
            audio_service (AudioService): The audio service to be used.
            create_subcaption (Optional[bool], optional): Whether to create subcaptions for the scene. Defaults to True.
            cache_dir_delete (bool, optional): Whether to delete the cache directory. Defaults to False.
            skip (bool, optional): Whether to skip audio processing. Defaults to False.
            transcript (bool, optional) : Write only Transcript is False and Write Transcript and based Caption is True. Defaults to None
        """
        self.audio_service = audio_service
        self.audio_service.set_sounds_dir(cache_file, self, cache_dir_delete)
        self.current_tracker = None
        if config.save_last_frame:
            self.create_subcaption = False
        else:
            self.create_subcaption = create_subcaption
        self.skip_sound_recording = skip
        self.sound_effects = SoundEffects(
            self,
            debug=debug,
            cache_dir=(cache_file if cache_file else self.audio_service.sounds_dir),
        )
        self.transcript = transcript

    def add_voiceover_text(
        self,
        text: Optional[str] = None,
        mobject: Optional[Mobject] = None,
        sound_file: str | Path = None,
        subcaption: Optional[str] = None,
        max_subcaption_len: int = 70,
        subcaption_buff: float = 0.1,
        gain=None,
        gain_to_background: Optional[float] = None,
        **kwargs,
    ) -> SoundTracker:
        """Generates and adds voiceover audio to the scene.

        Args:
            text (str): The text to be spoken.
            subcaption (Optional[str]): Alternative subcaption text. Defaults to None.
            max_subcaption_len (int): Max characters for subcaption. Defaults to 70.
            subcaption_buff (float): Duration between subcaption chunks in seconds. Defaults to 0.1.
            gain_to_background (Optional[float]): Gain adjustment for background sound. Defaults to None.
            **kwargs: Additional arguments for audio segment customization.

        Returns:
            SoundTracker: Tracker for the generated sound.

        Raises:
            Exception: If audio service is not initialized.
        """
        if not hasattr(self, "audio_service"):
            raise Exception("You need to call init_sound() before adding a sound.")

        if self.skip_sound_recording and sound_file is None:
            if text is not None:
                self.add_subcaption(text)
                if isinstance(self.transcript, bool):
                    self.audio_service.transcript_append(text)
            return SoundTracker(
                scene=self,
                sound_file=sound_file,
                data={"input_data": {"id": self.voice_id, "input_text": text}},
                audio_cache_dir=self.audio_service.sounds_dir,
                voice_id=self.voice_id,
            )

        dict_ = {
            "input_data": {"id": self.voice_id, "input_text": text},
            "original_audio": sound_file,
            "final_audio": sound_file,
        }

        if isinstance(sound_file, AudioSegment):
            dict_ = {
                "input_data": {"id": self.voice_id, "input_text": text},
                "original_audio": None,
                "final_audio": None,
            }

        if sound_file is None:
            dict_ = self.audio_service._wrap_generate_from_text(
                text=text,
                mobject=mobject,
                voice_id=self.voice_id,
                animations_hashes=self.renderer.animations_hashes,
                num_plays=self.renderer.num_plays,
                disable_caching=config.disable_caching,
                **kwargs,
            )
            sound_file = str(
                Path(self.audio_service.sounds_dir)
                / dict_.get("final_audio", "dummy.wav")
            )

        tracker = SoundTracker(
            scene=self,
            data=dict_,
            sound_file=sound_file,
            voice_id=self.voice_id,
            animations_hashes=self.renderer.animations_hashes,
            num_plays=self.renderer.num_plays,
            disable_caching=config.disable_caching,
        )

        sound_exist = False
        if isinstance(sound_file, AudioSegment):
            self.renderer.skip_animations = self.renderer._original_skipping_status
            if gain:
                sound_file = sound_file.apply_gain(gain)
            self.renderer.file_writer.add_audio_segment(
                sound_file,
                time=self.renderer.time + 0,
                gain_to_background=gain_to_background,
            )
            sound_exist = True
        elif os.path.exists(sound_file):
            self.renderer.skip_animations = self.renderer._original_skipping_status
            self.renderer.file_writer.add_sound(
                sound_file,
                time=self.renderer.time + 0,
                gain=gain,
                gain_to_background=gain_to_background,
            )
            sound_exist = True

        if sound_exist:
            self.current_tracker = tracker
            if self.create_subcaption:
                if subcaption is None and text:
                    # Remove placeholders
                    subcaption = re.sub(r"<[^<>]+/>", "", text)
                if subcaption:
                    self.add_wrapped_subcaption(
                        subcaption,
                        tracker.duration,
                        subcaption_buff=subcaption_buff,
                        max_subcaption_len=max_subcaption_len,
                    )
                    if isinstance(self.transcript, bool):
                        self.audio_service.transcript_append(text)

        return tracker

    def add_wrapped_subcaption(
        self,
        subcaption: str,
        duration: float,
        subcaption_buff: float = 0.1,
        max_subcaption_len: int = 70,
    ) -> None:
        """Adds a subcaption to the scene. If the subcaption is longer than `max_subcaption_len`, it is split into chunks that are smaller than `max_subcaption_len`.

        Args:
            subcaption (str): The subcaption text.
            duration (float): The duration of the subcaption in seconds.
            max_subcaption_len (int, optional): Maximum number of characters for a subcaption. Defaults to 70.
            subcaption_buff (float, optional): The duration between split subcaption chunks in seconds. Defaults to 0.1.
        """
        subcaption = " ".join(subcaption.split())
        n_chunk = ceil(len(subcaption) / max_subcaption_len)
        tokens = subcaption.split(" ")
        chunk_len = ceil(len(tokens) / n_chunk)
        chunks_ = list(chunks(tokens, chunk_len))
        try:
            assert len(chunks_) == n_chunk or len(chunks_) == n_chunk - 1
        except AssertionError:
            import ipdb

            ipdb.set_trace()

        subcaptions = [" ".join(i) for i in chunks_]
        subcaption_weights = [
            len(subcaption) / len("".join(subcaptions)) for subcaption in subcaptions
        ]

        current_offset = 0
        for idx, subcaption in enumerate(subcaptions):
            chunk_duration = duration * subcaption_weights[idx]
            self.add_subcaption(
                subcaption,
                duration=max(chunk_duration - subcaption_buff, 0),
                offset=current_offset,
            )
            current_offset += chunk_duration

    def wait_voiceover(self, subcaption, mobject: Optional[Mobject] = None, **kwargs):
        """Plays the voiceover and waits for it to finish.

        Args:
            text (Optional[str], optional): The text to be spoken. Defaults to None.
            mobject (Optional[Mobject], optional): The Mobject to be spoken. Defaults to None.
            **kwargs: Additional keyword arguments for the voiceover method.
        """
        with self.voiceover(
            text=subcaption, mobject=mobject, subcaption=subcaption, **kwargs
        ) as tracker:
            self.safe_wait(tracker.duration)

    def add_sfx(
        self,
        *animes: Animation | Mobject,
        sound_effect_name: str | None = None,
        sound_effect_index: int = 0,
        sound_effect_run_time_index: int = 0,
        sound_add_position: str | None = None,
        run_time: float = 1.0,
        repeat: bool = True,
        gain: int = -10,
        gain_to_background: float | None = None,
        **kwargs,
    ):
        """
        Add sound effects to animations or objects.

        Args:
            *args: Animation or Mobject to which the sound effect will be added.
            sound_effect_name (str, optional): Name of the sound effect.
            sound_position (str, optional): Position of the sound effect.
            sound_index (int, optional): Index for the sound effect.
            gain (float, optional): Gain of the audio segment.
            gain_to_background (float, optional): Gain of the segment from the background.
            **kwargs: Additional parameters for sound effect configuration.
        """
        self.sound_effects.add_sound_effect(
            *animes,
            sound_effect_name=sound_effect_name,
            sound_effect_index=sound_effect_index,
            sound_effect_run_time=sound_effect_run_time_index,
            sound_effect_position=sound_add_position,
            repeat=repeat,
            run_time=run_time,
            gain=gain,
            gain_to_background=gain_to_background,
            **kwargs,
        )

    def play_voiceover(
        self,
        *animes: Animation | Mobject,
        subcaption=None,
        sound_position="over",
        **kwargs,
    ):
        r"""Plays animations with an accompanying voiceover and optional subcaption.

        This method allows for the simultaneous playback of animations and a voiceover,
        with the option to display a subcaption at specified times during the animation.

        Parameters
        ----------
        args : Animation | Mobject
            The animations to be played. Mobjects can be added using ``Add`` animations.
        subcaption : str
            The text to be displayed as a subcaption during the animation.
        mobject : Optional[Mobject], optional
            An optional Mobject to associate with the voiceover.
        sound_position : str, optional
            The position of the voiceover relative to the animations:
            "before" (start), "over" (during), "after" (end), or "add" (additive).
        sound_file : str, optional
            The path to a sound file to be played during the animation.
        gain_to_background : Optional[float], optional
            A gain adjustment for the background sound during the voiceover.
        **kwargs :
            Additional keyword arguments passed to the renderer.
        """

        match sound_position:
            case "before":
                if all([isinstance(obj, Mobject) for obj in animes]):
                    self.play(Add(*animes, run_time=0.5))
                else:
                    self.play(*animes)
                self.wait_voiceover(
                    subcaption=subcaption,
                    **kwargs,
                )
            case "after":
                self.wait_voiceover(
                    subcaption=subcaption,
                    **kwargs,
                )
                if all([isinstance(obj, Mobject) for obj in animes]):
                    self.play(Add(*animes, run_time=0.5))
                else:
                    self.play(*animes)
            case _ if all([isinstance(obj, Mobject) for obj in animes]):
                self.play_voiceover(
                    Add(*animes, run_time=1.0),
                    subcaption=subcaption,
                    sound_position="after",
                    **kwargs,
                )
            case _:
                with self.voiceover(
                    text=subcaption,
                    **kwargs,
                ) as tracker:
                    self.play(*animes, run_time=tracker.duration)

    def wait_for_voiceover(self) -> None:
        """Waits for the current voiceover to finish playing."""
        if not hasattr(self, "current_tracker"):
            return
        if self.current_tracker is None:
            return

        self.safe_wait(self.current_tracker.get_remaining_duration())

    def safe_wait(self, duration: float) -> None:
        """Waits for a given duration. If the duration is less than one frame, it waits for one frame.

        Args:
            duration (float): The duration to wait for in seconds.
        """
        if duration > 1 / config["frame_rate"]:
            self.wait(duration)

    @contextmanager
    def voiceover(
        self,
        text: Optional[str] = None,
        mobject: Optional[Mobject] = None,
        sound_file: str | Path = None,
        **kwargs,
    ) -> Generator[SoundTracker, None, None]:
        """The main function to be used for adding sound to a scene.

        Args:
            text (Optional[str], optional): The text to be spoken. Defaults to None.
            mobject (Optional[Mobject], optional): The Mobject to be spoken. Defaults to None.

        Yields:
            Generator[SoundTracker, None, None]: The sound tracker object.
        """
        if all(sound_src is None for sound_src in (text, mobject, sound_file)):
            raise ValueError(
                "Please specify either a sound text string and mobject path."
            )
        else:
            text, mobject = text_and_mobject(text, mobject)

        try:
            # Increment voice_id after adding a new sound
            self.voice_id += 1

            yield self.add_voiceover_text(
                text=text, mobject=mobject, sound_file=sound_file, **kwargs
            )
        finally:
            self.wait_for_voiceover()

    def font_setup(self):
        pass

    def color_setup(self):
        pass

    def scene_setup(self):
        pass

    @override
    def render(self, preview: bool = False) -> None:
        """Renders this Scene.

        Args:
            preview (bool, optional): If true, opens scene in a file viewer. Defaults to False.
        """
        self.font_setup()
        self.color_setup()
        self.setup()
        self.scene_setup()
        try:
            self.construct()
        except EndSceneEarlyException:
            pass
        except RerunSceneException as e:
            self.remove(*self.mobjects)
            self.renderer.clear_screen()
            self.renderer.num_plays = 0
            return True
        self.tear_down()
        # We have to reset these settings in case of multiple renders.
        self.renderer.scene_finished(self)
        self.sound_effects.finished(self)
        self.audio_service.finish(self, self.transcript)
            
        # Show info only if animations are rendered or to get image
        if (
            self.renderer.num_plays
            or config["format"] == "png"
            or config["save_last_frame"]
        ):
            logger.info(
                f"Rendered {str(self)}\nPlayed {self.renderer.num_plays} animations",
            )

        # If preview open up the render after rendering.
        if preview:
            config["preview"] = True

        if config["preview"] or config["show_in_file_browser"]:
            open_media_file(self.renderer.file_writer)

        if hasattr(self, "audio_service"):
            if hasattr(self.audio_service, "app_exec"):
                self.audio_service.app_exec()
