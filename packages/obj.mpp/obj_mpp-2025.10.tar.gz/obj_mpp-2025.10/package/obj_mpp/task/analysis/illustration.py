"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

import numpy as nmpy
from logger_36 import L
from obj_mpp.constant.signal import MAX_UINT16
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.type.marked_point.instance.base import instance_t

array_t = nmpy.ndarray


def ContourMapOfDetection(instances: h.Sequence[instance_t], /) -> array_t:
    """"""
    output = nmpy.zeros(SIGNAL_CONTEXT.lengths, dtype=nmpy.uint16, order="C")

    if (n_instances := instances.__len__()) > MAX_UINT16:
        _PlotExclamationPoints(output)
        L.Log(
            "Number of marked points too high for storage as UInt16",
            actual=n_instances,
            expected=f"<={MAX_UINT16}",
        )
        return output

    for label, instance in enumerate(instances):
        output[instance.bbox.domain][instance.Contour()] = MAX_UINT16 - label

    return output


def RegionMapOfDetection(instances: h.Sequence[instance_t], /) -> array_t:
    """"""
    output = nmpy.zeros(SIGNAL_CONTEXT.lengths, dtype=nmpy.uint16, order="C")

    if (n_instances := instances.__len__()) > MAX_UINT16:
        _PlotExclamationPoints(output)
        L.Log(
            "Number of marked points too high for storage as UInt16",
            actual=n_instances,
            expected=f"<={MAX_UINT16}",
        )
        return output

    distance_map = nmpy.zeros_like(output, dtype=nmpy.float64, order="C")
    for label, instance in enumerate(instances, start=1):
        local_dmp = distance_map[instance.bbox.domain]  # dmp=distance map
        instance_dmp = instance.InnerDistanceMap()
        without_intersection = instance_dmp > local_dmp

        local_dmp[without_intersection] = instance_dmp[without_intersection]
        output[instance.bbox.domain][without_intersection] = label

    return output


def _PlotExclamationPoints(array: array_t, /) -> None:
    """"""
    value = nmpy.iinfo(array.dtype).max

    half_width = array.shape[1] // 2
    half_half_width = half_width // 2
    half_bar_width = max(array.shape[1] // 20, 1)
    separation = max((2 * half_bar_width) // 4, 1)

    for col in (half_half_width, half_width, half_width + half_half_width):
        col_slice = slice(col - half_bar_width, col + half_bar_width)
        array[1 : (-2 * half_bar_width - separation - 1), col_slice] = value
        array[(-2 * half_bar_width - 1) : -1, col_slice] = value


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
