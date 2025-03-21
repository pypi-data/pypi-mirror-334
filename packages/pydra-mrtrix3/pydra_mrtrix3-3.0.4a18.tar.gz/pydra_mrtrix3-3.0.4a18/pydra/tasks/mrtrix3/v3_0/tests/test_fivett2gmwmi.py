# Auto-generated test for fivett2gmwmi

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Fivett2Gmwmi


def test_fivett2gmwmi(tmp_path, cli_parse_only):

    task = Fivett2Gmwmi(
        debug=False,
        force=False,
        in_5tt=Nifti1.sample(),
        mask_in=None,
        mask_out=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
