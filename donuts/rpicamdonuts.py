'''This code is inheritated from donuts for sending
   PiCamera Y channel data into donuts algorithm.
'''
from .donuts import Donuts
from .image import Image
import numpy as np

class RPiCamDonuts(Donuts):
    
    def construct_object(self, image_input):
        image = np.empty(100, np.uinit8).reshape(10,10)
        header = {NAXIS:2, NAXIS1:10, NAXIS:10, exposure: self.exposure_keyname}
        if isinstance(image_input, str):
            with fits.open(filename) as hdulist:
                hdu = hdulist[self.image_ext]
                image = hdu.data
                header = hdu.header
        else:
            image = image_input
            if isinstance(image_input, list):
                image = np.array(image_input)
            header['NAXIS2'], header['NAXIS1'] = image.shape
            

        image = self.image_class(image, header)
        image.preconstruct_hook()
        image.trim(
            prescan_width=self.prescan_width,
            overscan_width=self.overscan_width,
            border=self.border
        )

        if self.normalise:
            image.normalise(
                exposure_keyword=self.exposure_keyname
            )

        if self.subtract_bkg:
            image.remove_background(
                ntiles=self.ntiles
            )

        image.postconstruct_hook()
        image.compute_projections()

        return image
