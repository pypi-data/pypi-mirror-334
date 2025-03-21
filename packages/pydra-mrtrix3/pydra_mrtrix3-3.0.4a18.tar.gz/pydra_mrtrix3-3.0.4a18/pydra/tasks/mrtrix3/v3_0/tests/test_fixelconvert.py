# Auto-generated test for fixelconvert

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FixelConvert


@pytest.mark.xfail(reason="Task fixelconvert is known not pass yet")
def test_fixelconvert(tmp_path, cli_parse_only):

    task = FixelConvert(
        debug=False,
        fixel_in=File.sample(),
        fixel_out=File.sample(),
        force=False,
        in_size=None,
        name=None,
        nii=False,
        out_size=False,
        template=None,
        value=None,
    )
    result = task(plugin="serial")
    assert not result.errored
