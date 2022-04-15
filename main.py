from email.mime import audio
import ffmpeg

audio= ffmpeg.input('easy.mp3')

(
    ffmpeg
    .input('easy.mp3')
    .filter('showwaves', s='hd720', mode='cline', r='25', scale='sqrt', colors='#000080|#006400')
    .output(audio.audio, 'out.mp4', pix_fmt='yuv420p')
    .overwrite_output()
    .run()
)

