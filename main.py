from timeit import repeat
import ffmpeg
import random
import os


def generate_colors(n):
    colors = []
    r = lambda: random.randint(0, 255)
    for i in range(2*n):
        colors.append('#%02X%02X%02X' % (r(), r(), r()))
    return colors


# ffmpeg -i easy.mp3 -f segment -segment_time 2  out%03d.mp3
def segmentation(n):
    os.system(f'ffmpeg -i easy.mp3 -f segment -segment_time {n}  out%01d.mp3')


def showaves(q):
    colors = generate_colors(q)
    for i in range(q):
        try:
            audio = ffmpeg.input(f'out{i}.mp3')
            (
                ffmpeg
                .input(f'out{i}.mp3')
                .filter('showwaves', s='hd720', mode='cline', r='25', scale='sqrt', colors=f'{colors.pop()}|{colors.pop}')
                .output(audio.audio, f'out{i}.mp4', pix_fmt='yuv420p')
                .overwrite_output()
                .run()
            )
        except Exception as e:
            print(e)
        with open('concat.txt', 'a') as f:
            f.write(f'file out{i}.mp4\n')


#  ffmpeg -f concat -i text.txt -c copy result.mp4    
def concat():
    os.system('ffmpeg -f concat -i concat.txt -c copy result.mp4')

def background_gif():
    os.system('ffmpeg -i result.mp4 -ignore_loop 0 -i bg.gif -filter_complex "[1:v]scale=1280:-1,crop=iw:720[bg]; \
              [0:v]scale=800:-1[fg];[bg][fg]overlay=10:10:shortest=1" -q:v 3 final.mp4')
    # try:
    #     (
    #         ffmpeg
    #         .input('result.mp4')
    #         .overlay(gif, eof_action=)
    #         .output(wave.audio, 'final.mp4')
    #         .overwrite_output()
    #         .run()
    #     )
    # except Exception as e:
    #     print(e)

# ffmpeg -i input.mp4 -ignore_loop 0 -i input.gif -filter_complex overlay=10:10:shortest=1 out.mkv


if __name__ == '__main__':
    # print('Введите как часто менять цвет волны (секунды)')
    # n = int(input())
    # segmentation(n)
    # files = os.listdir()
    # q = 0
    # for el in files:
    #     if el.startswith('out'):
    #         q += 1
    # showaves(q)
    # concat()
    # os.remove('concat.txt')
    # for el in os.listdir():
    #     if el.startswith('out'):
    #         os.remove(el)
    background_gif()