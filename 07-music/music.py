import sys
import wave
import struct
import numpy as np

def unpackFrames(myMusicFile, channels, frameRate,step):
    myMusicFile.rewind()
    myMusicFile.setpos(step)
    unpackedData = struct.unpack("%ih" % (channels * frameRate), myMusicFile.readframes(frameRate))

    if channels == 2:

        unpackedData = list(map(lambda x, y: (x + y) / 2, unpackedData[0::2], unpackedData[1::2]))

    return unpackedData


def main():
    if len(sys.argv) != 3:
        print("Wrong Number Arguments")
        raise SystemExit


    myReferenceNumber=int(sys.argv[1])

    with wave.open(sys.argv[2],'r') as myMusicFile:
        channels= myMusicFile.getnchannels()
        frameRate=myMusicFile.getframerate()
        countFrames=myMusicFile.getnframes()


        offsetOfWindow=0
        myPeaks=[]
        myChanged = []

        while ((frameRate//10)*offsetOfWindow+frameRate) <=countFrames:
            unpackedFrames = unpackFrames(myMusicFile, channels, frameRate,(frameRate//10)*offsetOfWindow)

            unpacked =unpackedFrames
            amplit=[]
            myActualPeaks=[]
            clustered =[]
            cluster = []

            fourier= np.fft.rfft(unpacked)

            for c in fourier:
                amplit.append(np.abs(c))

            avg=sum(amplit)/len(amplit)

            for i, oneApmpli in enumerate(amplit):
                if oneApmpli >= 20*avg:
                    myActualPeaks.append((i,oneApmpli))

            for i in range(len(myActualPeaks)):
                if i == len(myActualPeaks)-1 or (myActualPeaks[i][0] + 1 != myActualPeaks[i+1][0]) :
                    cluster.append(myActualPeaks[i])
                    clustered.append(max(cluster, key=lambda y:y[1]))
                    cluster = []
                elif myActualPeaks[i+1][0]== myActualPeaks[i][0] + 1:
                    cluster.append(myActualPeaks[i])
                else:
                    clustered.append(max(cluster.append(myActualPeaks[i]), key=lambda y: y[1]))
                    cluster = []

            sortedCluster= list(filter(lambda a: a[0] != 0, clustered))
            sortedCluster.sort(key=lambda y: y[1])
            countOfSorted=len(sortedCluster)
            if  3 < countOfSorted:
                clusters=sortedCluster[-3:]
                clusters.sort(key=lambda x: x[0])
                myPeaks.append([freq[0] for freq in  clusters ])
            else:
                clusters=sortedCluster
                clusters.sort(key=lambda x: x[0])
                myPeaks.append([freq[0] for freq in clusters ])
            offsetOfWindow = offsetOfWindow + 1

        countOfPeaks=len(myPeaks)
        for i in range(countOfPeaks):
            helper=[]
            for myPeak in myPeaks[i]:
                tone = ""
                C0 = myReferenceNumber * pow(2, -4.75)
                name = ["c", "cis", "d", "es", "e", "f",
                        "fis", "g", "gis", "a", "bes", "b"]
                cap_name = ["C", "Cis", "D", "Es", "E",
                            "F", "Fis", "G", "Gis", "A", "Bes", "B"]
                h = round(12 * np.log2(myPeak / C0))
                h=int(h)
                octave = int(h // 12)
                n = int(h % 12)
                a = pow(2, 1 / 12)
                c = 1200 * np.log2(myPeak / (myReferenceNumber * pow(a, h - 57)))
                if octave < 3:
                    tone += cap_name[n] + (2 - octave) * ","
                else:
                    tone += name[n] + (octave - 3) * "'"
                c = round(c)
                if c >= 0:
                    tone += "+"
                tone += str(int(c)) + " "

                helper.append(tone)
            myChanged.append(helper)

        lenghtMyChanged=len(myChanged)
        i=0
        if not all(len(change) == 0 for change in myChanged):
            for j in range(0,lenghtMyChanged):
                start = "{:04.1f}".format(i * 0.1)
                end = ""
                vocals=map(str, myChanged[j])

                if j == lenghtMyChanged-1 and len(myChanged[j]) !=0:
                    end=  "{:04.1f}".format(j*0.1 + 0.1)
                    if len(myChanged[j]) != 0:
                        print((start + "-" + end + " " + "".join(vocals))[:-1])
                elif j == 0 and myChanged[j + 1] != myChanged[j] and len(myChanged[j]) != 0:
                    end = "{:04.1f}".format(0.1)
                    if len(myChanged[j]) != 0:
                        print((start + "-" + end + " " + "".join(vocals))[:-1])
                    i = j + 1
                elif  myChanged[j+1] != myChanged[j] and len(myChanged[j]) !=0:
                    end = "{:04.1f}".format(j * 0.1 + 0.1)
                    if len(myChanged[j]) != 0:
                        print((start + "-" + end + " " + "".join(vocals))[:-1])
                    i = j + 1





if __name__ == '__main__':
    main()