"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import math
import typing as h

import numpy as nmpy
from obj_mpp.type.marked_point.model.mark import (
    mark_h,
    mark_interval_h,
    mark_precision_h,
)

array_t = nmpy.ndarray
number_sampler_t = nmpy.random.Generator


@d.dataclass(slots=True, repr=False, eq=False)
class mark_sampler_t:
    Samples: h.Callable[[int], array_t] = d.field(init=False)
    SimilarSamples: h.Callable[[mark_h, float, int], array_t] = d.field(init=False)
    #
    _IntegerSamples: h.Callable[..., int | array_t] | None = None
    _RealSamples: h.Callable[..., float | array_t] | None = None

    @classmethod
    def New(
        cls,
        interval: mark_interval_h,
        precision: mark_precision_h,
        stripe: type[mark_h],
        sampler: number_sampler_t,
        /,
    ) -> h.Self:
        """"""
        output = cls()
        output._IntegerSamples = sampler.integers
        output._RealSamples = sampler.uniform

        first, last = interval

        if precision is None:
            if stripe is int:
                Samples = lambda _arg: output._IntegerSamples(
                    first, high=last + 1, size=_arg
                )
            else:
                Samples = lambda _arg: output._RealSamples(
                    low=first, high=last, size=_arg
                )
        else:
            if stripe is int:
                maximum = (last - first) // precision
            else:
                maximum = int((last - first) / precision)
            Samples = (
                lambda _arg: precision
                * output._IntegerSamples(0, high=maximum + 1, size=_arg)
                + first
            )

        SimilarSamples = lambda _ref, _frt, _nbr: output._SimilarSamples(
            _ref, stripe, interval, _frt, _nbr
        )

        output.Samples = Samples
        output.SimilarSamples = SimilarSamples

        return output

    def _SimilarSamples(
        self,
        reference: mark_h,
        stripe: type[mark_h],
        interval: mark_interval_h,
        fraction: float,
        n_samples: int,
        /,
    ) -> array_t:
        """
        Note that the (optional) precision is ignored.
        """
        first = max(reference * (1.0 - fraction), interval[0])
        last = min(reference * (1.0 + fraction), interval[1])

        if stripe is int:
            return self._IntegerSamples(
                math.floor(first), high=math.ceil(last) + 1, size=n_samples
            )
        else:
            if last < interval[1]:
                last = math.nextafter(last, last + 1.0)
            return self._RealSamples(low=first, high=last, size=n_samples)


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
