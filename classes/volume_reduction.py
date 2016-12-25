from array import array

class Volume_Reduction(object):
    def __init__(self, original_player, original_buff):
        self.player = original_player
        self.buff = original_buff
        self.frame_count = 0

    def read(self, frame_size):
        self.frame_count = self.frame_count + 1
        frame = self.buff.read(frame_size)

        volume = self.player.volume
        if volume < 1.0:
            frame_array = array('h', frame)

            for i in range(len(frame_array)):
                frame_array[i] = int(frame_array[i] * volume)

            frame = frame_array.tobytes()

        return frame
	