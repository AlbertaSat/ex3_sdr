import pmt
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, trim_len=16):
        gr.sync_block.__init__(self, name='trim_pdu', in_sig=None, out_sig=None)
        self.trim_len = trim_len
        self.message_port_register_in(pmt.intern('in'))
        self.message_port_register_out(pmt.intern('out'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg):
        meta = pmt.car(msg)
        data = pmt.cdr(msg)
        vec = pmt.u8vector_elements(data)
        trimmed = vec[self.trim_len:]
        new_vec = pmt.init_u8vector(len(trimmed), trimmed)
        self.message_port_pub(pmt.intern('out'), pmt.cons(meta, new_vec))