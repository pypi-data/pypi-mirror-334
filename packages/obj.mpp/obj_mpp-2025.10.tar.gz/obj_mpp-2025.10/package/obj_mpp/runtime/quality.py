"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as d
import typing as h

from obj_mpp.type.quality.base import quality_context_t


@d.dataclass(slots=True, repr=False, eq=False)
class _proxy_t:
    _actual: quality_context_t | None = None

    def Initialize(
        self,
        stripe: type[quality_context_t],
        /,
        *,
        q_kwargs: dict[str, h.Any] | None = None,
        s_kwargs: dict[str, h.Any] | None = None,
    ) -> None:
        """"""
        if q_kwargs is None:
            q_kwargs = {}
        if s_kwargs is None:
            s_kwargs = {}
        self._actual = stripe()
        self._actual.SetKwargs(q_kwargs, s_kwargs)

    def __getattr__(self, item: h.Any, /) -> h.Any:
        """"""
        return getattr(self._actual, item)

    def __getitem__(self, item: h.Any, /) -> h.Any:
        """"""
        # TODO: Can self._actual be a sequence???
        return self._actual[item]


QUALITY_CONTEXT = _proxy_t()


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
