import subprocess, json, os
EP='/home/claude/tempo-assets/episodes/briefai-13'; S='/home/claude/b13/seg'; OUT='/home/claude/tempo-assets/pub/b13'; os.makedirs(OUT,exist_ok=True)
segs=['a1']+[f'v{k}' for k in range(1,9)]+['a2']
open('/home/claude/b13/list.txt','w').write(''.join(f"file '{S}/{s}.mp4'\n" for s in segs))
subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i','/home/claude/b13/list.txt','-c','copy','/home/claude/b13/video.mp4'],check=True)
# audio : voix Vids + musique maison très basse, puis -14 LUFS
subprocess.run(['ffmpeg','-loglevel','error','-y','-i',EP+'/vids/vids_export.mp4','-stream_loop','-1','-i','/home/claude/tempo-assets/episodes/briefai-01/music.mp3',
 '-filter_complex','[0:a]aresample=48000,volume=1.0[v];[1:a]aresample=48000,volume=0.10[m];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]',
 '-map','[a]','-c:a','aac','-b:a','192k','/home/claude/b13/audio.m4a'],check=True)
subprocess.run(['ffmpeg','-loglevel','error','-y','-i','/home/claude/b13/video.mp4','-i','/home/claude/b13/audio.m4a','-map','0:v','-map','1:a','-c:v','copy','-c:a','copy','-shortest',OUT+'/b13_demo.mp4'],check=True)
print(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',OUT+'/b13_demo.mp4']).decode())
