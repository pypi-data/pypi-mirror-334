"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

import numpy as nmpy
from logger_36 import L
from obj_mpp.constant.signal import INFINITY_NUMPY_FLOAT, INFINITY_NUMPY_INT
from obj_mpp.type.marked_point.instance.base import instance_t
from obj_mpp.type.quality.base import quality_context_t as _base_t

array_t = nmpy.ndarray


@d.dataclass(slots=True, repr=False, eq=False)
class _contrast_t(_base_t):

    q_defaults = {
        "ring_thickness_ext": 1,
        "ring_thickness_int": INFINITY_NUMPY_INT,
        "normalized": False,
    }

    def SetKwargs(self, q_kwargs: dict[str, h.Any], _: dict[str, h.Any], /) -> None:
        """"""
        self._SetKwargsWithDefaults(q_kwargs, self.q_defaults, {}, {})


def _Contrast_BrightOnDark(
    instance: instance_t,
    signal: array_t,
    ring_thickness_ext: int,
    ring_thickness_int: int,
    normalized: bool,
    /,
) -> float:
    """
    The DilatedRegion method must accept positive and negative (if not
    nmpy.isinf(ring_thickness_int)) dilation parameters.
    """
    region = instance.region
    dilated, dilated_bbox_domain = instance.DilatedRegion(ring_thickness_ext)

    sum_region, area_region, sum2_region = _SumsAndArea(
        signal[instance.bbox.domain], region, normalized
    )
    sum_dilated, area_dilated, sum2_dilated = _SumsAndArea(
        signal[dilated_bbox_domain], dilated, normalized
    )
    if area_dilated <= area_region:
        L.error("Dilated area not strictly larger than original area.")
        return -INFINITY_NUMPY_FLOAT

    if ring_thickness_int == INFINITY_NUMPY_INT:
        sum_eroded = area_eroded = sum2_eroded = 0
    else:
        eroded, eroded_bbox_domain = instance.DilatedRegion(-ring_thickness_int)
        sum_eroded, area_eroded, sum2_eroded = _SumsAndArea(
            signal[eroded_bbox_domain], eroded, normalized
        )
        if area_eroded >= area_region:
            L.error("Eroded area not strictly smaller than original area.")
            return -INFINITY_NUMPY_FLOAT

    area_ext = area_dilated - area_region
    area_int = area_region - area_eroded

    average_ext = (sum_dilated - sum_region) / area_ext
    average_int = (sum_region - sum_eroded) / area_int

    if normalized:
        var_ext = ((sum2_dilated - sum2_region) / area_ext) - average_ext**2
        var_int = ((sum2_region - sum2_eroded) / area_int) - average_int**2

        return (average_int - average_ext) / (var_int * var_ext) ** 0.25
    else:
        return average_int - average_ext


def _Contrast_DarkOnBright(
    instance: instance_t,
    signal: array_t,
    ring_thickness_ext: int,
    ring_thickness_int: int,
    normalized: bool,
    /,
) -> float:
    """
    See _Contrast_BrightOnDark for conditions.
    """
    contrast = _Contrast_BrightOnDark(
        instance,
        signal,
        ring_thickness_ext,
        ring_thickness_int,
        normalized,
    )
    if contrast == -INFINITY_NUMPY_FLOAT:
        # To avoid returning +INFINITY_NUMPY_FLOAT by negation below.
        return -INFINITY_NUMPY_FLOAT

    return -contrast


def _SumsAndArea(
    local_signal: array_t, region: array_t, with_sum_of_sq: bool, /
) -> tuple[float, float, float | None]:
    """"""
    values = local_signal[region]

    area_msk = nmpy.count_nonzero(region)
    sum_region = values.sum().item()
    if with_sum_of_sq:
        sum_of_sq = (values**2).sum().item()
    else:
        sum_of_sq = None

    return sum_region, area_msk, sum_of_sq


class contrast_bright_on_dark_t(_contrast_t):

    def Quality(self, instance: instance_t, /) -> float:
        """"""
        return _Contrast_BrightOnDark(
            instance,
            self.signal,
            self.q_kwargs["ring_thickness_ext"],
            self.q_kwargs["ring_thickness_int"],
            self.q_kwargs["normalized"],
        )


class contrast_dark_on_bright_t(_contrast_t):

    def Quality(self, instance: instance_t, /) -> float:
        """"""
        return _Contrast_DarkOnBright(
            instance,
            self.signal,
            self.q_kwargs["ring_thickness_ext"],
            self.q_kwargs["ring_thickness_int"],
            self.q_kwargs["normalized"],
        )


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
