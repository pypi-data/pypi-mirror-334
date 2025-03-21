# Auto-generated test for tensor2metric

import pytest
from fileformats.generic import File, Directory, FsObject  # noqa
from fileformats.medimage import Nifti1  # noqa
from fileformats.medimage_mrtrix3 import ImageFormat, ImageIn, Tracks  # noqa
from pydra.tasks.mrtrix3.v3_0 import Tensor2Metric


def test_tensor2metric(tmp_path, cli_parse_only):

    task = Tensor2Metric(
        debug=False,
        dkt=None,
        force=False,
        mask=None,
        mk_dirs=None,
        modulate=None,
        num=None,
        rk_ndirs=None,
        tensor=Nifti1.sample(),
        ad=None,
        adc=None,
        ak=None,
        cl=None,
        cp=None,
        cs=None,
        fa=None,
        mk=None,
        rd=None,
        rk=None,
        value=None,
        vector=None,
    )
    result = task(plugin="serial")
    assert not result.errored
