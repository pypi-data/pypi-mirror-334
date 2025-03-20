"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import glob
from pathlib import Path as path_t

from json_any.api.storage import LoadFromJSON
from logger_36 import L
from obj_mpp.constant.interface.storage import JSON_BASE_NAME
from obj_mpp.constant.signal import INFINITY_NUMPY_FLOAT
from obj_mpp.interface.storage.save.generic import OutputDocument
from obj_mpp.type.marked_point.instance.base import instance_t


def PreviousDetection(
    use_history: bool, fixed_history: bool, base_path: path_t, signal_id: str, /
) -> list[instance_t] | None:
    """"""
    if not use_history:
        return None

    path = OutputDocument(
        base_path, JSON_BASE_NAME, "json", signal_id, for_all_dates=True
    )
    history_documents = sorted(glob.glob(str(path)))
    if history_documents.__len__() == 0:
        L.warning("No history found; To be disregarded if first run.")
        return None

    history_document = history_documents[-1]

    output, issues = LoadFromJSON(history_document)
    if (issues is not None) and (issues.__len__() > 0):
        L.error("\n".join(issues))
        return None

    if output.__len__() == 0:
        return None

    for instance in output:
        instance.age = 1
        if fixed_history:
            instance.quality = INFINITY_NUMPY_FLOAT

    L.info(f"Using history {history_document} with {output.__len__()} object(s).")

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
