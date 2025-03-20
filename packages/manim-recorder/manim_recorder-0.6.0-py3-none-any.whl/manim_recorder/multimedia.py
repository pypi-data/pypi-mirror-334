"""
multimedia for manim-recorder
"""

import uuid
import platform
import os
import wave
import time
import datetime
from pathlib import Path
from tempfile import NamedTemporaryFile
import srt
import sox
import numpy as np
from pydub.utils import mediainfo
from mutagen.mp3 import MP3, HeaderNotFoundError
from pydub import AudioSegment
from pydub.silence import detect_nonsilent
from manim import logger, Scene, config
from manim.scene.scene_file_writer import convert_audio
from manim_recorder.helper import get_audio_basename


def adjust_speed(input_path: str, output_path: str, tempo: float) -> None:
    """ """
    same_destination = False
    if input_path == output_path:
        same_destination = True
        path_, ext = os.path.splitext(input_path)
        output_path = path_ + str(uuid.uuid1()) + ext

    tfm = sox.Transformer()
    tfm.tempo(tempo)
    tfm.build(input_filepath=input_path, output_filepath=output_path)
    if same_destination:
        os.rename(output_path, input_path)


def get_duration(path: str) -> float:
    """ """
    # Create a Path object
    file_path = Path(path)

    # Use match-case to check the file extension
    match file_path.suffix.lower():
        case ".mp3":
            try:
                audio = MP3(path)
                return audio.info.length
            except HeaderNotFoundError:
                logger.info(f"Recover File : {path}")
                audio = AudioSegment.from_file(path, format="mp3")
                os.remove(path)
                audio.export(path, format="mp3")
                return get_duration(path)
        case ".m4a":
            audio = mediainfo(path)
            return float(audio["duration"])
        case ".wav":
            with wave.open(str(path), "rb") as wav_file:
                return wav_file.getnframes() / wav_file.getframerate()
        case _:
            return False


