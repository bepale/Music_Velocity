import pickle
import os
import midi

PATH = 'Input/'

def funcround(num) :
    '''
    Round off Function (사사오입 반올림 함수)
    Set the quantize to 1/16 (퀀타이즈 맞추기)

    :param num: data to round (반올림할 데이터)
    :return: rounded data (반올림된 데이터)
    '''
    jud = (num/0.125)%1
    jud = 1 if jud >0.5 else 0
    return (num//0.125+jud)*0.125

def extractmidi_information(Track,resolution) :
    '''
    Extract pitch, offset, and duration information

    :param Track: python midi track object (파이썬 미디의 트랙 오브젝트)
    :param resolution: midi resolution value (미디의 resolution 값)
    :return: List in pitch,offset,duration(피치, 오프셋, 듀레이션 값)
    '''
    nod = []
    PitchInfro = {}
    for event in Track :
        if not ( isinstance(event,midi.NoteEvent) or isinstance(event,midi.NoteOffEvent)) : continue
        stamp = event.tick / resolution # get a location
        # Note on event
        if isinstance(event,midi.NoteEvent) and event.data[1]>0 :
            PitchInfro[event.data[0]] = [stamp,event.data[1]]
        # Note off event
        elif event.data[0] in PitchInfro :
            Offset=  funcround(PitchInfro[event.data[0]][0])
            velocity = PitchInfro[event.data[0]][1]
            nod.append([event.data[0],Offset,funcround(stamp-Offset),velocity])
            del PitchInfro[event.data[0]]
    return nod


def make_Data():
    notes = []
    # Except Billie Jean, I Feel for You, Look Away, Hero
    except_midi = ["83-2-1", "85-5-1", "89-1-1", "89-1-2", "94-5-1", "94-5-2"]

    for i in os.listdir(PATH):
        if i in except_midi : continue
        # read midi file
        data = midi.read_midifile(PATH + i)
        # convert to relative value
        data.make_ticks_abs()
        nod = extractmidi_information(data[0], data.resolution)

        # delete data with small duration and empty data
        for _ in nod :
            if _ in notes : continue
            if _[2]*4 < 0.125 : continue
            notes.append(_)

    # save data
    with open("Data.pickle",'wb') as file:
        pickle.dump(notes,file)

if __name__ == "__main__" :
    make_Data()
