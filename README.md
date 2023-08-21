# midi_fractal_noise

Tested on windows 11

## Install
```bash
pip install -r requirements.txt
```

## Use
### Print usage and exit
```bash
C:\Python310\python.exe run.py -h
```


### List available midi devices
```bash
PS C:\Users\tom_q\Documents\Projects\midi_fractal_noise> C:\Python310\python.exe run.py -l
Available midi devices:
  0: Microsoft GS Wavetable Synth 0
  1: Focusrite USB MIDI 1
  2: AXE-FX II MIDI Out 2
  3: MidiView 3

Exiting...
```


## Run with chosen device
```bash
C:\Python310\python.exe run.py -m Focusrite
```
