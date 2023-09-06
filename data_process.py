import numpy as np
import pretty_midi as pyd
import os

from processor import MidiEventProcessor

total = 0
def preprocess_midi(path):
    global total
    data = pyd.PrettyMIDI(path)
    main_notes = []
    acc_notes = []
    for ins in data.instruments:
        acc_notes.extend(ins.notes)
    for i in range(len(main_notes)):
        main_notes[i].start = round(main_notes[i].start, 2)
        main_notes[i].end = round(main_notes[i].end, 2)
    for i in range(len(acc_notes)):
        acc_notes[i].start = round(acc_notes[i].start, 2)
        acc_notes[i].end = round(acc_notes[i].end, 2)
    main_notes.sort(key = lambda x:x.start)
    acc_notes.sort(key = lambda x:x.start)
    mpr = MidiEventProcessor()
    repr_seq = mpr.encode(main_notes+acc_notes)
    total += len(repr_seq)
    return repr_seq

def preprocess_pop909(midi_root, save_dir):
    save_py = []
    midi_paths = [d for d in os.listdir(midi_root)][:10]
    i = 0
    out_fmt = '{}-{}.data'
    for path in midi_paths:
        print(' ', end='[{}]'.format(path), flush=True)
        dirname = midi_root + path
        filename = os.path.join(dirname, [file for file in filter(lambda x: x.endswith('.mid'), [i[2] for i in os.walk(dirname)][0])][0])
        try:
            data = preprocess_midi(filename)
        except KeyboardInterrupt:
            print(' Abort')
            return
        except EOFError:
            print('EOF Error')
            return
        save_py.append(data)
    save_py = np.array(save_py)
    print(save_py.size)
    np.save("pop909-event-token.npy", save_py)

if __name__ == '__main__':
    # replace the folder with your POP909 data folder
    preprocess_pop909("POP909/","midi_data/")