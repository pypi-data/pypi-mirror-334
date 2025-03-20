from pathlib import Path
import os
import json, random
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
from manim import *
from manim.scene.scene_file_writer import convert_audio
from manim_recorder.helper import get_audio_basename
from manim_recorder.multimedia import SoundSegment

LIB_SOUND_EFFECTS_DIR = f"{os.path.dirname(__file__)}/sound"


class SoundEffects:
    """Tracks the progress of a sound in a scene."""

    def __init__(
        self,
        scene: Scene,
        cache_dir: Path = None,
        debug: bool = False,
        sound_effect_save: bool = False,
        gain: int = -10,
    ):
        """
        Initializes a sound effect object for a given scene.

        Parameters:
            scene (Scene): The scene in which the sound effect will be used.
            cache_dir (str | None): The directory for caching sound effects (default is "sfx").
        """
        self.scene = scene
        self.sfx_cache_file = cache_dir
        self.gain = gain
        self.sound_effect_save = sound_effect_save
        self.debug = debug
        self.audio_segment = SoundSegment(gain=gain)

    def add_sound_effect(
        self,
        *animes: Animation,
        sound_effect_name: str | None = None,
        sound_effect_index: int = 0,
        sound_effect_run_time: int = 0,
        sound_effect_position: str | None = None,
        repeat: bool = True,
        run_time: float = 1.0,
        gain: int = -10,
        gain_to_background: float | None = None,
        **kwargs,
    ):
        if sound_effect_name is None:
            for anime in animes:
                anime_name = type(anime).__name__
                match anime:
                    case Mobject():
                        anime = Add(anime, run_time=1.0)
                        anime_name = "Add"
                    case _ as x if anime_name == "_AnimationBuilder":
                        anime_name = "_AnimationBuilder"

                sound_effect_file = self.get_sound_effect_file(
                    name=anime_name,
                    index=sound_effect_index,
                    run_time=sound_effect_run_time,
                    repeat=repeat,
                )
                if sound_effect_file is None:
                    self.scene.play(anime, **kwargs)
                    continue

                self.play_animation_sound_effect(
                    anime,
                    sound_file=sound_effect_file,
                    sound_position=sound_effect_position,
                    run_time=run_time,
                    gain=gain,
                    gain_to_background=gain_to_background,
                    **kwargs,
                )
            return True
        sound_effect_file = self.get_sound_effect_file(
            name=sound_effect_name,
            index=sound_effect_index,
            run_time=sound_effect_run_time,
            repeat=repeat,
        )
        if sound_effect_file:
            anime_play = None
            if all([isinstance(anime, Mobject) for anime in animes]):
                anime_play = Add(*animes, run_time=run_time)
            elif all([isinstance(anime, Animation) for anime in animes]):
                anime_play = AnimationGroup(*animes)
            else:
                anime_play = []
                for anime in animes:
                    match anime:
                        case Mobject():
                            anime_play.append(Add(anime, run_time=0.5))
                        case _:
                            anime_play.append(anime)
                anime_play = AnimationGroup(*animes)

            if anime_play:
                self.play_animation_sound_effect(
                    anime_play,
                    sound_file=sound_effect_file,
                    sound_position=sound_effect_position,
                    run_time=run_time,
                    gain=gain,
                    gain_to_background=gain_to_background,
                    **kwargs,
                )

    def save_sound_effect_file(self, audio_trim):
        """
        Saves the trimmed audio as a sound effect file in the specified cache directory.

        Parameters:
            audio_trim: The audio segment to be saved as a sound effect.

        Returns:
            str | None: The path to the saved sound effect file if successful, None otherwise.
        """
        try:
            # Ensure the cache directory exists
            sfx_dir = os.path.join(self.sfx_cache_file, "sfx")
            os.makedirs(sfx_dir, exist_ok=True)

            # Generate the base name for the sound effect file
            sfx_file = get_audio_basename("sfx_")
            if config.disable_caching:
                sfx_file = f"sfx_{self.scene.renderer.num_plays}"

            # Define the full path for the sound effect file
            sfx_file_path = os.path.join(sfx_dir, f"{sfx_file}.wav")

            # Remove existing file if it exists
            if os.path.exists(sfx_file_path):
                os.remove(sfx_file_path)

            # Export the trimmed audio to the specified file
            audio_trim.export(sfx_file_path, format="wav")

            # Check if the file was created successfully
            if os.path.exists(sfx_file_path):
                logger.info(f"Sound effect file saved: {sfx_file_path}")
                return sfx_file_path
            else:
                logger.error("Failed to save sound effect file.")
                return None

        except Exception as e:
            logger.error(f"An error occurred while saving the sound effect file: {e}")
            return None

    def sound_effect_trimming(
        self, sound_effect_file, sound_effect_dict, run_time, repeat
    ):
        """
        Trims the sound effect audio file based on specified parameters.

        Parameters:
            sfx_file (str): The path to the sound effect file to be trimmed.
            data (dict): A dictionary containing trimming parameters, which may include:
                - start_time (int): The starting point for trimming in milliseconds.
                - end_time (int): The ending point for trimming in milliseconds.
                - time_limit (int): The maximum duration for the audio in milliseconds.
                - run_time (list): A list of lists specifying trimming durations.
                - repeat (list): A list containing start and end times for repeating the audio.

        Returns:
            str: The path to the saved trimmed audio file, or the original sfx_file if no trimming is performed.
        """
        audio_run_time = run_time
        if audio_run_time is None:
            return sound_effect_file

        audio = AudioSegment.from_file(sound_effect_file)
        trimmed_audio = []
        start_time = sound_effect_dict.get("start_time")
        end_time = sound_effect_dict.get("end_time")
        time_limit = sound_effect_dict.get("time_limt")
        repeat_value = sound_effect_dict.get("repeat") if repeat else []

        audio_len = len(audio)

        run_time = sound_effect_dict.get("run_time")
        if isinstance(repeat_value, list) and audio_run_time > 0:
            if len(repeat_value) == 2:

                start_time = repeat_value[0]
                end_time = repeat_value[1]
                trimmed_audio = audio[start_time:end_time]
                desired_length_ms = audio_run_time * 1000
                num_repeats = desired_length_ms // len(trimmed_audio) + 1

                if num_repeats > 1:
                    long_audio = trimmed_audio * num_repeats
                    trimmed_audio = long_audio[:desired_length_ms]

        if len(trimmed_audio) == 0:
            if isinstance(run_time, list):
                run_time_index = int(audio_run_time - 1)
                if run_time_index < len(run_time):
                    """
                    run_time : [
                        [end_time]
                        [start_time, end_time]
                    ]
                    """

                    trim_silence = run_time[run_time_index]
                    if len(trim_silence) == 1:
                        end_time = trim_silence[0]
                    elif len(trim_silence) > 1:
                        start_time = trim_silence[0]
                        end_time = trim_silence[1]
                elif isinstance(time_limit, int):
                    """
                    "sfx_name": "pen_writing.mp3",
                    "start_time": 657,
                    "run_time": [
                        [end_time],
                        [start_time, end_time]
                    ],
                    "time_limit" : 59040
                    """
                    audio_end_time = audio_run_time * 1000
                    if audio_end_time <= audio_len:
                        end_time = audio_end_time

            if isinstance(start_time, int) and isinstance(end_time, int):
                duration_ = end_time - start_time
                if duration_ < len(audio) and start_time > 0 and end_time > start_time:
                    trimmed_audio = audio[start_time:end_time]
                elif (
                    duration_ < len(audio) and start_time == 0 and end_time > start_time
                ):
                    trimmed_audio = audio[:end_time]
                elif duration_ < len(audio) and end_time == 0 and end_time < start_time:
                    trimmed_audio = audio[start_time:]
            elif isinstance(start_time, int) and end_time is None:
                if start_time < len(audio):
                    trimmed_audio = audio[start_time:]
            elif start_time is None and isinstance(end_time, int):
                if end_time < len(audio):
                    trimmed_audio = audio[:end_time]

        if len(trimmed_audio) == 0:
            return sound_effect_file

        if self.gain:
            trimmed_audio = trimmed_audio.apply_gain(self.gain)

        if self.sound_effect_save:
            return self.save_sound_effect_file(trimmed_audio)
        return trimmed_audio

    def get_sound_effect_json_file(self, name, index, **kwargs):

        if not os.path.exists(f"{LIB_SOUND_EFFECTS_DIR}/{name}.json"):
            return

        with open(f"{LIB_SOUND_EFFECTS_DIR}/{name}.json") as sound_effect_json:
            sound_effect_js = json.load(sound_effect_json)

        try:
            sound_effect_file = self.find_sound_effect_file(
                sound_effect_js[index].get("sfx_name")
            )

            if sound_effect_file:
                if self.debug:
                    logger.warn(
                        "Sound Effect : %s", sound_effect_js[index].get("sfx_name")
                    )
                    logger.warn(
                        "Start : End : %s:%s",
                        sound_effect_js[index].get("start_time"),
                        sound_effect_js[index].get("end_time"),
                    )
                return self.sound_effect_trimming(
                    sound_effect_file, sound_effect_js[index], **kwargs
                )
        except IndexError:
            logger.error(f"Not Found %s", f"{name}_{index}")
            logger.error(
                "%s : Total Sound Effect - %s",
                f"{name}_{index}",
                f"{len(sound_effect_js)}",
            )

    def find_sound_effect_file(self, file_name):
        file_path = f"{LIB_SOUND_EFFECTS_DIR}/sfx/{file_name}"
        if Path(f"{file_path}").exists():
            return Path(f"{file_path}")
        elif Path(f"{file_path}.wav").exists():
            return Path(f"{file_path}.wav")
        elif Path(f"{file_path}.mp3").exists():
            return Path(f"{file_path}.mp3")

    def get_sound_effect_file(self, name, **kwargs):
        sound_effect_file = self.get_sound_effect_json_file(name, **kwargs)
        if sound_effect_file is None:
            sound_effect_file = self.find_sound_effect_file(name)
        if sound_effect_file:
            logger.info(f"SFX : Append {name} sound effect")
        return sound_effect_file

    def add_sound_effect(
        self,
        *animes: Animation,
        sound_effect_name: str | None = None,
        sound_effect_index: int = 0,
        sound_effect_run_time: int = 0,
        sound_effect_position: str | None = None,
        repeat: bool = True,
        run_time: float = 1.0,
        gain: int = -10,
        gain_to_background: float | None = None,
        **kwargs,
    ):
        if sound_effect_name is None:
            for anime in animes:
                anime_name = type(anime).__name__
                match anime:
                    case Mobject():
                        anime = Add(anime, run_time=1.0)
                        anime_name = "Add"
                    case _ as x if anime_name == "_AnimationBuilder":
                        anime_name = "_AnimationBuilder"

                sound_effect_file = self.get_sound_effect_file(
                    name=anime_name,
                    index=sound_effect_index,
                    run_time=sound_effect_run_time,
                    repeat=repeat,
                )
                if sound_effect_file is None:
                    self.scene.play(anime, **kwargs)
                    continue

                self.play_animation_sound_effect(
                    anime,
                    sound_file=sound_effect_file,
                    sound_position=sound_effect_position,
                    run_time=run_time,
                    gain=gain,
                    gain_to_background=gain_to_background,
                    **kwargs,
                )
            return True
        sound_effect_file = self.get_sound_effect_file(
            name=sound_effect_name,
            index=sound_effect_index,
            run_time=sound_effect_run_time,
            repeat=repeat,
        )
        if sound_effect_file:
            anime_play = None
            if all([isinstance(anime, Mobject) for anime in animes]):
                anime_play = Add(*animes, run_time=run_time)
            elif all([isinstance(anime, Animation) for anime in animes]):
                anime_play = AnimationGroup(*animes)
            else:
                anime_play = []
                for anime in animes:
                    match anime:
                        case Mobject():
                            anime_play.append(Add(anime, run_time=0.5))
                        case _:
                            anime_play.append(anime)
                anime_play = AnimationGroup(*animes)

            if anime_play:
                self.play_animation_sound_effect(
                    anime_play,
                    sound_file=sound_effect_file,
                    sound_position=sound_effect_position,
                    run_time=run_time,
                    gain=gain,
                    gain_to_background=gain_to_background,
                    **kwargs,
                )

    def finished(self, scene):
        self.audio_segment.finish(scene=scene, suffix=".sfx", extension="wav")

    def play_animation_sound_effect(self, anime, sound_file, **kwargs):
        if not self.audio_segment.is_init_audio():
            self.audio_segment.init_audio()

        self.audio_segment.automatic_detect_audio_src(
            sound_file, time=self.scene.renderer.time + 0
        )

        self.scene.play_voiceover(
            anime,
            sound_file=sound_file,
            **kwargs,
        )

    @staticmethod
    def search(sfx_name=None, not_exist_file=None):
        # ANSI escape codes for colors
        COLORS_MP3 = ["\033[92m", "\033[94m", "\033[93m"]
        COLORS_WAV = ["\033[91m", "\033[96m", "\033[95m"]
        RESET = "\033[0m"
        if isinstance(sfx_name, str):

            if (Path(LIB_SOUND_EFFECTS_DIR) / f"{sfx_name}.json").exists():
                sfx_file = Path(LIB_SOUND_EFFECTS_DIR) / f"{sfx_name}.json"
                with open(sfx_file) as sfxs_json:
                    sfxs_json = json.load(sfxs_json)
                    if not_exist_file is not True:
                        print(
                            f"{COLORS_MP3[2]}Index\t\t SFX Name\t\t\t\t\t\t\tRun Time{RESET}"
                        )
                    for sfx_json, i in zip(sfxs_json, list(range(len(sfxs_json)))):
                        default_sfx = ""
                        full_path = os.path.join(
                            f"{LIB_SOUND_EFFECTS_DIR}/sfx", sfx_json["sfx_name"]
                        )
                        sfx_name = os.path.splitext(sfx_json["sfx_name"])[0]
                        run_time = sfx_json.get("run_time")
                        if run_time:
                            run_time = len(run_time)
                        if i == 0:
                            default_sfx = f" {COLORS_MP3[1]}(Default){RESET}"
                        if os.path.isfile(full_path) and not_exist_file is None:
                            print(
                                f"{COLORS_MP3[0]}{i}\t\t- {sfx_name}\t\t\t\t\t\t\t{run_time}{RESET}{default_sfx}"
                            )
                        else:
                            print(
                                f"{COLORS_WAV[0]}{i}\t\t- {sfx_name}\t\t\t\t\t\t\t{run_time}{RESET}{default_sfx}"
                            )
            elif (Path(LIB_SOUND_EFFECTS_DIR) / f"sfx/{sfx_name}.mp3").exists():
                COLOR = random.choice(COLORS_MP3)
                print(f"{COLOR}{entry}{RESET}")
            elif (Path(LIB_SOUND_EFFECTS_DIR) / f"sfx/{sfx_name}.wav").exists():
                COLOR = random.choice(COLORS_MP3)
                print(f"{COLOR}{entry}{RESET}")
        else:
            entries = os.listdir(f"{LIB_SOUND_EFFECTS_DIR}/sfx")
            for entry in entries:
                full_path = os.path.join(f"{LIB_SOUND_EFFECTS_DIR}/sfx", entry)
                if os.path.isfile(full_path):
                    if entry.endswith(".mp3"):
                        entry = os.path.splitext(entry)[0]
                        COLOR = random.choice(COLORS_MP3)
                        print(f"{COLOR}{entry}{RESET}")
                    elif entry.endswith(".wav"):
                        entry = os.path.splitext(entry)[0]
                        COLOR = random.choice(COLORS_WAV)
                        print(f"{COLOR}{entry}{RESET}")

    @staticmethod
    def debug_file(not_exist_file=None, full_lst=False):
        # ANSI escape codes for colors
        COLORS_MP3 = ["\033[92m", "\033[94m", "\033[93m"]
        COLORS_WAV = ["\033[91m", "\033[96m", "\033[95m"]
        RESET = "\033[0m"
        entries = os.listdir(f"{LIB_SOUND_EFFECTS_DIR}")
        if not_exist_file is True and full_lst is False:
            print(f"{COLORS_MP3[2]}Index\t\t SFX Name\t\t\t\t\t\t\tRun Time{RESET}")
        for entry in entries:
            full_path = os.path.join(f"{LIB_SOUND_EFFECTS_DIR}/", entry)
            
            if os.path.isfile(full_path) and entry.endswith(".json"):
                entry = os.path.splitext(entry)[0]
                print(f"\n\n== {entry} ===========================")
                print(
                    f"{COLORS_WAV[0]}Sound Effect File JSON :{RESET}{COLORS_WAV[1]}{full_path}{RESET}"
                )
                SoundEffects.search(entry, not_exist_file=not_exist_file)


if __name__ == "__main__":
    SoundEffects.debug_file()
