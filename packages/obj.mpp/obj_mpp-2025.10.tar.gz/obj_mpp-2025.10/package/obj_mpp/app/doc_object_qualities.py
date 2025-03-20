"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

from obj_mpp.constant.catalog import Q_CATALOG_SECTION
from obj_mpp.task.catalog.importer import ImportedElement

ROW_WIDTH = 35
TYPE_ROW_WIDTH = 14


def Main() -> None:
    """"""
    quality_context_t = ImportedElement(None, Q_CATALOG_SECTION)

    quality_row_width = (
        max(
            quality_class[0].__name__.__len__()
            for quality_class in quality_context_t.values()
        )
        - 2
        + 4
    )
    empty_quality_class = quality_row_width * " "
    row_widths = (quality_row_width, ROW_WIDTH, TYPE_ROW_WIDTH, ROW_WIDTH)
    hline = "+" + "+".join((row_width + 2) * "-" for row_width in row_widths) + "+"

    print(
        f"{hline}\n"
        f"| {'**Quality**':{quality_row_width}} "
        f"| {'**Parameter**':{ROW_WIDTH}} "
        f"| {'**Type**':{TYPE_ROW_WIDTH}} "
        f"| {'**Default Value**':{ROW_WIDTH}} |\n"
        f"{hline}\n"
        f"{hline}",
    )

    for quality_name, quality_class in quality_context_t.items():
        print(f"| {quality_name:{quality_row_width}} ", end="")

        value = quality_class[0]()
        value.SetKwargs({}, {})
        for kwargs in (value.s_kwargs, value.q_kwargs):
            if kwargs is None:
                continue

            subsequent = False
            for name, value in kwargs.items():
                if name.startswith("_"):
                    continue

                if subsequent:
                    print(f"| {empty_quality_class} ", end="")
                else:
                    subsequent = True
                print(
                    f"| {name:{ROW_WIDTH}} "
                    f"| {TYPE_ROW_WIDTH * ' '} "
                    f"| {value:{ROW_WIDTH}} |\n"
                    f"{hline}",
                )

        print(hline)


if __name__ == "__main__":
    #
    Main()

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
