# Auto-generated test for warpinvert

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import WarpInvert


@pytest.mark.xfail(reason="Task warpinvert is known not pass yet")
def test_warpinvert(tmp_path, cli_parse_only):

    task = WarpInvert(
        debug=False,
        displacement=False,
        force=False,
        in_=Nifti1.sample(),
        template=None,
        out=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
