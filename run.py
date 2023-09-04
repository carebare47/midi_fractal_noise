import os
import time
import rtmidi
from fractal_noise import FractalNoiseGenerator
from midi_coms import MidiOutWrapper
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--list', '-l', action='store_true', help='List available midi devices and exit')
parser.add_argument('--midi_device', '-m', help='Overwrite default midi device, '\
                                                'a substring match will do (run with -l to show available devices)')
parser.add_argument('--hide_graph', '-g', action='store_true', help='Hide debug window')
parser.add_argument('--print', '-p', action='store_true', help='Print value sent to midi device')

args = parser.parse_args()
list_midi_devices_only = args.list
if 'posix' in os.name:
    midi_port_search_term = 'Claret'
else:
    midi_port_search_term = 'Focusrite'
if args.midi_device:
    midi_port_search_term = args.midi_device
print_value = args.print

# minilogue_xd midi settings
MINILOGUE_MIDI_VCF_CUTOFF_CC = 43
MINILOGUE_MIDI_VCF_MIN = 44
MINILOGUE_MIDI_VCF_MAX = 127
MINILOGUE_MIDI_CHANNEL = 2

# fractal noise parameters
OCTAVES = 5
DT = 1.0/50.0
SHOW_GRAPH = not args.hide_graph
POINTS = 256
SPAN = 1.0
SPEED = 0.20

try:
    midiout = rtmidi.MidiOut()
except rtmidi.SystemError as e:
    pass
midiout = rtmidi.MidiOut()
# Swap for a string that partially matches your midi device
available_ports = midiout.get_ports()
if list_midi_devices_only:
    print("Available midi devices:")
    for idx, port in enumerate(available_ports):
        print(f"  {idx}: {port}")
    print("\nExiting...\n")
    exit(0)

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
        midi_wrapper.send_control_change(cc=MINILOGUE_MIDI_VCF_CUTOFF_CC, value=next_value, ch=MINILOGUE_MIDI_CHANNEL)
        if not print_value:
            print(f"sent {next_value}")
        time.sleep(DT)

del midiout


