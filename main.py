import ffmpeg
import random
import os


# function creating different colors for audiowave in HEX format
# arg - quantity of parts
def generate_colors(q):
    colors = []
    r = lambda: random.randint(0, 255)
    for i in range(2*q):
        colors.append('#%02X%02X%02X' % (r(), r(), r()))
    return colors


# ffmpeg command for division audio file in parts
# (duration - specified N seconds)
def segmentation(n, file_name):
    os.system(f'ffmpeg -i {file_name} -f segment -segment_time {n}  out%01d.mp3')


# ffmpeg-python script converting audio in audiowaves mp4 with different colors
def showaves(q):
    colors = generate_colors(q)
    for i in range(q):
        try:
            audio = ffmpeg.input(f'out{i}.mp3')
            (
                ffmpeg
                .input(f'out{i}.mp3')
                .filter(
                    'showwaves', s='hd720', mode='cline', r='25',
                    scale='sqrt', colors=f'{colors.pop()}|{colors.pop}')
                .output(audio.audio, f'out{i}.mp4', pix_fmt='yuv420p')
                .overwrite_output()
                .run()
            )
        except Exception as e:
            print(e)
        with open('concat.txt', 'a') as f:
            f.write(f'file out{i}.mp4\n')


#  ffmpeg command to union all mp4 files in one
def concat():
    os.system('ffmpeg -f concat -i concat.txt -c copy result.mp4')


# ffmpeg command to set gif file as a background
def background_gif():
    os.system('ffmpeg -i result.mp4 -ignore_loop 0 -i bg.gif -filter_complex "[1:v]scale=1280:-1,crop=iw:720[bg]; \
              [0:v]scale=800:-1[fg];[bg][fg]overlay=240:125:shortest=1" -q:v 3 final.mp4')


if __name__ == '__main__':
    print('Введите как часто менять цвет волны (секунды)')
    n = int(input())
    print('Введите название исходного аудио файла (как пример - test.mp3)')
    file_name = input()
    segmentation(n, file_name)
    files = os.listdir()
    q = 0
    for el in files:
        if el.startswith('out'):
            q += 1
    showaves(q)
    concat()
    os.remove('concat.txt')
    for el in os.listdir():
        if el.startswith('out'):
            os.remove(el)
    background_gif()
