"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import inspect as nspt
import types as t
import typing as h

from logger_36 import L

parameter_t = nspt.Parameter

UNSUPPORTED_PARAMETER_KINDS = (
    parameter_t.POSITIONAL_OR_KEYWORD,
    parameter_t.VAR_POSITIONAL,
    parameter_t.VAR_KEYWORD,
)


class signature_t(h.NamedTuple):
    """
    kwargs: {name: (type, default_value)}.
    type[Any] is used as a simplified version of type[Any] | complex_type_hint.
    """

    has_unsupported: bool
    kwargs: dict[str, tuple[h.Any, h.Any]]
    return_type: type | t.GenericAlias | None

    @classmethod
    def Of(cls, function: h.Callable, /) -> h.Self:
        """"""
        signature = nspt.signature(function)

        has_unsupported = False
        kwargs = {}
        for name, value in signature.parameters.items():
            if value.kind == parameter_t.KEYWORD_ONLY:
                kwargs[name] = (value.annotation, value.default)
            elif value.kind in UNSUPPORTED_PARAMETER_KINDS:
                has_unsupported = True

        return cls(
            has_unsupported=has_unsupported,
            kwargs=kwargs,
            return_type=signature.return_annotation,
        )


def CheckPassedParameters(
    Function: h.Callable,
    parameters: dict[str, h.Any],
    expected_type: type | t.GenericAlias | None,
    /,
) -> None:
    """"""
    signature = signature_t.Of(Function)
    if signature.has_unsupported:
        L.StageIssue(
            f"{Function.__name__} has parameter(s) with unsupported kind. "
            f"Supported kinds are {parameter_t.POSITIONAL_ONLY} "
            f"and {parameter_t.KEYWORD_ONLY}."
        )

    if signature.return_type != expected_type:
        L.StageIssue(
            f"{Function.__name__}: Invalid return type(s)",
            actual=signature.return_type,
            expected=expected_type,
        )

    valid_names = tuple(signature.kwargs.keys())
    for name, value in parameters.items():
        if name in signature.kwargs:
            stripe = signature.kwargs[name][0]
            if not isinstance(value, stripe):
                L.StageIssue(
                    f"Incorrect parameter type passed for {Function.__name__}:{name}",
                    actual=f"{value} with type {type(value).__name__}",
                    expected=stripe,
                )
        else:
            L.StageIssue(
                f"Invalid parameter passed to {Function.__name__}",
                actual=name,
                expected=valid_names,
                expected_is_choices=True,
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
