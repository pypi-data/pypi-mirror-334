"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

from obj_mpp.constant.catalog import MPM_CATALOG_SECTION
from obj_mpp.task.catalog.importer import ImportedElement

ROW_WIDTH = 35
TYPE_ROW_WIDTH = 14
FLOAT_PRECISION = 3


def Main() -> None:
    """"""
    model_t = ImportedElement(None, MPM_CATALOG_SECTION)

    mkpt_row_width = (
        max(class_type.__name__.__len__() for class_type in model_t.values()) - 2 + 4
    )
    empty_mkpt_class = mkpt_row_width * " "
    row_widths = (mkpt_row_width, ROW_WIDTH, TYPE_ROW_WIDTH) + 3 * (ROW_WIDTH,)
    hline = "+" + "+".join((row_width + 2) * "-" for row_width in row_widths) + "+"

    print(
        f"{hline}\n"
        f"| {'**Object**':{mkpt_row_width}} "
        f"| {'**Mark**':{ROW_WIDTH}} "
        f"| {'**Type**':{TYPE_ROW_WIDTH}} "
        f"| {'**Valid Range**':{ROW_WIDTH}} "
        f"| {'**Default Range**':{ROW_WIDTH}} "
        f"| {'**Default Precision**':{ROW_WIDTH}} |\n"
        f"{hline}\n"
        f"{hline}"
    )

    for element_name, element_t in model_t.items():
        print(f"| {element_name:{mkpt_row_width}} ", end="")

        model = element_t()
        for detail_idx, (name, value) in enumerate(model.items()):
            ini_name = f"``{name}``"
            mark_type = f"*{value.type.__name__}*"

            extreme_values = []
            if value.min_inclusive:
                extreme_values.append("[")
            else:
                extreme_values.append("]")
            if issubclass(value.type, float):
                extreme_values.append(
                    f"{value.min:.{FLOAT_PRECISION}}, {value.max:.{FLOAT_PRECISION}}"
                )
            else:
                extreme_values.append(f"{value.min}, {value.max}")
            if value.max_inclusive:
                extreme_values.append("]")
            else:
                extreme_values.append("[")

            if value.default_interval is None:
                default_interval = "None"
            else:
                if issubclass(value.type, float):
                    low_bound = f"{value.default_interval[0]:.{FLOAT_PRECISION}}"
                    high_bound = f"{value.default_interval[1]:.{FLOAT_PRECISION}}"
                else:
                    low_bound = value.default_interval[0]
                    high_bound = value.default_interval[1]
                default_interval = f"({low_bound}, {high_bound})"

            if value.default_precision is None:
                default_precision = "None"
            else:
                if issubclass(value.type, float):
                    default_precision = f"{value.default_precision:.{FLOAT_PRECISION}}"
                else:
                    default_precision = value.default_precision

            if detail_idx > 0:
                print(f"| {empty_mkpt_class} ", end="")
            print(
                f"| {ini_name:{ROW_WIDTH}} "
                f"| {mark_type:{TYPE_ROW_WIDTH}} "
                f"| {''.join(extreme_values):{ROW_WIDTH}} "
                f"| {default_interval:{ROW_WIDTH}} "
                f"| {default_precision:{ROW_WIDTH}} |\n"
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
