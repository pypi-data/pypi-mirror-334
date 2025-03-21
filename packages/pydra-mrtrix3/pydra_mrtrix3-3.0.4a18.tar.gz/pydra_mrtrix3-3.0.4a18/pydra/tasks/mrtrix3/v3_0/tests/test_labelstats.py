# Auto-generated test for labelstats

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import LabelStats


def test_labelstats(tmp_path, cli_parse_only):

    task = LabelStats(
        debug=False,
        force=False,
        in_file=Nifti1.sample(),
        output=None,
        voxelspace=False,
    )
    result = task(plugin="serial")
    assert not result.errored
