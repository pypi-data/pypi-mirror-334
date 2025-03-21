# Auto-generated test for warpinit

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import WarpInit


def test_warpinit(tmp_path, cli_parse_only):

    task = WarpInit(
        debug=False,
        force=False,
        template=Nifti1.sample(),
        warp=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
