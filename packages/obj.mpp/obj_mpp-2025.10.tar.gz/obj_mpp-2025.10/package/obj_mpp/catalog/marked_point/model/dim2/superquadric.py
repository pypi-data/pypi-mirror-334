"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d

from obj_mpp.constant.mark import (
    DEFAULT_POSITIVE_EXPONENT_DEFINITION,
    DEFAULT_RADII_RATIO_LARGER_DEFINITION,
    DEFAULT_RADIUS_DEFINITION,
    DefaultAngleDefinition,
)
from obj_mpp.type.marked_point.model.base2 import model_t as _base_t
from obj_mpp.type.marked_point.model.mark import (
    mark_h,
    mark_interval_h,
    mark_precision_h,
)


@d.dataclass(slots=True, repr=False, eq=False)
class superquadric_t(_base_t):
    """
    minor_exponent: exponent corresponding to the minor axis ("minor" is not in the
    sense of "smallest").
    """

    def __post_init__(self) -> None:
        """"""
        _base_t.__post_init__(self)
        self.clear()
        self.update(
            {
                "semi_minor_axis": DEFAULT_RADIUS_DEFINITION,
                "major_minor_ratio": DEFAULT_RADII_RATIO_LARGER_DEFINITION,
                "minor_exponent": DEFAULT_POSITIVE_EXPONENT_DEFINITION,
                "major_exponent": DEFAULT_POSITIVE_EXPONENT_DEFINITION,
                "angle": DefaultAngleDefinition(1.0),
            }
        )

    def NormalizedMarkRanges(
        self,
        ranges: dict[str, mark_interval_h | tuple[mark_h, mark_h, mark_precision_h]],
        /,
    ) -> dict[str, tuple[mark_interval_h, mark_precision_h]]:
        """"""
        if "exponent" in ranges:
            ranges = ranges.copy()
            ranges["minor_exponent"] = ranges["major_exponent"] = ranges["exponent"]
            del ranges["exponent"]

        return _base_t.NormalizedMarkRanges(self, ranges)

    @staticmethod
    def MarksHeader() -> tuple[str, ...]:
        """"""
        return (
            "Semi Minor Axis",
            "Semi Major Axis",
            "Exp of S.Min.A",
            "Exp of S.Maj.A",
            "Angle (radian)",
        )

    @classmethod
    def EducatedMarksHeader(cls) -> tuple[str, ...]:
        """"""
        return cls.MarksHeader() + ("Angle (degree)",)


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
