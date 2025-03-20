# Manim Recorder

## Installation

### Blank Audio
```bash
pip install "manim-recorder[blank]"
```
### Audio Recording
```bash
pip install "manim-recorder[gui_recorder]"
```

### GTTs
```bash
pip install "manim-recorder[gTTS]"
```

### All
```bash
pip install manim-recorder
```

## GUI (Using PySide6)

![GUI Recorder 1](https://github.com/avnlearn/manim-recorder/blob/main/assets/GUI%20recording_001-0.2.5.png?raw=true)

![GUI Recorder 1](https://github.com/avnlearn/manim-recorder/blob/main/assets/GUI%20recording_002-0.2.5.png?raw=true)

![GUI Recorder 1](https://github.com/avnlearn/manim-recorder/blob/main/assets/GUI%20recording_003-0.2.5.png?raw=true)

```python
from manim import *
# from manim_recorder import VoiceoverScene
from manim_recorder.voiceover_scene import SoundScene
# from manim_recorder.services.recorder import RecorderService
from manim_recorder.recorder.gui import RecorderService


class VoiceRecorder(SoundScene):
    def construct(self):
        self.set_audio_service(
            RecorderService()
        )

        circle = Circle()
        square = Square().shift(2 * RIGHT)

        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT),
                      run_time=tracker.duration)

        with self.voiceover(text="Thank you for watching.") as tracker:
            self.play(Uncreate(circle))

        self.wait()

```

## CLI (Pynput)

```python
from manim import *
# from manim_recorder import VoiceoverScene
from manim_recorder.voiceover_scene import SoundScene
# from manim_recorder.services.recorder import RecorderService
from manim_recorder.recorder.pynput import RecorderService
from pathlib import Path


class VoiceRecorder(SoundScene):
    def construct(self):
        self.set_audio_service(
            RecorderService(
                device_index=0,
                # cache_dir=Path(
                #     config.media_dir + "/voiceovers/" + self.__class__.__name__.lower()
                # ),
            )
        )

        circle = Circle()
        square = Square().shift(2 * RIGHT)
        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT),
                      run_time=tracker.duration)

        with self.voiceover(text="Thank you for watching.") as tracker:
            self.play(Uncreate(circle))

        self.wait()
```

## Termux Cli

```python
from manim import *
from manim_recorder.voiceover_scene import SoundScene
from manim_recorder.recorder.termux import RecorderService
from pathlib import Path


class Recordering(SoundScene):
    def construct(self):
        self.set_speech_service(
            RecorderService(
            )
        )

        circle = Circle()
        square = Square().shift(2 * RIGHT)
        with self.voiceover(text="This circle is drawn as I speak.") as tracker:
            self.play(Create(circle), run_time=tracker.duration)

        # with self.voiceover("This circle is drawn as I speak.") as tracker:
        #     self.safe_wait(tracker.duration)

        with self.voiceover(text="Let's shift it to the left 2 units.") as tracker:
            self.play(circle.animate.shift(2 * LEFT),
                      run_time=tracker.duration)

        with self.voiceover(text="Thank you for watching."):
            self.play(Uncreate(circle))

        self.wait()
```

## Blank Voice

```python
import pprint, json
from manim import *
import pathlib
from manim_recorder.voiceover_scene import SoundScene
from manim_recorder.service.blank import BlankService


class Example_Without_Wait(SoundScene):
    def construct(self):
        self.set_audio_service(BlankService())
        config.disable_caching = True
        circle = Circle()
        square = Square().shift(2 * RIGHT)
        self.play_voiceover(circle, subcaption="Create Circle")
        self.wait_voiceover("move to circle")
        self.play(circle.animate.shift(2 * RIGHT))
        self.play_voiceover(
            circle.animate.shift(2 * LEFT),
            subcaption="two unit",
        )
        self.play_voiceover(Uncreate(circle), subcaption="Thank you!")
```
