"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2018
SEE COPYRIGHT NOTICE BELOW
"""

"""
Just import this module to turn debugging on.
"""

import faulthandler as flth

flth.enable()


# def CallTracker(frame, event, _, indent = [0]):
#     """
#     Inspired from:
#     https://stackoverflow.com/questions/8315389/how-do-i-print-functions-as-they-are-called
#     answered Nov 29 '11 at 18:11 by kindall   (https://stackoverflow.com/users/416467/kindall)
#     edited   Dec  7 '15 at  2:44 by martineau (https://stackoverflow.com/users/355230/martineau)
#     improved Nov 21 '18 at  1:44 by ChaimG    (https://stackoverflow.com/users/2529619/chaimg)
#     """
#     code = frame.f_code
#
#     modname_start = code.co_filename.find('/mpp/')
#     if modname_start < 0:
#         return
#     else:
#         modname_start += 5
#
#     if event == 'call':
#         indent[0] += 2
#         print(f'{"=" * indent[0]}> {code.co_filename[modname_start:-3]}:{code.co_name}@{code.co_firstlineno}')
#     elif event == 'return':
#         print(f'<{"-" * indent[0]} {code.co_filename[modname_start:-3]}:{code.co_name}')
#         indent[0] -= 2
#
#     return CallTracker
#
# import sys as sstm; sstm.settrace(CallTracker)


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
