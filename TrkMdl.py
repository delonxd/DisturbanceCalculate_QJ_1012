import numpy as np


class TrkMdl:
    def __init__(self,
                 r0=1.177,
                 c0=0,
                 l0=1.314e-3,
                 g0=0.1,
                 freq=1700,
                 length=0.06,
                 cmp=12.5e-6,
                 ):
        w = 2 * np.pi * freq

        zc = np.sqrt((r0 + 1j * w * l0) / (g0 + 1j * w * c0))
        gama = np.sqrt((r0 + 1j * w * l0) * (g0 + 1j * w * c0))

        gl = gama * length

        sh = np.sinh(gl)
        ch = np.cosh(gl)

        # ya = (ch - 1) / (zc * sh)
        # yb = 1 / (zc * sh)
        #
        # za = 1 / ya
        # zb = 1 / yb

        ycmp = 1j * w * cmp

        ch1 = ch + zc * sh * ycmp
        gl_p = np.arccosh(ch1)

        gama1 = gl_p/length

        sh1 = np.sinh(gl_p)
        zc1 = zc * sh / sh1

        self.r0 = r0
        self.c0 = c0
        self.l0 = l0
        self.g0 = g0

        self.freq = freq
        self.w = w

        self.length = length
        self.cmp = cmp
        self.ycmp = ycmp

        self.zc = zc
        self.gama = gama
        self.sh = sh
        self.ch = ch

        self.zc1 = zc1
        self.gama1 = gama1
        self.sh1 = sh1
        self.ch1 = ch1
