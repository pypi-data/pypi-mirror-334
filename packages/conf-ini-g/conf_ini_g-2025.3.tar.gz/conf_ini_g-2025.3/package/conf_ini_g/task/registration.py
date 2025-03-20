"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2021
SEE COPYRIGHT NOTICE BELOW
"""

import types as t
from pathlib import Path as path_t

from babelwidget.main import base_h as library_wgt_h
from conf_ini_g.catalog.boolean import boolean_wgt_t

# from conf_ini_g.catalog.callable import callable_wgt_t
from conf_ini_g.catalog.choices import choices_wgt_t
from conf_ini_g.catalog.collection import collection_wgt_t
from conf_ini_g.catalog.none import none_wgt_t
from conf_ini_g.catalog.path import path_wgt_t
from conf_ini_g.catalog.text_line import text_line_t
from value_factory.api.catalog import choices_t  # callable_t
from value_factory.api.type import hint_t

# TODO: callable_t still a WIP.

# Widgets can be mapped from types or annotations. Since annotations are more specific
# than types, they must be placed first to ensure they get a chance to be selected.
_TYPE_WIDGET_TRANSLATOR: dict[type, type[library_wgt_h]] = {
    # Annotations
    # callable_t: callable_wgt_t,
    choices_t: choices_wgt_t,
    # Types
    t.NoneType: none_wgt_t,
    t.UnionType: choices_wgt_t,
    bool: boolean_wgt_t,
    float: text_line_t,
    int: text_line_t,
    list: collection_wgt_t,
    path_t: path_wgt_t,
    set: collection_wgt_t,
    str: text_line_t,
    tuple: collection_wgt_t,
}


def RegisterNewTranslation(new_type: type, widget_type: type[library_wgt_h], /) -> None:
    """"""
    if new_type in _TYPE_WIDGET_TRANSLATOR:
        # Raising an exception is adapted here since it is a developer-oriented function
        raise ValueError(
            f'{new_type.__name__}: Type already registered with "{_TYPE_WIDGET_TRANSLATOR[new_type]}" '
            f"in type-to-widget translations."
        )

    _TYPE_WIDGET_TRANSLATOR[new_type] = widget_type


def ValueWidgetTypeForType(stripe: hint_t, /) -> type[library_wgt_h]:
    """"""
    base_hint = stripe.type
    nnts = stripe.annotations
    if nnts is None:
        nnts = ()

    for registered_type, widget_type in _TYPE_WIDGET_TRANSLATOR.items():
        if (base_hint is registered_type) or any(
            issubclass(type(_nnt), registered_type) for _nnt in nnts
        ):
            return widget_type

    return text_line_t


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
