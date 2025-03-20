"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import tempfile as tmpf
from pathlib import Path as path_t

from logger_36 import L


def CreateOutputFolder(path: path_t, /) -> path_t:
    """"""
    output = path

    if path.exists():
        if (not path.is_dir()) or (tuple(path.iterdir()).__len__() > 0):
            output = None
            L.error(f"Not a folder or not empty: {path}")
    else:
        try:
            path.mkdir()
        except Exception as error:
            output = None
            L.error(f"Folder creation failed for: {path}\nwith error:\n{error}")

    if output is None:
        output = path_t(tmpf.mkdtemp())
        L.info(f"Temporary alternative output folder: {output}")

    return output


def OutputDocument(
    base_path: path_t,
    basename: str,
    extension: str,
    signal_id: str | None,
    /,
    *,
    for_all_dates: bool = False,
) -> path_t:
    """"""
    if signal_id is None:
        # For interactive workflow where path was chosen by user
        output = base_path
    else:
        # For non-interactive workflow where path is chosen by Obj.MPP
        if for_all_dates:
            path = base_path.parent / "*"
        else:
            path = base_path
        output = path / f"{signal_id}-{basename}.{extension}"

    return output


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
