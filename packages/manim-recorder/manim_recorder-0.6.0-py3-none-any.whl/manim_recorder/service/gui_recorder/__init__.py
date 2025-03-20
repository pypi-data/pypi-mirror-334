from pathlib import Path
import sys
from manim_recorder.service import AudioService
from manim_recorder.service.gui_recorder.__main__ import Recorder, QApplication, sys
from manim_recorder.helper import get_audio_basename, logger
from PySide6.QtCore import Signal, QObject, QEventLoop


class Communicate(QObject):
    recorder_data = Signal(
        str, str, int, object
    )  # Ensure this matches the emitted signal
    accept = Signal(str)


class RecorderService(AudioService):
    """Speech service that records from a microphone during rendering."""

    def __init__(
        self,
        global_speed: float = 1.00,
        cache_dir: Path = None,
        text_check: bool = None,
        sound_recording_skip: bool = False,
        **kwargs,
    ):
        """Initialize the Audio service.
        Args:
        """
        AudioService.__init__(
            self,
            global_speed=global_speed,
            cache_dir=cache_dir,
            text_check=text_check,
            sound_recording_skip=sound_recording_skip,
        )
        self.app = QApplication(sys.argv)
        self.communicator = Communicate()
        self.communicator.accept.connect(self.recorder_complated)
        self.recorder = Recorder(communicator=self.communicator, **kwargs)
        # self.recorder.show()
        self.loop = QEventLoop()

    def generate_from_text(
        self,
        text: str,
        cache_dir: str = None,
        path: str = None,
        voice_id: int = None,
        mobject: str | None = None,
        sound_recording_skip: bool = False,
        num_plays: int = 0,
        **kwargs,
    ) -> dict:

        if cache_dir is None:
            cache_dir = self.sounds_dir

        input_data = {"id": voice_id, "input_text": text}
        cached_result = self.get_cached_result(
            input_data, cache_dir, voice_id=voice_id, **kwargs
        )

        if cached_result is not None:
            return cached_result

        if not self.recorder.isVisible():
            self.recorder.show()

        audio_path = (
            self.get_audio_basename(**kwargs) + ".wav" if path is None else path
        )

        self.communicator.recorder_data.emit(
            str(Path(cache_dir) / audio_path), text, voice_id, mobject
        )

        self.loop = QEventLoop()
        self.communicator.accept.connect(self.loop.quit)
        self.loop.exec()

        json_dict = {"input_data": input_data, "original_audio": audio_path}

        return json_dict

    def recorder_complated(self, message):
        logger.info(f"Save Audio File : {message}")

    def app_exec(self):
        self.recorder.close()
        self.loop.exit()
        sys.exit(self.app.exec)
        QApplication.exit()
