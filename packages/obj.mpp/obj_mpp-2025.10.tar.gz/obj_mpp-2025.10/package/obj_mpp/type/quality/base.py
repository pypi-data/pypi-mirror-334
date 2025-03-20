"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

from logger_36 import L
from obj_mpp.runtime.model import MARKED_POINT_MODEL
from obj_mpp.type.marked_point.instance.base import instance_t


@d.dataclass(slots=True, repr=False, eq=False)
class quality_context_t:
    """
    s_kwargs: for use in raw signal conversion into a signal used for quality
        computation.
    q_kwargs: marked-point-related; for use in quality computation.
    """

    s_defaults: h.ClassVar[dict[str, h.Any]] = {}
    q_defaults: h.ClassVar[dict[str, h.Any]] = {}

    signal: h.Any = None
    s_kwargs: dict[str, h.Any] | None = None
    q_kwargs: dict[str, h.Any] | None = None

    def SetKwargs(
        self, q_kwargs: dict[str, h.Any], s_kwargs: dict[str, h.Any], /
    ) -> None:
        """"""
        self._SetKwargsWithDefaults(
            q_kwargs, self.q_defaults, s_kwargs, self.s_defaults
        )

    def _SetKwargsWithDefaults(
        self,
        q_kwargs: dict[str, h.Any],
        q_defaults: dict[str, h.Any],
        s_kwargs: dict[str, h.Any],
        s_defaults: dict[str, h.Any],
        /,
    ) -> None:
        """"""
        for kwargs, defaults in ((q_kwargs, q_defaults), (s_kwargs, s_defaults)):
            invalid_s = set(kwargs.keys()).difference(defaults.keys())
            if invalid_s.__len__() > 0:
                invalid_s = ", ".join(invalid_s)
                L.StageIssue(
                    f"Invalid quality signal or quality parameter(s): {invalid_s}"
                )

            for name, value in defaults.items():
                if name not in kwargs:
                    kwargs[name] = value

        self.q_kwargs = q_kwargs
        self.s_kwargs = s_kwargs

    def SetSignal(self, raw_signal: h.Any, /) -> bool:
        """
        The returned value has a "signal is invalid" meaning. Consequently, any current
        procedure should abort.

        Default implementation: identity. The raw signal is also required to have the
        same dimension as the marked point model since this is probably a common
        requisite for quality computation. In case it is not, then SetSignalUnsafe can
        be "renamed" to SetSignal in derived quality context classes.
        """
        if raw_signal.ndim != MARKED_POINT_MODEL.dimension:
            return True

        self.signal = raw_signal
        return False

    def SetSignalUnsafe(self, raw_signal: h.Any, /) -> bool:
        """
        See SetSignal.
        """
        self.signal = raw_signal
        return False

    def Quality(self, instance: instance_t, /) -> float:
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
