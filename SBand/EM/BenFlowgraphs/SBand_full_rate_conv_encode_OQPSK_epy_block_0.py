import numpy as np
from gnuradio import gr


class intelsat_descrambler(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block

    def __init__(self):  # only default arguments here
        """arguments to this function how up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Intelsat Descrambler',   # will show up in GRC
            in_sig=[np.byte],
            out_sig=[np.byte]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
 
        self.LFSR = int(0xfffff)
        self.synchronousCount = 0

    def work(self, input_items, output_items):
        input_bits = input_items[0]
        out = output_items[0]

        for i in range(len(input_bits)):
            bit = int(input_bits[i]) & 1
            tap1 = self.LFSR & 1
            tap3 = (self.LFSR >> 2) & 1
            tap9 = (self.LFSR >> 8) & 1
            tap20 = (self.LFSR >> 19) & 1

            xnor1 = int(not (tap3 ^ tap20))
            xnor2 = int(not (xnor1 ^ int(self.synchronousCount == 0b11111)))
            xnor3 = int(not (xnor2 ^ bit))

            if not (tap1 ^ tap9):
                self.synchronousCount = (self.synchronousCount + 1) & 0b11111
            else:
                self.synchronousCount = 0

            self.LFSR = ((self.LFSR << 1) | bit) & 0xfffff
            out[i] = xnor3  # write each descrambled bit

        return len(input_bits)  # inform scheduler you handled this many items
