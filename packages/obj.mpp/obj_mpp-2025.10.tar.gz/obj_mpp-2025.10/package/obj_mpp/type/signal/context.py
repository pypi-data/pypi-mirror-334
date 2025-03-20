"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import collections.abc as a
import dataclasses as d
import typing as h
from pathlib import Path as path_t

import numpy as nmpy
from logger_36 import L
from obj_mpp.interface.storage.api import signal_loading_fct_p
from obj_mpp.type.signal.domain import domain_h

array_t = nmpy.ndarray


@d.dataclass(slots=True, repr=False, eq=False)
class signal_context_t:
    """
    Domain-related details correspond to the domain the marked points will be
    superimposed on. In particular, the dimension is the dimension of marked points.
    """

    dimension: int | None = None
    lengths: tuple[int, ...] | None = None
    domain: domain_h | None = None
    grid_sites: tuple[array_t, ...] | None = None
    grid_sites_flat: tuple[array_t, ...] | None = None

    signal_original: h.Any = None
    signal_for_qty: h.Any = None
    map_or_pdf: array_t | None = None
    map_or_pdf_is_new: bool = False

    path_signal: path_t | None = None
    path_map_or_pdf: path_t | None = None

    SignalLoadedFrom: signal_loading_fct_p | None = None
    loading_prm: dict[str, h.Any] | None = None

    def Initialize(
        self,
        path_signal: str | path_t,
        path_map_or_pdf: str | path_t,
        SignalLoadedFrom: signal_loading_fct_p,
        dimension: int,
        /,
        **loading_prm,
    ) -> None:
        """"""
        self.dimension = dimension
        self.SignalLoadedFrom = SignalLoadedFrom
        self.loading_prm = loading_prm

        self.path_signal = path_t(path_signal)
        if isinstance(path_map_or_pdf, (str, path_t)):
            # TODO: Should there be a message about incorrect type? Is it even possible?
            self.path_map_or_pdf = path_t(path_map_or_pdf)

    def LazySignalDetails(self) -> a.Iterator[tuple[path_t, str | None]]:
        """"""
        if self.path_signal.is_dir():
            paths_signal = self.path_signal.rglob("*.*")
        else:
            paths_signal = (self.path_signal,)

        if self.path_map_or_pdf is None:
            MapOrPDFPathFromSignal = lambda _arg: None
            should_skip_map_or_pdf = next_should_skip = True
        elif self.path_map_or_pdf.is_file():
            MapOrPDFPathFromSignal = lambda _arg: self.path_map_or_pdf
            should_skip_map_or_pdf = False
            next_should_skip = True
        elif self.path_signal.is_file():
            MapOrPDFPathFromSignal = lambda _arg: self.path_map_or_pdf / _arg.name
            should_skip_map_or_pdf = False
            next_should_skip = True
        else:
            MapOrPDFPathFromSignal = (
                lambda _arg: self.path_map_or_pdf / _arg.relative_to(self.path_signal)
            )
            should_skip_map_or_pdf = next_should_skip = False

        for path_signal in paths_signal:
            if not path_signal.is_file():
                continue

            no_errors = True
            for path, SetLoaded, should_skip in (
                (path_signal, self.SetSignals, False),
                (
                    MapOrPDFPathFromSignal(path_signal),
                    self.SetMapOrPDF,
                    should_skip_map_or_pdf,
                ),
            ):
                if should_skip:
                    continue

                loaded, error = self.SignalLoadedFrom(path, **self.loading_prm)
                if error is None:
                    SetLoaded(loaded)
                else:
                    no_errors = False
                    L.error(f"Unable to load {path}:\n{error}")
                    break

            self.map_or_pdf_is_new = not should_skip_map_or_pdf
            should_skip_map_or_pdf = next_should_skip

            if no_errors:
                yield path_signal, f"{path_signal.stem}_{path_signal.suffix[1:]}"
            else:
                yield path_signal, None

    def SetSignals(
        self,
        signal: h.Any,
        /,
        *,
        reset_mode: bool = False,
    ) -> None:
        """"""
        if reset_mode or (self.dimension is None):
            # If not reset_mode, then initialize has not been called.
            self.dimension = signal.ndim
        self.lengths = signal.shape[: self.dimension]
        self.domain = tuple((0, _elm - 1) for _elm in self.lengths)
        self.grid_sites = nmpy.indices(self.lengths)
        self.grid_sites_flat = tuple(_elm.flatten() for _elm in self.grid_sites)

        self.signal_original = signal

        abs_min = abs(signal.min())
        abs_max = abs(signal.max())
        max_of_abs = max(abs_min, abs_max)
        self.signal_for_qty = signal.astype(nmpy.float64, copy=False) / max_of_abs

    def SetMapOrPDF(self, map_or_pdf: array_t, /) -> None:
        """"""
        self.map_or_pdf = map_or_pdf


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
