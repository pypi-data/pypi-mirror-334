"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import numpy as nmpy
from obj_mpp.runtime.signal import SIGNAL_CONTEXT
from obj_mpp.type.marked_point.model.point import point_h


def FormattedPoint(point: point_h, /) -> str:
    """"""
    lengths = (str(_elm - 1).__len__() + 3 for _elm in SIGNAL_CONTEXT.lengths)
    as_str = ",".join(
        f"{_crd:{_lgt}.2f}" for _crd, _lgt in zip(point, lengths, strict=True)
    )
    return f"+[cyan]({as_str})[/]"


def FormattedAngle(angle: float, /) -> str:
    """"""
    return f"/_[blue]{angle * 180.0 / nmpy.pi:5.1f}[/]"


def FormattedExponent(exponent: float, /) -> str:
    """"""
    return f"^[magenta]{exponent:.2f}[/]"


def FormattedQuality(quality: float | None, /) -> str:
    """"""
    if quality is None:
        as_str = "?"
    else:
        as_str = f"{quality:.3f}"

    return f"=[green]{as_str}[/]"


def FormattedAge(age: int, /) -> str:
    """"""
    return f"@[magenta]{age}[/]"


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
