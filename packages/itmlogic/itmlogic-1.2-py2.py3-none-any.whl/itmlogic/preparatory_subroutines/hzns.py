def hzns(pfl, dist, hg, gme):
    """
    Subroutine to find horizon parameters as described in Section 48 by Hufford
    (see references/itm.pdf).

    Parameters
    ----------
    pfl : List
        Terrain profile in meters.
    dist : float
        Distance in meters.
    hg : list
        Heights of transmitter and receiver off ground (meters).
    gme : float
        Effective earth curvature.

    Returns
    -------
    the : dict
        Horizon take-off angle.
    dl : dict
        Horizon distances.

    """
    the = {}
    dl = {}

    np = pfl[0]
    xi = pfl[1]
    za = pfl[2] + hg[0]
    zb = pfl[np + 2] + hg[1]
    qc = 0.5 * gme
    q = qc * dist
    the[1] = (zb - za) / dist
    the[0] = the[1] - q
    the[1] = -the[1] - q
    dl[0]  = dist
    dl[1]  = dist

    if np >= 2:
        sa = 0
        sb = dist
        wq = 1

        for i in range(2, np + 1):

            sa = sa + xi
            sb = sb - xi

            q = pfl[i+1] - (qc * sa + the[0]) * sa - za

            if q > 0:
                the[0] = the[0] + q / sa
                dl[0] = sa

                wq = 0

            if wq == 0:
                q = pfl[i + 1] - (qc * sb + the[1]) * sb - zb
                if q > 0:
                    the[1] = the[1] + q / sb
                    dl[1] = sb

    return the, dl
