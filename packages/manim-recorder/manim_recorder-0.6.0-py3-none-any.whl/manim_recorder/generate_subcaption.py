import srt
import json
import pathlib
import os
import pprint
import datetime
from manim import logger
from manim_recorder.multimedia import get_duration


class Generate_Subcaption:
    def __init__(self, file, cache=False, **kwargs):
        self.jsons_file = file
        self.jsons_dirname = os.path.dirname(file)
        self.jsons_basename = os.path.basename(file)
        self.cache_only = cache
        if cache:
            self.jsons_basename = os.path.basename(self.jsons_dirname)
        self.Transcript = []

    def caption(self):
        audio_dicts = self.jsons_lst(self.jsons_file)
        if self.cache_only:
            audio_dicts = self.cache_json(self.jsons_file)
        start = datetime.timedelta(seconds=10)
        end = 0
        sub_caption = []
        manifest = []
        transcript = []
        paragraph = ""
        section = None
        for audio_dict in audio_dicts:
            audio_file = audio_dict["file"]
            if os.path.exists(audio_file):
                audio_duration = get_duration(audio_file)
                if audio_duration <= 0:
                    logger.warning(
                        "Audio duration for %s is non-positive : %s",
                        audio_file,
                        audio_duration,
                    )
                    continue  # Skip this audio file
                paragraph = (
                    f"{paragraph} {audio_dict["caption"]}"
                    if paragraph
                    else f"{audio_dict["caption"]}"
                )
                if section != audio_dict.get("section"):
                    section = audio_dict.get("section")
                    print(section)
                    transcript.append(paragraph)
                    paragraph = ""
                manifest.append(
                    {
                        "index": len(sub_caption),
                        "file": audio_file,
                        "section": audio_dict.get("section"),
                        "text": audio_dict["caption"],
                    }
                )
                end = start + datetime.timedelta(seconds=audio_duration)
                sub_caption.append(
                    srt.Subtitle(
                        index=len(sub_caption),
                        start=start,
                        end=end,
                        content=audio_dict["caption"],
                    )
                )
                logger.info(
                    "Added subtitle: %s | Start: %s | End: %s",
                    audio_dict["caption"],
                    start,
                    end,
                )
                start = end + datetime.timedelta(seconds=10)
            else:
                logger.warning("Audio file does not exist: %s", audio_file)
        transcript.append(paragraph)
        self.Transcript = transcript
        return (srt.compose(sub_caption), manifest)

    def cache_json(self, cache_js, section_number=None):
        cache_js = pathlib.Path(cache_js).absolute()
        audio_dicts = []
        with open(cache_js) as j:
            k = json.load(j)
            i_dirname = os.path.dirname(cache_js)
            if len(k) > 0:
                for k_audio in k:
                    file_name = k_audio["final_audio"]
                    audio_dict = {
                        "caption": k_audio["input_data"]["input_text"],
                        "file": os.path.join(i_dirname, file_name),
                    }
                    if section_number:
                        audio_dict.update(
                            {
                                "section": f"Section {section_number}",
                            }
                        )
                    audio_dicts.append(audio_dict)
        return audio_dicts

    def jsons_lst(self, jsons_file):
        audio_dicts = []
        with open(jsons_file) as f:
            section_number = 0
            for i in f.readlines():
                i = i.strip()
                if os.path.isfile(i):
                    audio_dict = self.cache_json(i, section_number=section_number + 1)
                    audio_dicts.extend(audio_dict)
                section_number += 1
        return audio_dicts

    def subtitle_write(self, file_name=None, transcript=False):
        name, _ = os.path.splitext(self.jsons_file)
        subcaption_file = os.path.join(self.jsons_dirname, f"{name}.srt")
        caption_str, manifest = self.caption()

        with open(subcaption_file, "w") as f:
            f.write(caption_str)

        with open("manifest.json", "w") as json_file:
            json.dump(manifest, json_file, ensure_ascii=False, indent=4)
        if len(self.Transcript) and transcript:
            with open("Transcript.txt", "w") as transcript:
                transcript.write("\n".join(self.Transcript))

        logger.info("Save file : %s", subcaption_file)



    
