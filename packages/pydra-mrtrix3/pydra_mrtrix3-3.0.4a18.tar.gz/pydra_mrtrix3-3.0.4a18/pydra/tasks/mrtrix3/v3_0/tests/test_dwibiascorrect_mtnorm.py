# Auto-generated test for dwibiascorrect_mtnorm

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiBiascorrect_Mtnorm


@pytest.mark.xfail(reason="Task dwibiascorrect_mtnorm is known not pass yet")
def test_dwibiascorrect_mtnorm(tmp_path, cli_parse_only):

    task = DwiBiascorrect_Mtnorm(
        cont=None,
        debug=False,
        force=False,
        fslgrad=None,
        grad=None,
        in_file=Nifti1.sample(),
        lmax=None,
        mask=None,
        nocleanup=False,
        scratch=None,
        bias=None,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
