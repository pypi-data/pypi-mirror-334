# Auto-generated test for fixel2tsf

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Fixel2Tsf


def test_fixel2tsf(tmp_path, cli_parse_only):

    task = Fixel2Tsf(
        angle=None,
        debug=False,
        fixel_in=Nifti1.sample(),
        force=False,
        tracks=Tracks.sample(),
        tsf=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
