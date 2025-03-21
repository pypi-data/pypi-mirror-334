# Auto-generated test for fixelcrop

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FixelCrop


@pytest.mark.xfail(reason="Task fixelcrop is known not pass yet")
def test_fixelcrop(tmp_path, cli_parse_only):

    task = FixelCrop(
        debug=False,
        force=False,
        input_fixel_directory=File.sample(),
        input_fixel_mask=Nifti1.sample(),
        output_fixel_directory=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
