# Auto-generated test for dwi2tensor

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Tensor


def test_dwi2tensor(tmp_path, cli_parse_only):

    task = Dwi2Tensor(
        constrain=False,
        debug=False,
        directions=None,
        dwi=Nifti1.sample(),
        force=False,
        fslgrad=None,
        grad=None,
        iter=None,
        mask=None,
        ols=False,
        b0=None,
        dkt=None,
        dt=File.sample(),
        predicted_signal=None,
    )
    result = task(plugin="serial")
    assert not result.errored
