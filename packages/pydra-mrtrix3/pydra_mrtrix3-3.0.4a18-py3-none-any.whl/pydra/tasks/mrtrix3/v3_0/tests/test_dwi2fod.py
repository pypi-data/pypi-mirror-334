# Auto-generated test for dwi2fod

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Fod


def test_dwi2fod(tmp_path, cli_parse_only):

    task = Dwi2Fod(
        algorithm="csd",
        debug=False,
        directions=None,
        dwi=Nifti1.sample(),
        filter=None,
        force=False,
        fslgrad=None,
        grad=None,
        lmax=None,
        mask=None,
        neg_lambda=None,
        niter=None,
        norm_lambda=None,
        response_odf=[File.sample()],
        shells=None,
        strides=None,
        threshold=None,
        predicted_signal=None,
    )
    result = task(plugin="serial")
    assert not result.errored
