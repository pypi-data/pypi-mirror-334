import sys
import os
import time
import wave
import pyaudio
import threading
from manim import logger
from manim_recorder.helper import get_audio_basename


class PyAudio_:
    """
    A class to record and play audio using PyAudio.
    """

    def __init__(
        self,
        format: int = pyaudio.paInt16,
        channels: int = 1 if sys.platform == "darwin" else 2,
        rate: int = 44100,
        chunk: int = 1024,
        device_index: int = None,
        file_path: str = get_audio_basename() + ".wav",
        **kwargs,
    ):
        """Initialize the audio recorder."""
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.device_index = device_index
        self.file_path = file_path

        self.lock = threading.Lock()
        self.p = pyaudio.PyAudio()

        self.frames = []
        self.is_recording = False
        self.is_paused = False
        self.playback_thread = None
        self.stop_playback_event = threading.Event()
        self.is_playing = False
        self.current_playback_frame_index = 0
        self.playback_paused = False
        self.playback_lock = threading.Lock()

    def __str__(self) -> str:
        """Return the file path if it exists."""
        if isinstance(self.file_path, str):
            if os.path.exists(self.file_path):
                return self.file_path
        return "No valid file path set."

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, key):
        return self.frames[key]

    def __setitem__(self, key, value):
        self.frames[key] = value

    def __iter__(self):
        return iter(self.frames)

    def __float__(self):
        """Return the total recording duration in seconds."""
        return len(self) * self.chunk / self.rate if len(self) else 0.0

    def __bool__(self):
        return True if len(self) else False

    def append(self, value):
        self.frames.append(value)

    def set_device_index(self, device_index) -> None:
        """Set the input device index for recording."""
        try:
            self.p.get_device_info_by_host_api_device_index(0, device_index)
            self.device_index = device_index
            return True
        except Exception as e:

            logger.error("Invalid device index. Please try again. {}".format(e))
            return False

    def set_channels(self, channels: int = None) -> None:
        """Set the number of audio channels."""
        if channels is None:
            channels = self.device_index
        try:
            self.channels = self.p.get_device_info_by_host_api_device_index(
                0, channels
            ).get("maxInputChannels")
            return True
        except Exception as e:
            logger.error("Invalid device index. Please try again. {}".format(e))
            return False

    def get_device_count(self) -> int:
        """Return the number of audio input devices."""
        return self.p.get_host_api_info_by_index(0).get("deviceCount")

    def get_devices_name(self) -> list:
        """Return a list of available audio input device names."""
        return [
            self.p.get_device_info_by_host_api_device_index(0, i).get("name")
            for i in range(self.get_device_count())
            if self.p.get_device_info_by_host_api_device_index(0, i).get(
                "maxInputChannels"
            )
            > 0
        ]

    def start_recording(self) -> None:
        """Start recording audio."""
        self.recording_frames = []
        self.is_recording = True
        self.is_paused = False
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self) -> None:
        """Internal method to handle audio recording."""
        try:
            stream = self.p.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk,
                input_device_index=self.device_index,
            )

            while self.is_recording:
                if not self.is_paused:
                    data = stream.read(self.chunk)
                    with self.lock:
                        self.append(data)

        except Exception as e:
            logger.error("An error occurred during recording: {}".format(e))
        finally:
            stream.stop_stream()
            stream.close()

    def pause_recording(self) -> None:
        """Pause the recording."""
        self.is_paused = True

    def resume_recording(self) -> None:
        """Resume the recording."""
        self.is_paused = False

    def stop_recording(self) -> None:
        """Stop the recording."""
        self.is_recording = False
        self.thread.join()

    def save_recording(self) -> None:
        """Save the recorded audio to a file."""
        with wave.open(self.file_path, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            # wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.rate)
            wf.writeframes(b"".join(self))

    def play_playback(self) -> None:
        """Start playback of the recorded audio."""
        if not len(self):
            return False
        self.is_playing = True
        self.stop_playback_event.clear()  # Clear the stop event

        self.playback_thread = threading.Thread(target=self._playback)
        self.playback_thread.start()

    def _playback(self) -> None:
        """Internal method to handle audio playback."""
        stream = self.p.open(
            format=self.format, channels=self.channels, rate=self.rate, output=True
        )
        self.current_playback_frame_index = 0  # Initialize current playback frame
        while (
            self.current_playback_frame_index < len(self)
            and not self.stop_playback_event.is_set()
        ):
            with self.playback_lock:
                if self.playback_paused:
                    time.sleep(0.1)
                    continue
                stream.write(self[self.current_playback_frame_index])
                self.current_playback_frame_index += (
                    1  # Increment the current playback frame
                )

        stream.stop_stream()
        stream.close()

    def pause_playback(self) -> None:
        """Pause the playback."""
        self.playback_paused = True

    def resume_playback(self) -> None:
        """Resume the playback."""
        self.playback_paused = False

    def stop_playback(self) -> None:
        """Stop the playback."""
        self.is_playing = False
        self.stop_playback_event.set()  # Signal to stop playback
        if self.playback_thread is not None:
            self.playback_thread.join()  # Wait for the playback thread to finish

    def close(self) -> None:
        """Terminate the PyAudio session."""
        self.p.terminate()

    def get_recording_format_duration(self) -> str:
        """Return the recording duration formatted as HH:MM:SS."""
        struct_time = time.gmtime(float(self))
        return time.strftime("%H:%M:%S", struct_time)

    def set_filepath(self, path: str) -> None:
        """Set the file path for saving the recording."""
        self.file_path = str(path)
