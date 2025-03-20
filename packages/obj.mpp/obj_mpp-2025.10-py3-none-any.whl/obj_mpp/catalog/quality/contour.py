"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h
from enum import Enum as enum_t

import numpy as nmpy
from obj_mpp.type.marked_point.instance.base import instance_t
from obj_mpp.type.quality.base import quality_context_t as _base_t


class measure_e(enum_t):
    MEAN = 1
    STDDEV = 2
    VARIANCE = 3
    MEDIAN = 4
    MIN = 5
    MAX = 6


@d.dataclass(slots=True, repr=False, eq=False)
class contour_t(_base_t):

    q_defaults = {"measure": measure_e.MEAN}

    def SetKwargs(self, q_kwargs: dict[str, h.Any], _: dict[str, h.Any], /) -> None:
        """"""
        if (measure := q_kwargs.get("measure")) is None:
            q_kwargs["measure"] = self.q_defaults["measure"]
        elif isinstance(measure, str):
            # For example, "mean".
            q_kwargs["measure"] = measure_e(measure.upper())

        self.q_kwargs = q_kwargs

    def Quality(self, instance: instance_t, /) -> float:
        """"""
        domain = instance.bbox.domain
        contour = instance.Contour()

        # Cannot be empty (see Contour).
        signal = self.signal[domain][contour]
        measure = self.q_kwargs["measure"]

        if measure == measure_e.MEAN:
            return signal.mean().item()
        elif measure == measure_e.STDDEV:
            return signal.std().item()
        elif measure == measure_e.VARIANCE:
            return signal.var().item()
        elif measure == measure_e.MEDIAN:
            return signal.median().item()
        elif measure == measure_e.MIN:
            return nmpy.min(signal).item()
        else:  # measure == measure_e.MAX:
            return nmpy.max(signal).item()


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
