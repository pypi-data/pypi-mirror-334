# Auto-generated test for dwinormalise_manual

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import DwiNormalise_Manual


@pytest.mark.xfail(reason="Task dwinormalise_manual is known not pass yet")
def test_dwinormalise_manual(tmp_path, cli_parse_only):

    task = DwiNormalise_Manual(
        cont=None,
        debug=False,
        force=False,
        fslgrad=None,
        grad=None,
        input_dwi=Nifti1.sample(),
        input_mask=Nifti1.sample(),
        intensity=None,
        nocleanup=False,
        percentile=None,
        scratch=None,
        output_dwi=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
