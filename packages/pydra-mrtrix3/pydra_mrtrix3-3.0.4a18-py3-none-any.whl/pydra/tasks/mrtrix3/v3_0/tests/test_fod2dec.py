# Auto-generated test for fod2dec

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Fod2Dec


def test_fod2dec(tmp_path, cli_parse_only):

    task = Fod2Dec(
        contrast=None,
        debug=False,
        force=False,
        in_file=Nifti1.sample(),
        lum=False,
        lum_coefs=None,
        lum_gamma=None,
        mask=None,
        no_weight=False,
        threshold=None,
        out_file=File.sample(),
    )
    result = task(plugin="serial")
    assert not result.errored
