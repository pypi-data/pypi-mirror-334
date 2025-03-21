# Auto-generated test for dwigradcheck

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiGradcheck


@pytest.mark.xfail(reason="Task dwigradcheck is known not pass yet")
def test_dwigradcheck(tmp_path, cli_parse_only):

    task = DwiGradcheck(
        cont=None,
        debug=False,
        force=False,
        fslgrad=None,
        grad=None,
        in_file=Nifti1.sample(),
        mask=None,
        nocleanup=False,
        number=None,
        scratch=None,
        export_grad_fsl=None,
        export_grad_mrtrix=None,
    )
    result = task(plugin="serial")
    assert not result.errored
