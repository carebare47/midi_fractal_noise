import time
import rtmidi
from fractal_noise import FractalNoiseGenerator
from midi_coms import MidiOutWrapper

# minilogue_xd midi settings
MINILOGUE_MIDI_VCF_CUTOFF = 43
MINILOGUE_MIDI_VCF_MIN = 30
MINILOGUE_MIDI_VCF_MAX = 127
MINILOGUE_MIDI_CHANNEL = 2

# fractal noise parameters
OCTAVES = 6
DT = 1.0/50.0
SHOW_GRAPH = True
POINTS = 256
SPAN = 1.0
SPEED = 0.20

midiout = rtmidi.MidiOut()
# Swap for a string that partially matches your midi device
midi_port_search_term = 'Focusrite'
available_ports = midiout.get_ports()
midi_port_number = None

try:
    midi_port_number = [idx for idx, x in enumerate(available_ports) if midi_port_search_term in x][0]
except IndexError as e:
    print(e)
    print(f"Can't find '{midi_port_search_term}' as a substring for in any of the detected midi ports: {available_ports}")
    exit(0)


f = FractalNoiseGenerator(midi_out_min=MINILOGUE_MIDI_VCF_MIN,
                          midi_out_max=MINILOGUE_MIDI_VCF_MAX,
                          points=POINTS,
                          span=SPAN,
                          speed=SPEED,
                          octaves=OCTAVES,
                          dt=DT,
                          debug_window=SHOW_GRAPH)

midiout.open_port(midi_port_number)

midi_wrapper = MidiOutWrapper(midiout, ch=1)

with midiout:
    while True:
        next_value = f.return_next_point()
        f.my_step()
        midi_wrapper.send_control_change(cc=MINILOGUE_MIDI_VCF_CUTOFF, value=next_value, ch=MINILOGUE_MIDI_CHANNEL)
        print(f"sent {next_value}")
        time.sleep(DT)

del midiout


