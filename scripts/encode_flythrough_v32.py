from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[1];dest=ROOT/'recon/v32';frames=ROOT/'build/v32-flythrough-frames';meta=json.loads((dest/'flythrough.json').read_text())
assert all((frames/f'{i:05d}.png').exists() for i in range(meta['frames']))
subprocess.run(['C:/ffmpeg/ffmpeg.exe','-hide_banner','-loglevel','error','-y','-framerate','24','-i',str(frames/'%05d.png'),'-c:v','libvpx-vp9','-b:v','1100k','-crf','32','-row-mt','1','-deadline','good','-cpu-used','4','-pix_fmt','yuv420p','-an',str(dest/'general-flythrough.webm')],check=True)
probe=json.loads(subprocess.check_output(['C:/ffmpeg/ffprobe.exe','-v','error','-show_format','-show_streams','-of','json',str(dest/'general-flythrough.webm')]))
s=next(s for s in probe['streams'] if s['codec_type']=='video');assert (s['width'],s['height'],s['r_frame_rate'])==(1280,720,'24/1');assert abs(float(probe['format']['duration'])-28)<.1
meta['bytes']=(dest/'general-flythrough.webm').stat().st_size;(dest/'flythrough.json').write_text(json.dumps(meta,indent=2));print('FLY_ENCODE_COMPLETE',meta['bytes'])
