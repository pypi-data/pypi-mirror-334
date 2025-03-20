"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

import numpy as nmpy
from obj_mpp.constant.signal import INFINITY_NUMPY_FLOAT
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.type.marked_point.instance.base import instance_t
from obj_mpp.type.quality.base import quality_context_t as _base_t

array_t = nmpy.ndarray


@d.dataclass(slots=True, repr=False, eq=False)
class _gradient_t(_base_t):

    q_defaults = {"high_definition": 0.5, "min_fraction_high": 0.0}

    def SetKwargs(
        self, q_kwargs: dict[str, h.Any], s_kwargs: dict[str, h.Any], /
    ) -> None:
        """"""
        self._SetKwargsWithDefaults(q_kwargs, self.q_defaults, s_kwargs, {})

    def SetSignal(
        self,
        raw_signal: h.Any,
        /,
    ) -> bool:
        """"""
        if raw_signal.ndim != MARKED_POINT_MODEL.dimension:
            return True

        gradient = list(nmpy.gradient(raw_signal))

        sq_gradient_sum = gradient[0] ** 2
        for grad_cmp in gradient[1:]:
            sq_gradient_sum += grad_cmp**2
        norm = nmpy.sqrt(sq_gradient_sum)

        maximum = norm.max()
        if maximum > 0.0:
            for idx in range(gradient.__len__()):
                gradient[idx] /= maximum

        self.signal = gradient
        return False


def _Gradient_DarkOnBright(
    instance: instance_t,
    gradient: tuple[array_t, ...],
    high_definition: float,
    min_fraction_high: float,
    /,
    *,
    _called_from_bod: bool = False,
) -> float:
    """"""
    sites, normals = instance.Normals()
    if sites is None:
        return -INFINITY_NUMPY_FLOAT

    bbox = instance.bbox

    qualities = nmpy.zeros(sites[0].shape, dtype=nmpy.float64)
    for idx in range(gradient.__len__()):
        qualities += normals[:, idx] * gradient[idx][bbox.domain][sites]
    if _called_from_bod:
        qualities *= -1.0

    threshold = high_definition * qualities.max()
    if threshold < 0.0:
        return -INFINITY_NUMPY_FLOAT

    n_high = nmpy.count_nonzero(qualities >= threshold)
    if n_high / qualities.size < min_fraction_high:
        return -INFINITY_NUMPY_FLOAT

    return qualities.mean()


def _Gradient_BrightOnDark(
    instance: instance_t,
    gradient: tuple[array_t, ...],
    high_definition: float,
    min_fraction_high: float,
    /,
) -> float:
    """
    See _Gradient_DarkOnBright for conditions.
    """
    return _Gradient_DarkOnBright(
        instance, gradient, high_definition, min_fraction_high, _called_from_bod=True
    )


class gradient_bright_on_dark_t(_gradient_t):

    def Quality(self, instance: instance_t, /) -> float:
        """"""
        return _Gradient_BrightOnDark(
            instance,
            self.signal,
            self.q_kwargs["high_definition"],
            self.q_kwargs["min_fraction_high"],
        )


class gradient_dark_on_bright_t(_gradient_t):

    def Quality(self, instance: instance_t, /) -> float:
        """"""
        return _Gradient_DarkOnBright(
            instance,
            self.signal,
            self.q_kwargs["high_definition"],
            self.q_kwargs["min_fraction_high"],
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
