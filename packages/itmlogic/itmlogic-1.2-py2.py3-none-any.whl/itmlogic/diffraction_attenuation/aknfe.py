import math
import numpy as np

def aknfe(v2):
    """
    Returns the attenuation due to a single knife edge - the Fresnel integral (in decibels,
    Eqn 4.21 of "The ITS Irregular Terrain Model, version 1.2.2: The Algorithm" – see also
    Eqn 6.1) evaluated for nu equal to the square root of the input argument.

    Parameters
    ----------
    v2 : float
        Input for computing knife edge diffraction.

    Returns
    -------
    aknfe1 : float
        Attenuation due to a single knife edge.

    """
    if v2 < 5.76:
        if v2 <= 0: ### addition to avoid logging v2 <= 0
            v2 = 0.00001 ### addition to avoid logging v2 <= 0
        aknfe1 = 6.02 + 9.11 * math.sqrt(v2) - 1.27 * v2

    else:

        aknfe1 = 12.953 + 4.343 * np.log(v2)

    return aknfe1
