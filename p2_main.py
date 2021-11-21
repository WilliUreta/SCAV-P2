import os
import subprocess

def cut_n_seconds(path,seconds, output_name):

    #os.system()
    subprocess.call(["ffmpeg", "-i", path, "-t", str(seconds),
                    "-c:v", "copy", "-c:a", "copy", output_name])

# ffmpeg -i BBB.mp4 -ss 20 -t 10 -c:v copy -c:a copy cut_BBB.mp4
# obre el video bbb, desde segon 20, durant10s, mateix videocodec


def extract_yuv(path, output_name):

    # https://trac.ffmpeg.org/wiki/Histogram
    # https://ffmpeg.org/ffmpeg-filters.html#scale-1
    # ffplay video -vf histogram
    # ffplay video -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay"
    # ffmpeg -i cut_BBB.mp4 -vf "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" yuv_cut_BBB.mp4

    # -vf video fileter. stream a i b. el b, fes histograma de yuva444. hh es un mapeig. al a fes overlay de a i hh (b)
    subprocess.call(["ffmpeg", "-i", path, "-vf",
                     "split=2[a][b],[b]histogram,format=yuva444p[hh],[a][hh]overlay" ,
                     output_name])

def resize_vid(path, output_size):

    if output_size==1:
        actual_size = str("scale=720:480")
        output_name = "720_480_"+os.path.basename(path)
    elif output_size==2:
        actual_size = str("scale=480:360")
        output_name = "480_360_" + os.path.basename(path)
    elif output_size == 3:
        actual_size = str("scale=360:240")
        output_name = "360_240_" + os.path.basename(path)
    elif output_size == 4:
        actual_size = str("scale=160:120")
        output_name = "160_120_" + os.path.basename(path)
    else:
        print("No  valid resolution")
        return

    subprocess.call(["ffmpeg", "-i", path, "-vf", actual_size, output_name])

def change_audio(path, mono, codec, output):

    # Mono-Stereo Part
    if mono == 1: mono_param = "1"  #-ac 1      No va????
    else:
        mono_param = "2" # test it!!!
        print("Audio kept at stereo")

    # Codec part
    if codec == 0:
        codec_param = "copy" #-c:a copy
    elif codec == 1:
        codec_param = "aac"   #-c:a aac AAC. aac o libfdk_aac
    elif codec == 2:    #vorbis no va!!
        codec_param = "libvorbis" # -c:a vorbis ogg bitrate amb -b:a 192k
    elif codec == 3:    #mp3 no va!!! no built
        codec_param = "libmp3lame" # -c:a mp3bitrate amb -b:a 192k
    else:
        print("No valid codec!")
        return

    # ffmpeg -i trimmed_vid.mp4 -t 5 -ac 1 -c:a copy test_copy.mp4  #-t 5 temporal
    subprocess.call(["ffmpeg", "-i", path, "-ac", mono_param, "-c:a",
                     codec_param, output_name])


if __name__ == '__main__':

    program = int(input("Choose what program to run: \n1. Cut video"
                        "\n2. Overlay YUV histogram \n3. Resize"
                        "\n4. Change audio\n"))

    if program ==1:
        path = input("Enter path to video file you want to cut: ")
        seconds = int(input("Length in seconds of video: "))
        output_name = input("Name of output file: ")
        cut_n_seconds(path, seconds, output_name)
    elif program==2:
        path = input("Enter path to video file you want a yuv overlay: ")
        output_name = input("Name of output file: ")
        extract_yuv(path,output_name)
    elif program==3:
        path = input("Enter path to video file you want to resize: ")
        output_size = int(input("Choose output resolution:\n1. 720p\n2. 480p"
                                "\n3. 360x240 \n4. 160x120 \n"))
        #output_name = input("Name of output file, can be a full path: ")
        #output name sera name original precedit de resolucio

        resize_vid(path, output_size)

    elif program==4:
        path = input("Enter path to video file you want to change audio: ")
        mono = int(input("Do you want audio in: \n1. Mono \n2. Stereo\n"))
        codec = int(input("What codec do you want: \n0. The same as original"
                          "\n1. aac \n2. Vorbis \n3. mp3\n"))
        output_name = input("Name of output file: ")
        change_audio(path,mono,codec,output_name)
    else:
        print("Program not valid")
