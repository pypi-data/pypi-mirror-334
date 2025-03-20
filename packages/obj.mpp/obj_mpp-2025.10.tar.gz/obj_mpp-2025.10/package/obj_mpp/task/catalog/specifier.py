"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

import typing as h

from conf_ini_g.api.functional import config_t
from obj_mpp.constant.catalog import MPM_CATALOG_SECTION, Q_CATALOG_SECTION
from obj_mpp.constant.config.label import label_e
from obj_mpp.task.catalog.importer import ImportedElement
from obj_mpp.type.marked_point.model.mark import mark_h
from value_factory.api.catalog import collection_t


def SpecifyCatalogMarkedPoints(config: config_t, /) -> None:
    """"""
    s_name = label_e.sct_mark_ranges.value
    basic = config[s_name].ppt.basic
    mark_hint = h.Annotated[tuple, collection_t(items_types=mark_h, lengths=(2, 3))]

    for mkpt_name, mkpt_type in ImportedElement(None, MPM_CATALOG_SECTION).items():
        for mark, definition in mkpt_type().items():
            config.AddPluginParameter(
                s_name,
                mark,
                hint=mark_hint,
                default=definition.default_interval,
                controlling_value=mkpt_name,
                basic=basic,
            )


def SpecifyCatalogQualities(config: config_t, /) -> None:
    """"""
    s_name = label_e.sct_quality_prm.value
    basic = config[s_name].ppt.basic

    for q_name, (q_context, _) in ImportedElement(None, Q_CATALOG_SECTION).items():
        for p_name, value in q_context.q_defaults.items():
            config.AddPluginParameter(
                s_name,
                p_name,
                hint=type(value),
                default=value,
                controlling_value=q_name,
                basic=basic,
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
