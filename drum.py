# Author :- Mohit Bhatia

import leap.Leap as Leap
from time import time, sleep
import subprocess

vel_tracker = {}
required_frame_count = 0

class DrumListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected to Leap"

        self.drums = []
        self.drums.append('snare.wav')
        self.drums.append('kick.wav')
        self.drums.append('tambourene.wav')
        self.drums.append('verb.wav')
        self.drums.append('1.wav')
        self.drums.append('chordD.wav')
        self.drums.append('pearll.wav')
        self.drums.append('chamber.wav')
        self.drums.append('drumroll.wav')
        self.last_drum_hit = []

        for x in xrange(len(self.drums)):
            self.last_drum_hit.append(6)

        self.ready_to_play = {}


    def on_frame(self, controller):
        global pointer_radius, x_range, required_frame_count

        frame = controller.frame()

        for hand in frame.hands:
            pos = hand.palm_position
            vel = hand.palm_velocity
            id = hand.id

            if vel.z < -350 and not id in self.ready_to_play:
               
                if not id in vel_tracker:
                    vel_tracker[id] = []
                count = len(vel_tracker[id])
                print str(count) + " for ID " + str(id)
                if count >= 1:
                    first_time = vel_tracker[id][0][2]
                    if time() - first_time > .8:
                        del vel_tracker[id]
                        vel_tracker[id] = []

                # Add in the frame
                if count < required_frame_count:
                    vel_tracker[id].append((vel, pos, time()))
                else:

                    vel_tracker[id] = []

                    # Play the appropriate drum in the array
                    drum_x = pos.x + 500
                    drum_x  = drum_x / 1000.0 * len(self.drums)
                    drum_x = int(drum_x)

                    self.ready_to_play[id] = drum_x
            # We might be moving backwards, so we should hit the drum
            elif vel.z > -100 and id in self.ready_to_play:
                drum_x = self.ready_to_play[id]
                # Make sure we aren't playing too fast
                if time() - self.last_drum_hit[drum_x] < .05:
                    print "Playing too fast on ID " + str(id)
                else:
                    print "hit"
                    subprocess.Popen(["afplay", self.drums[drum_x]])
                    self.last_drum_hit[drum_x] = time()

                del self.ready_to_play[id]



def main():
    global screen_size

    leap_controller = Leap.Controller()
    listener = DrumListener()

    leap_controller.add_listener(listener)


    sleep(0.01)

    finished = False
    while not finished:
        sleep(0.01)

    leap_controller.remove_listener(listener)

if __name__ == '__main__':
    main()

