"""Capture visible satellite overview in a separate manifest, preserving old walk."""
from pathlib import Path
import json,time,hashlib
from datetime import datetime,timezone
import firefox_capture as F
import ctypes
from ctypes import wintypes as W
root=F.ROOT;dest=root/'references/streetview-capture/syston-overhead-v28';dest.mkdir(exist_ok=True)
def firefox_window():
    hs=[];cb=ctypes.WINFUNCTYPE(W.BOOL,W.HWND,W.LPARAM)(lambda h,p:hs.append(h) or True);F.U.EnumWindows(cb,0)
    rows=[]
    for h in hs:
        b=ctypes.create_unicode_buffer(2048);F.U.GetWindowTextW(h,b,len(b))
        if 'Mozilla Firefox' in b.value:rows.append((h,b.value))
    if not rows:raise RuntimeError('No Firefox window')
    return next((r for r in rows if r[0]==F.U.GetForegroundWindow()),rows[0])
F.window=firefox_window
with F.driver_lock():
    h,title,r=F.focus();print('Firefox title:',title,flush=True)
    import subprocess
    subprocess.run(['powershell','-NoProfile','-Command',"Set-Clipboard -Value 'https://www.google.com/maps/@52.69918,-1.07310,110m/data=!3m1!1e3'"],check=True)
    F.pg.hotkey('ctrl','l');time.sleep(.4);F.pg.hotkey('ctrl','v');time.sleep(.3);F.pg.press('enter');time.sleep(8)
    url=F.read_url();time.sleep(2);im,title,rect=F.grab()
    file=dest/'01-junction-satellite.png';assert not file.exists();im.save(file)
    (dest/'manifest.json').write_text(json.dumps({'file':str(file.relative_to(root)),'url':url,'visible_title':title,'captured_utc':datetime.now(timezone.utc).isoformat(),'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'dimensions':list(im.size),'source':'Visible Firefox Google Maps satellite view','edits':'None; full map viewport with attribution','limits':'Map centre is not surveyed position; imagery date only if visible; reference only'},indent=2)+'\n')
    print(file)