def chunks(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def wav2mp3(wav_path, mp3_path=None, remove_wav=True, bitrate="312k"):
    """Convert wav file to mp3 file"""

    if mp3_path is None:
        mp3_path = Path(wav_path).with_suffix(".mp3")

    # Convert to mp3
    AudioSegment.from_wav(wav_path).export(mp3_path, format="mp3", bitrate=bitrate)

    if remove_wav:
        # Remove the .wav file
        os.remove(wav_path)
    logger.info(f"Saved {mp3_path}")
    return


def remove_silence(audio_segment, silence_thresh_db=-14, min_silence_len=1000):
    """
    Remove silence from an AudioSegment.

    Parameters:
    - audio_segment: AudioSegment, the audio segment to process.
    - silence_thresh_db: int, the threshold (in dBFS) below which audio is considered silent.
    - min_silence_len: int, minimum length of silence (in milliseconds) to be considered as silence.

    Returns:
    - A new AudioSegment instance with silence removed.
    """
    # Detect non-silent chunks
    nonsilent_ranges = detect_nonsilent(
        audio_segment,
        min_silence_len=min_silence_len,
        silence_thresh=audio_segment.dBFS + silence_thresh_db,
    )

    # Create a new audio segment with non-silent parts
    non_silent_audio = AudioSegment.silent(
        duration=0
    )  # Start with an empty audio segment

    for start, end in nonsilent_ranges:
        non_silent_audio += audio_segment[start:end]  # Append non-silent chunks

    return non_silent_audio


def detect_leading_silence(sound, silence_threshold=-20.0, chunk_size=10):
    """
    Detect the length of leading silence in an AudioSegment.

    Parameters:
    - sound: AudioSegment, the audio segment to analyze.
    - silence_threshold: float, the threshold in dB below which audio is considered silent.
    - chunk_size: int, the size of the chunks to analyze in milliseconds.

    Returns:
    - int: The length of leading silence in milliseconds.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0 to avoid infinite loop.")

    trim_ms = 0  # ms
    while (
        trim_ms < len(sound)
        and sound[trim_ms : trim_ms + chunk_size].dBFS < silence_threshold
    ):
        trim_ms += chunk_size

    return trim_ms


def trim_silence(
    sound: AudioSegment,
    silence_threshold=-40.0,
    chunk_size=5,
    buffer_start=200,
    buffer_end=200,
) -> AudioSegment:
    """
    Trim leading and trailing silence from an AudioSegment.

    Parameters:
    - sound: AudioSegment, the audio segment to trim.
    - silence_threshold: float, the threshold in dB below which audio is considered silent.
    - chunk_size: int, the size of the chunks to analyze in milliseconds.
    - buffer_start: int, milliseconds to keep at the start after trimming.
    - buffer_end: int, milliseconds to keep at the end after trimming.

    Returns:
    - AudioSegment: A new AudioSegment with silence trimmed.
    """
    if buffer_start < 0 or buffer_end < 0:
        raise ValueError("Buffer values must be non-negative.")

    start_trim = detect_leading_silence(sound, silence_threshold, chunk_size)
    end_trim = detect_leading_silence(sound.reverse(), silence_threshold, chunk_size)

    # Adjust for buffer
    start_trim = max(0, start_trim - buffer_start)
    end_trim = max(0, end_trim - buffer_end)

    # Ensure we don't exceed the audio length
    duration = len(sound)
    trimmed_sound = sound[start_trim : duration - end_trim]

    return trimmed_sound


def normalize(audio_data: np.ndarray) -> np.ndarray:
    max_amplitude = np.max(np.abs(audio_data))
    if max_amplitude > 0:
        return audio_data / max_amplitude
    return audio_data


def compress(
    audio_data: np.ndarray, threshold: float = 0.1, ratio: float = 4.0
) -> np.ndarray:
    compressed_data = np.where(
        np.abs(audio_data) > threshold,
        np.sign(audio_data) * (threshold + (np.abs(audio_data) - threshold) / ratio),
        audio_data,
    )
    return compressed_data


def get_file_path(scene: Scene, suffix):
    return scene.renderer.file_writer.movie_file_path.with_suffix(suffix)


class SoundSegment:
    def __init__(self, gain: int | None = None):
        self.audio_segment = None

    def init_audio(self):
        if self.audio_segment is None:
            self.audio_segment = AudioSegment.silent()

    def is_init_audio(self):
        return isinstance(self.audio_segment, AudioSegment)

    def append_audio_file(
        self,
        audio_file: str,
        time: float | None = None,
        gain: float | None = None,
        **kwargs,
    ):
        if Path(audio_file).suffix not in (".wav", ".raw"):
            with NamedTemporaryFile(suffix=".wav", delete=False) as wav_file_path:
                convert_audio(file_path, wav_file_path, "pcm_s16le")
                new_segment = AudioSegment.from_file(wav_file_path.name)
                logger.info(f"Automatically converted {file_path} to .wav")
            Path(wav_file_path.name).unlink()
        else:
            new_segment = AudioSegment.from_file(audio_file)
        if gain:
            new_segment = new_segment.apply_gain(gain)

        self.append_audio_segment(new_segment, time, **kwargs)

    def append_audio_segment(
        self,
        new_segment: AudioSegment,
        time: float | None = None,
        gain_to_background: float | None = None,
    ):
        """Creates an empty, silent, Audio Segment."""
        segment = self.audio_segment
        curr_end = segment.duration_seconds
        if time is None:
            time = curr_end

        if time < 0:
            raise ValueError("Adding sound at timestamp < 0")

        new_end = time + new_segment.duration_seconds
        diff = new_end - curr_end
        if diff > 0:
            segment = segment.append(
                AudioSegment.silent(int(np.ceil(diff * 1000))),
                crossfade=0,
            )
        self.audio_segment = segment.overlay(
            new_segment,
            position=int(1000 * time),
            gain_during_overlay=gain_to_background,
        )

    def automatic_detect_audio_src(self, audio_src, **kwargs):
        if isinstance(audio_src, AudioSegment):
            self.append_audio_segment(audio_src, **kwargs)
        else:
            self.append_audio_file(audio_src, **kwargs)

    def finish(self, scene: Scene, suffix: str = ".sfx", extension: str = "wav"):
        if config.format in ["gif", "png"] or self.audio_segment is None:
            return
        if len(self.audio_segment) == 0:
            return
        sound_effect_file_path = get_file_path(scene, f"{suffix}.{extension}")

        self.append_audio_segment(AudioSegment.silent(0))
        self.audio_segment.export(sound_effect_file_path, format=extension)
        logger.info(f"Voiceover File ready at %s", sound_effect_file_path)


class Transcript:
    def __init__(self):
        self.transcripts = []

    def append(self, text: str):
        if text:
            self.transcripts.append(text)
        else:
            self.transcripts.append("\n")

    def caption(self):
        if len(self.transcripts) == 0:
            return

        start = datetime.timedelta(seconds=5)
        end = 0
        sub_caption = []
        for text in self.transcripts:
            audio_duration = self.text2duration(text)
            if audio_duration <= 0:
                logger.warning(
                    "Audio duration for %s is non-positive : %s",
                    audio_file,
                    audio_duration,
                )
                continue
            end = start + datetime.timedelta(seconds=audio_duration)
            sub_caption.append(
                srt.Subtitle(
                    index=len(sub_caption),
                    start=start,
                    end=end,
                    content=text,
                )
            )
            start = end + datetime.timedelta(seconds=10)

        return srt.compose(sub_caption)

    def text2duration(self, text: str):
        if text:
            return (self.words_count(text) / 155) * 60
        else:
            return 1.0

    def words_count(self, text: str):
        return len(text.split())

    def finish(self, scene: Scene, create_subcaption: bool):
        if config.format in ["gif", "png"] or not len(self.transcripts):
            return
        transcript_file = get_file_path(scene, ".md")
        if transcript_file:
            with open(transcript_file, "w") as tsx:
                tsx.write(" ".join(self.transcripts))
                logger.info("Transcript file has been written as %s", transcript_file)
            if create_subcaption:
                transcript_file = transcript_file.with_suffix(".vo.srt")
                caption_str = self.caption()
                if caption_str:
                    with open(transcript_file, "w") as caption_f:
                        caption_f.write(caption_str)
                        logger.info(
                            "Voiceover Subcaption file has been written as %s",
                            transcript_file,
                        )
