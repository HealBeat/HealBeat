import pretty_midi, mido
from config import velocity_to_limb, NOTE_TO_DRUM

def open_midi_in(port_hint=""):
    names = mido.get_input_names()
    for n in names:
        if port_hint.lower() in n.lower():
            return mido.open_input(n)
    raise RuntimeError(f"MIDI 입력 포트를 찾을 수 없습니다. 현재 포트: {names}")

def extract_hits_from_midi(midi_path):
    pm = pretty_midi.PrettyMIDI(midi_path)
    hits = []
    for inst in pm.instruments:
        if inst.is_drum:
            for note in inst.notes:
                drum = NOTE_TO_DRUM.get(note.pitch)
                if drum:
                    limb = velocity_to_limb.get(note.velocity, None)
                    hits.append((note.start, drum, limb))
    hits.sort(key=lambda x: x[0])
    return hits
