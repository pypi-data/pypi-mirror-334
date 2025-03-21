# Auto-generated test for dwishellmath

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiShellmath


@pytest.mark.xfail(reason="Task dwishellmath is known not pass yet")
def test_dwishellmath(tmp_path, cli_parse_only):

    task = DwiShellmath(
        cont=None,
        debug=False,
        force=False,
        fslgrad=None,
        grad=None,
        in_file=Nifti1.sample(),
        nocleanup=False,
        operation="mean",
        scratch=None,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
