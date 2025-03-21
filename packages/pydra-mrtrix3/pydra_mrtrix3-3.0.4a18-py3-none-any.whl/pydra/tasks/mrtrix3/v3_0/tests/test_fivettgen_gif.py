# Auto-generated test for fivettgen_gif

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import FivettGen_Gif


@pytest.mark.xfail(reason="Task fivettgen_gif is known not pass yet")
def test_fivettgen_gif(tmp_path, cli_parse_only):

    task = FivettGen_Gif(
        cont=None,
        debug=False,
        force=False,
        in_file=Nifti1.sample(),
        nocleanup=False,
        nocrop=False,
        scratch=None,
        sgm_amyg_hipp=False,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
