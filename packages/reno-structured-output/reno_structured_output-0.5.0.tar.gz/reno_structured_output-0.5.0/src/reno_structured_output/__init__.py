from collections import defaultdict
from pathlib import Path

import yaml
from reno.config import Config
from reno.scanner import Scanner


def collect_notes(conf: Config = Config("./")) -> dict:
    with Scanner(conf) as scnr:
        relnotes = scnr.get_notes_by_version()

    reporoot = Path(conf.reporoot)

    relnotes_content: dict = defaultdict(lambda: defaultdict(list))
    for version, version_details in relnotes.items():
        version_files = [x[0] for x in version_details]
        for f in version_files:
            version_file_content = yaml.load(
                (reporoot / f).read_text(), Loader=yaml.FullLoader
            )
            for category, notes in version_file_content.items():
                if isinstance(notes, str):
                    relnotes_content[version][category].append(notes)
                else:
                    relnotes_content[version][category].extend(notes)

    return relnotes_content


import json
