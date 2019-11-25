from intercom_bitplanes import Intercom_bitplanes

if __debug__:
    import sys
# Exploiting binaural redundancy.

class Intercom_binaural(Intercom_bitplanes):

    def init(self, args):
        Intercom_bitplanes.init(self, args)
        if self.number_of_channels == 2:
            self.record_send_and_play = self.record_send_and_play_stereo

    def record_send_and_play_stereo(self, indata, outdata, frames, time, status):
        
        #substract R=R-L
        indata[:, 0] -= indata[:, 1]
        
        self.send(indata)
        
        self.recorded_chunk_number = (self.recorded_chunk_number + 1) % self.MAX_CHUNK_NUMBER
        
        #access the buffer and obtain chunk
        chunk = self._buffer[self.played_chunk_number % self.cells_in_buffer]
        
        #Restore 
        chunk[:, 0] +=chunk[:, 1]

        self._buffer[self.played_chunk_number % self.cells_in_buffer] = self.generate_zero_chunk()
        self.played_chunk_number = (self.played_chunk_number + 1) % self.cells_in_buffer
        
        outdata[:] = chunk
        indata[:,0] -= indata[:,1]
        self.record_and_send(indata)
        self._buffer[self.played_chunk_number % self.cells_in_buffer][:,0] += self._buffer[self.played_chunk_number % self.cells_in_buffer][:,1]
        self.play(outdata)


if __name__ == "__main__":
    intercom = Intercom_binaural()
    parser = intercom.add_args()
    args = parser.parse_args()
    intercom.init(args)
    intercom.run()
