import numpy as nu
import wave
import sys
import struct

def open_wave(filename):
    return wave.open(filename)
    # f= wave.load(filename)
    # return f[1][0]

def main():
    if len(sys.argv) > 2:
        print("Wrong Number Arguments")
        raise SystemExit

    wav= open_wave(sys.argv[1])

    isStereo=False
    countOfChannels=wav.getnchannels()
    if(countOfChannels==2):
        isStereo=True
    frameRate=wav.getframerate()
    countOfFrames=wav.getnframes()
    sampleWidth=wav.getsampwidth()

    maximum= None
    minimum = None


    for j in range(0, int(countOfFrames/frameRate)):


        peaks=[]
        test = wav.readframes(wav.getframerate())
        datas = struct.unpack("%ih" % (wav.getframerate() * wav.getnchannels()), test)
        datas= nu.array(datas)
        if countOfChannels == 2:
            datas = list(map(lambda i, j: (i + j) / 2, datas[0::2], datas[1::2]))

        fft_data = (nu.fft.rfft(datas) / frameRate)
        fft_data = nu.abs(fft_data[:(frameRate//2)])
        avg = nu.average(fft_data)
        peak = 20 * avg

        for k, amp in enumerate(fft_data):
            if amp >= peak:
                peaks.append(k)

        if len(peaks) != 0:
            if maximum is None or max(peaks) > maximum:
                maximum = max(peaks)
            if minimum is None or min(peaks) < minimum:
                minimum = min(peaks)

    if minimum is not None and maximum is not None:
        print("low = "+str(minimum)+", high = " +str(maximum))
    else:
        print("no peaks")



    wav.close()

if __name__ == '__main__':
    main()


