"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import math
import typing as h

from logger_36 import L
from obj_mpp.type.marked_point.model.mark import (
    mark_definition_t,
    mark_h,
    mark_interval_h,
    mark_precision_h,
)


@d.dataclass(slots=True, repr=False, eq=False)
class model_t(dict[str, mark_definition_t]):

    dimension: int = d.field(init=False)

    @property
    def mark_types(self) -> dict[str, type[mark_h]]:
        """"""
        return {_nme: _vle.type for _nme, _vle in self.items()}

    def AreMarkRangesValid(self, ranges: dict[str, h.Any], /) -> bool:
        """"""
        valid_names = tuple(self.keys())
        issues = []
        for name, value in ranges.items():
            if name not in valid_names:
                issues.append(
                    (
                        "Invalid mark range",
                        {
                            "actual": name,
                            "expected": valid_names,
                            "expected_is_choices": True,
                        },
                    )
                )
                continue

            definition = self[name]

            if definition.type is int:
                valid_types = int
            elif definition.type is float:
                valid_types = (int, float)
            else:
                valid_types = definition.type
            if (
                (not isinstance(value, tuple))
                or ((value.__len__() != 2) and (value.__len__() != 3))
                or (not all(isinstance(_elm, valid_types) for _elm in value))
            ):
                issues.append(
                    (
                        f'Invalid range for mark "{name}"',
                        {
                            "actual": value,
                            "expected": "2- or 3-tuple of integers/floats",
                        },
                    )
                )
                continue

            if definition.type not in (int, float):
                continue

            if (value.__len__() == 3) and (value[2] < 0):
                issues.append(
                    (
                        "Invalid precision",
                        {
                            "actual": value[2],
                            "expected": "Value positive or equal to zero",
                        },
                    )
                )

            if value[0] > value[1]:
                issues.append(f"From_{value[0]} !>! to_{value[1]} for mark '{name}'")
                continue

            if value[0] < definition.min:
                issues.append(
                    f"Range start out-of-bound ({value[0]} < {definition.min}; "
                    f"expected: >=) for mark '{name}'"
                )
            elif (
                (definition.type is int)
                and (value[0] == definition.min)
                and not definition.min_inclusive
            ):
                issues.append(
                    f"Range start out-of-bound ({value[0]} <= {definition.min}; "
                    f"expected: >) for mark '{name}'"
                )

            if value[1] > definition.max:
                issues.append(
                    f"Range end out-of-bound ({value[1]} > {definition.min}; "
                    f"expected: <=) for mark '{name}'"
                )
            elif (
                (definition.type is int)
                and (value[1] == definition.max)
                and not definition.max_inclusive
            ):
                issues.append(
                    f"Range end out-of-bound ({value[1]} >= {definition.min}; "
                    f"expected: <) for mark '{name}'"
                )

        for issue in issues:
            if isinstance(issue, str):
                L.StageIssue(issue)
            else:
                L.StageIssue(issue[0], **(issue[1]))

        return issues.__len__() == 0

    def NormalizedMarkRanges(
        self,
        ranges: dict[str, mark_interval_h | tuple[mark_h, mark_h, mark_precision_h]],
        /,
    ) -> dict[str, tuple[mark_interval_h, mark_precision_h]]:
        """"""
        output = {}

        for name, value in self.items():
            if (actual := ranges.get(name)) is None:
                interval = value.default_interval
                precision = value.default_precision
                if interval is None:
                    L.StageIssue(f"{name}: Missing required range.")
                    continue
                else:
                    first, last = interval
            else:
                first, last, *precision = actual
                if precision.__len__() > 0:
                    precision = precision[0]
                else:
                    precision = value.default_precision

            first_original = first
            last_original = last
            stripe = value.type

            if precision is not None:
                if precision == 0:
                    precision = None
                else:
                    if stripe is int:
                        precision = int(precision)
                    else:
                        precision = float(precision)
                    first = precision * math.ceil(first / precision)
                    last = precision * math.floor(last / precision)
                    if last < first:
                        precision = None
                        L.StageIssue(
                            f"{name}: Invalid interval/precision combination "
                            f"leading to empty range."
                        )

            if stripe is float:
                # Adaptation of interval to numpy.uniform generating samples in [a,b[.
                if (first == first_original) and not value.min_inclusive:
                    first = math.nextafter(first, first + 1.0)
                if (last < last_original) or value.max_inclusive:
                    last = math.nextafter(last, last + 1.0)

            output[name] = ((first, last), precision)

        return output

    def DescriptionHeader(
        self, /, *, educated_version: bool = False
    ) -> tuple[str, ...]:
        """"""
        if educated_version:
            marks = self.EducatedMarksHeader() + ("Area",)
        else:
            marks = self.MarksHeader()

        return "Type", *self.PointHeader(), *marks, "Quality", "Age"

    @staticmethod
    def PointHeader() -> tuple[str, ...]:
        """"""
        raise NotImplementedError

    @staticmethod
    def MarksHeader() -> tuple[str, ...]:
        """"""
        raise NotImplementedError

    @staticmethod
    def EducatedMarksHeader() -> tuple[str, ...]:
        """"""
        raise NotImplementedError


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
