# Auto-generated test for amp2response

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Amp2Response


def test_amp2response(tmp_path, cli_parse_only):

    task = Amp2Response(
        amps=Nifti1.sample(),
        debug=False,
        directions=None,
        force=False,
        isotropic=False,
        lmax=None,
        mask=Nifti1.sample(),
        noconstraint=False,
        shells=None,
        response=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
