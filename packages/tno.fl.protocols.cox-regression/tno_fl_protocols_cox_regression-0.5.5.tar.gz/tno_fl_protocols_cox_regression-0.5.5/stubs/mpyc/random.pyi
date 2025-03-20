# pylint: disable=unused-argument

from collections.abc import Sequence

from mpyc.sectypes import SecureNumber

def shuffle(
    sectype: type[SecureNumber], x: Sequence[SecureNumber]
) -> Sequence[SecureNumber]: ...
