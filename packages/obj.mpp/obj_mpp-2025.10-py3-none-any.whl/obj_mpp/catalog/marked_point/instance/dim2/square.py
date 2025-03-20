"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import numpy as nmpy
from obj_mpp.catalog.marked_point.instance.dim2.rectangle import (
    CoarseBoundingBoxHalfLengths,
    Normals,
    Region,
)
from obj_mpp.interface.console.marked_point import FormattedAngle
from obj_mpp.type.marked_point.instance.base2 import instance_t as _base_t
from obj_mpp.type.marked_point.model.mark import mark_h

array_t = nmpy.ndarray

_HALF_SIDE, _ANGLE = range(2)


class square_t(_base_t):

    @property
    def educated_marks(self) -> tuple[mark_h, ...]:
        """"""
        return (
            self.marks[_HALF_SIDE],
            self.marks[_ANGLE],
            self.marks[_ANGLE] * 180.0 / nmpy.pi,
        )

    def _CoarseBoundingBoxHalfLengths(self) -> tuple[int, ...]:
        """"""
        return CoarseBoundingBoxHalfLengths(
            self.marks[_HALF_SIDE], 1.0, self.marks[_ANGLE]
        )

    def _Region(self) -> array_t:
        """"""
        return Region(
            self.marks[_HALF_SIDE],
            1.0,
            self.marks[_ANGLE],
            self.point,
            self.bbox.domain,
        )

    def Normals(self) -> tuple[tuple[array_t, ...] | None, array_t | None]:
        """"""
        cache_entry = self.Normals.__name__

        if cache_entry not in self._cache:
            self._cache[cache_entry] = Normals(
                1.0,
                self.marks[_ANGLE],
                self.point,
                self.bbox.min_s,
                self.crosses_border,
                self.Contour(),
            )

        return self._cache[cache_entry]

    def _RadiusForSimilarPoints(self, /, *, fraction: float = 0.1) -> float:
        """"""
        return 0.5 * fraction * self.marks[_HALF_SIDE] * (1.0 + 1.0)

    def FormattedMarks(self) -> str:
        """"""
        return f"[red]{self.marks[_HALF_SIDE]:.2f}[/]" + FormattedAngle(
            self.marks[_ANGLE]
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
