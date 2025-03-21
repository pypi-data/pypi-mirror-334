# Auto-generated test for dwinormalise_mtnorm

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiNormalise_Mtnorm


@pytest.mark.xfail(reason="Task dwinormalise_mtnorm is known not pass yet")
def test_dwinormalise_mtnorm(tmp_path, cli_parse_only):

    task = DwiNormalise_Mtnorm(
        cont=None,
        debug=False,
        force=False,
        fslgrad=None,
        grad=None,
        in_file=Nifti1.sample(),
        lmax=None,
        mask=None,
        nocleanup=False,
        reference=None,
        scratch=None,
        out_file=File.sample(),
        scale=None,
    )
    result = task(plugin="serial")
    assert not result.errored
