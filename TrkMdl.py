import numpy as np

# class PiNetwork:


class TrkMdl:
    def __init__(self,
                 r0=1.177,
                 c0=0,
                 l0=1.314e-3,
                 g0=0.1,
                 freq=1700,
                 interval=0.06,
                 cmp=12.5e-6,
                 ):
        w = 2 * np.pi * freq

        zc = np.sqrt((r0 + 1j * w * l0) / (g0 + 1j * w * c0))
        gama = np.sqrt((r0 + 1j * w * l0) * (g0 + 1j * w * c0))

        gl = gama * interval

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

        gama1 = gl_p/interval

        sh1 = np.sinh(gl_p)
        zc1 = zc * sh / sh1

        self.r0 = r0
        self.c0 = c0
        self.l0 = l0
        self.g0 = g0

        self.freq = freq
        self.w = w

        self.length = interval
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


class CableMdl:
    def __init__(self,
                 r0=43,
                 c0=28e-9,
                 l0=0.835e-3,
                 g0=10e-10,
                 freq=1700,
                 ):
        w = 2 * np.pi * freq

        zc = np.sqrt((r0 + 1j * w * l0) / (g0 + 1j * w * c0))
        gama = np.sqrt((r0 + 1j * w * l0) * (g0 + 1j * w * c0))

        self.r0 = r0
        self.c0 = c0
        self.l0 = l0
        self.g0 = g0

        self.freq = freq
        self.w = w

        self.zc1 = zc
        self.gama1 = gama

    def get_length_para(self, length):

        w = 2 * np.pi * self.freq

        zc = self.zc1
        gama = self.gama1

        gl = gama * length

        sh = np.sinh(gl)
        ch = np.cosh(gl)

        ya = (ch - 1) / (zc * sh)
        yb = 1 / (zc * sh)

        za = 1 / ya
        zb = 1 / yb

        r1 = np.real(zb)
        l1 = np.imag(zb) / w
        g1 = np.real(ya)
        c1 = np.imag(ya) / w

        return r1, l1, g1, c1
        # return ya, yb, za, zb

    def get_zl(self, z_in, length):
        zc = self.zc1
        gama = self.gama1
        gl = gama * length

        sh = np.sinh(gl)
        ch = np.cosh(gl)

        zl = (z_in * ch - sh * zc) / (- z_in / zc * sh + ch)

        return zl


class TransmissionMd:
    def __init__(self, trk, zl, length):
        self.trk = trk
        self.length = length
        self.zl = zl

        zc = self.trk.zc1
        gama = self.trk.gama1
        gl = gama * length

        sh = np.sinh(gl)
        ch = np.cosh(gl)

        self.vol = abs(ch + zc / zl * sh)
        self.z_in = (zl * ch + sh * zc) / (zl / zc * sh + ch)




if __name__ == '__main__':
    cable = CableMdl(r0=45)
    x1 = cable.get_length_para(4)
    print()



