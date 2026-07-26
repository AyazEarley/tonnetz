import pretty_midi
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_notes(filename):
    pm = pretty_midi.PrettyMIDI(os.path.join(BASE_DIR, "assets", "midi", filename))
    notes = []
    for instrument in pm.instruments:
        for note in instrument.notes:
            notes.append(note)
    return notes

celesteEvents = load_notes("celeste.mid")
crotalesEvents = load_notes("crotales.mid")
harpEvents = load_notes("harp.mid")