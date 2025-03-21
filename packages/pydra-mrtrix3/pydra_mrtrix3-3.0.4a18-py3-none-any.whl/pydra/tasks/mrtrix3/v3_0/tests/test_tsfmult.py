# Auto-generated test for tsfmult

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import TsfMult


@pytest.mark.xfail(reason="Task tsfmult is known not pass yet")
def test_tsfmult(tmp_path, cli_parse_only):

    task = TsfMult(
        debug=False,
        force=False,
        input1=File.sample(),
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
