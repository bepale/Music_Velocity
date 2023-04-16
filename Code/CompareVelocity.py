import os
import midi
import json

# load json to midi name information
with open("Infomation.json",'r') as file :
    Info =json.load(file)

PATH = 'Comp/'
offset_dict = {}
BarLength = 32 # 8 bar value

def func_comparemidi(usr_PATH) :
    '''
    Record the information of the MIDI to be compared

    :param usr_PATH: midi path
    '''
    for data in os.listdir(usr_PATH) :
        if 'pickle' in data: continue
        music = midi.read_midifile(usr_PATH + data)
        music.make_ticks_abs()
        if data not in offset_dict: offset_dict[data] = {}
        for event in music[-1] :
            if isinstance(event,midi.NoteOnEvent) and event.data[1]>0 :
                offset = event.tick/music.resolution
                if offset not in offset_dict[data]  :
                    offset_dict[data][offset] = []
                offset_dict[data][offset].append(event.data[1])

def func_printinfo(Array,rownum) :
    x = 0
    while x < rownum:
        for y in range(len(Array)):
            if Array[y][x]:
                print("%.2f" % (sum(Array[y][x]) / len(Array[y][x])), end='\t')
            else:
                print(end='\t')
        x += 1
        print()
    print()

if __name__ == "__main__" :

    for i in os.listdir(PATH) :
        func_comparemidi(PATH+i+'/')
    row = os.listdir(PATH)
    rownum = len(row)-1

    for i in offset_dict :
        print(Info[i],end='\t')
        print(i.split('.')[0],end='\t')
        col = list(offset_dict[i].keys())
        Arr = [[] for _ in range(rownum)]
        maxval = int(max(col))+1
        if maxval < BarLength : maxval = BarLength
        A= [[[] for __ in range(rownum)] for _ in range(maxval)]
        B = [[[] for __ in range(rownum)] for _ in range(maxval*2)]
        for j in offset_dict[i] :
            root = offset_dict[i][j][0]
            off = int(j)
            for idx,k in enumerate(offset_dict[i][j][1:]) :
                Arr[idx].append(abs(root-k))
                A[off][idx].append(abs(root-k))
                B[int(j*2)][idx].append(abs(root - k))

        func_printinfo(A,rownum)
        func_printinfo(B, rownum)