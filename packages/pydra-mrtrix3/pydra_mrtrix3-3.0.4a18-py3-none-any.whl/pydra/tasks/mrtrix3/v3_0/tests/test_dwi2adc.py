# Auto-generated test for dwi2adc

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Dwi2Adc


def test_dwi2adc(tmp_path, cli_parse_only):

    task = Dwi2Adc(
        cutoff=None,
        debug=False,
        force=False,
        fslgrad=None,
        grad=None,
        in_file=Nifti1.sample(),
        ivim=False,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
