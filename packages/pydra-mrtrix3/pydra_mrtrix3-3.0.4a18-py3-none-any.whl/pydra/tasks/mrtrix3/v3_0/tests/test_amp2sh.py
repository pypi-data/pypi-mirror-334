# Auto-generated test for amp2sh

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Amp2Sh


def test_amp2sh(tmp_path, cli_parse_only):

    task = Amp2Sh(
        amp=Nifti1.sample(),
        debug=False,
        directions=None,
        force=False,
        fslgrad=None,
        grad=None,
        lmax=None,
        normalise=False,
        rician=None,
        shells=None,
        strides=None,
        SH=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
