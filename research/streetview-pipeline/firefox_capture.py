"""Windows Firefox Street View screenshot/metadata pilot. Visible browser only.

Uses the user's existing Google Maps tab; no image endpoints, keys or tile APIs.
Screenshots retain the full map viewport and attribution. User specifically
authorised this personal reference capture; provenance does not establish a licence.
"""
from pathlib import Path
import argparse,ctypes,json,time,re,hashlib,math,sys
from ctypes import wintypes as W
from datetime import datetime,timezone
from contextlib import contextmanager
import mss,pyautogui as pg
pg.PAUSE=.035
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'references/streetview-capture/taraj-to-pharmacie'
U=ctypes.WinDLL('user32',use_last_error=True);K=ctypes.WinDLL('kernel32',use_last_error=True)
for name,args,ret in [('GetWindowTextW',[W.HWND,W.LPWSTR,ctypes.c_int],ctypes.c_int),('GetWindowRect',[W.HWND,ctypes.POINTER(W.RECT)],W.BOOL),('SetForegroundWindow',[W.HWND],W.BOOL),('ShowWindow',[W.HWND,ctypes.c_int],W.BOOL),('GetForegroundWindow',[],W.HWND),('GetClipboardData',[W.UINT],W.HANDLE),('OpenClipboard',[W.HWND],W.BOOL),('CloseClipboard',[],W.BOOL)]:
    f=getattr(U,name);f.argtypes=args;f.restype=ret
K.GlobalLock.argtypes=[W.HANDLE];K.GlobalLock.restype=W.LPVOID
K.GlobalUnlock.argtypes=[W.HANDLE];K.GlobalUnlock.restype=W.BOOL

@contextmanager
def driver_lock():
    """An OS-held lock prevents two of our desktop drivers sending inputs together."""
    import msvcrt
    BASE.mkdir(parents=True,exist_ok=True)
    with (BASE/'driver.lock').open('a+b') as handle:
        if handle.seek(0,2)==0:handle.write(b'0');handle.flush()
        handle.seek(0)
        try:msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
        except OSError:raise RuntimeError('Another capture driver is running; no inputs sent') from None
        try:yield
        finally:handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
def window():
    hs=[];cb=ctypes.WINFUNCTYPE(W.BOOL,W.HWND,W.LPARAM)(lambda h,p:hs.append(h) or True);U.EnumWindows(cb,0)
    candidates=[]
    for h in hs:
        b=ctypes.create_unicode_buffer(2048);U.GetWindowTextW(h,b,len(b))
        if 'Mozilla Firefox' in b.value and 'Google Maps' in b.value:candidates.append((h,b.value))
    if not candidates:raise RuntimeError('No Firefox Google Maps window; no input sent')
    return candidates[0]
def focus():
    h,title=window();U.ShowWindow(h,9);U.SetForegroundWindow(h);time.sleep(.07)
    if U.GetForegroundWindow()!=h:raise RuntimeError('Firefox not foreground; no input sent')
    r=W.RECT();assert U.GetWindowRect(h,ctypes.byref(r));assert r.right-r.left>600 and r.bottom-r.top>400
    return h,title,r
def clipboard_text():
    for _ in range(20):
        if U.OpenClipboard(None):break
        time.sleep(.05)
    else:raise RuntimeError('Clipboard busy')
    try:
        handle=U.GetClipboardData(13)
        if not handle:return ''
        p=K.GlobalLock(handle)
        if not p:return ''
        try:return ctypes.wstring_at(p)
        finally:K.GlobalUnlock(handle)
    finally:U.CloseClipboard()
def read_url():
    focus();pg.hotkey('ctrl','l');pg.hotkey('ctrl','c');time.sleep(.10);url=clipboard_text();pg.press('esc')
    if not re.match(r'https://(www\.)?google\.[^/]+/maps/',url):raise RuntimeError('Active tab is not Google Maps; URL withheld')
    return url
def parse_url(url):
    from urllib.parse import urlparse,parse_qs,unquote
    result={'url':url};m=re.search(r'@(-?[\d.]+),(-?[\d.]+),3a,([\d.]+)y,([\d.]+)h,([\d.]+)t',url)
    if m:
        result.update(latitude=float(m[1]),longitude=float(m[2]),fov_degrees=float(m[3]),heading_degrees=float(m[4]),url_tilt_degrees=float(m[5]),pitch_degrees=float(m[5])-90)
    else:
        m=re.search(r'@(-?[\d.]+),(-?[\d.]+)',url)
        if m:result.update(latitude=float(m[1]),longitude=float(m[2]))
    m=re.search(r'!1s([^!/?]+)',url)
    if m and ',3a,' in url:result['panorama_id']=unquote(m[1])
    q=parse_qs(urlparse(url).query)
    if 'viewpoint' in q:
        try:result['requested_latitude'],result['requested_longitude']=map(float,q['viewpoint'][0].split(','))
        except ValueError:pass
    for src,dst in [('heading','requested_heading_degrees'),('pitch','requested_pitch_degrees'),('fov','requested_fov_degrees')]:
        if src in q:result[dst]=float(q[src][0])
    if 'pano' in q:result['requested_panorama_id']=q['pano'][0]
    result['position_semantics']='URL Street View viewpoint; not a surveyed building position' if ',3a,' in url or 'map_action=pano' in url else 'Map viewport centre; not necessarily the selected place pin'
    place=re.search(r'!3d(-?[\d.]+)!4d(-?[\d.]+)',url)
    if place:result['place_latitude']=float(place[1]);result['place_longitude']=float(place[2])
    return result
def grab():
    h,title,r=focus()
    # Preserve map overlays, date/address panel, compass and all bottom attribution.
    top=r.top+112;left=r.left+8;right=r.right-8;bottom=r.bottom-8
    with mss.mss() as g:
        s=g.grab({'left':left,'top':top,'width':right-left,'height':bottom-top})
        im=Image.frombytes('RGB',s.size,s.rgb)
    return im,title,{'left':left,'top':top,'width':right-left,'height':bottom-top}
def navigate(url,delay=3):
    assert url.startswith('https://www.google.com/maps/')
    focus();pg.hotkey('ctrl','l');pg.write(url,interval=.001);pg.press('enter');time.sleep(delay)
def capture(label,notes='',stop='',role='',capture_date=None,expected_panorama=None):
    BASE.mkdir(parents=True,exist_ok=True);(BASE/'originals').mkdir(exist_ok=True)
    url=read_url();meta=parse_url(url)
    if expected_panorama and meta.get('panorama_id')!=expected_panorama:raise RuntimeError('Panorama changed before screenshot; stop rather than mislabel')
    time.sleep(.2);im,title,rect=grab()
    records=BASE/'manifest.jsonl';count=sum(1 for _ in records.open(encoding='utf8')) if records.exists() else 0
    ident=f'{count+1:05d}';slug=re.sub('[^a-z0-9_-]+','-',label.lower()).strip('-')[:80]
    file=BASE/'originals'/f'{ident}__{slug}.png';assert not file.exists();im.save(file)
    record={'id':ident,'file':str(file.relative_to(ROOT)).replace('\\','/'),'captured_utc':datetime.now(timezone.utc).isoformat(),'window_title':title,'label':label,'stop':stop,'role':role,'notes':notes,'metadata':meta,'dimensions':list(im.size),'screen_region':rect,'sha256':hashlib.sha256(file.read_bytes()).hexdigest(),'source':'Google Street View, visible Firefox viewport screenshot','rights_status':'Personal reference requested by user; Google restrictions researched, licence not established','image_edits':'Window viewport capture only; no resampling/crop/retouch of saved original','image_capture_date_observed':capture_date,'review_status':'unreviewed'}
    with records.open('a',encoding='utf8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(json.dumps({'id':ident,'file':record['file'],'latitude':meta.get('latitude',meta.get('requested_latitude')),'longitude':meta.get('longitude',meta.get('requested_longitude')),'heading':meta.get('heading_degrees',meta.get('requested_heading_degrees')),'pano':meta.get('panorama_id',meta.get('requested_panorama_id')),'title':title}),flush=True)
    return record
def drag(dx,dy):
    h,title,r=focus();x=r.left+(r.right-r.left)*.55;y=r.top+(r.bottom-r.top)*.55
    pg.moveTo(x,y);pg.dragRel(dx,dy,duration=.45,button='left');time.sleep(.6)
def pilot_batch(stop,heading_step=30,start_heading=0):
    before=parse_url(read_url());lat=before.get('latitude');lon=before.get('longitude');pano=before.get('panorama_id')
    if lat is None or lon is None:raise RuntimeError('No resolved Street View coordinates in URL')
    for heading in range(start_heading,360,heading_step):
        url=f'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}&heading={heading}&pitch=8&fov=75'
        if pano:url+='&pano='+pano
        navigate(url,3.5);capture(f'{stop}-heading-{heading:03d}',stop=stop,role='panorama-surroundings',notes='Planned heading sweep; verify resolved viewpoint and loading in contact sheet')
def check_gallery():
    """Verify our local gallery in a temporary tab; return to Maps afterwards."""
    h,title,r=focus();pg.hotkey('ctrl','t');pg.write((BASE/'index.html').as_uri(),interval=.001);pg.press('enter');time.sleep(3)
    if U.GetForegroundWindow()!=h:raise RuntimeError('Firefox lost focus before gallery verification')
    pg.hotkey('ctrl','shift','k');time.sleep(2)
    code="(()=>{const s=document.querySelector('#search'),v=document.querySelector('#roles');s.value='route-010';s.dispatchEvent(new Event('input'));const searchCount=document.querySelectorAll('article').length;v.value='left-frontage';v.dispatchEvent(new Event('change'));const filteredCount=document.querySelectorAll('article').length;const matching=[...document.querySelectorAll('.tag')].every(e=>e.textContent.includes('left-frontage'));s.value='';v.value='';s.dispatchEvent(new Event('input'));copy(JSON.stringify({images:records.length,searchCount,filteredCount,matching,labelFields:document.querySelectorAll('[data-field=label]').length,exportHandler:typeof document.querySelector('#save').onclick}));})()"
    pg.write(code,interval=.001);pg.press('enter');time.sleep(2)
    result=json.loads(clipboard_text())
    assert result['searchCount']>=12 and result['filteredCount']>=1 and result['matching']
    assert result['labelFields']==result['images'] and result['exportHandler']=='function'
    pg.hotkey('ctrl','shift','k');time.sleep(1)
    with mss.mss() as g:
        shot=g.grab({'left':r.left+8,'top':r.top+112,'width':r.right-r.left-16,'height':r.bottom-r.top-120})
        Image.frombytes('RGB',shot.size,shot.rgb).save(BASE/'gallery-ui-check.png')
    (BASE/'gallery-ui-check.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    pg.hotkey('ctrl','w');time.sleep(.5);print(json.dumps(result))
def main():
    p=argparse.ArgumentParser();p.add_argument('action',choices=['status','capture','navigate','drag','click','key','sweep','gallery-check','viewport-check']);p.add_argument('--label',default='street-view');p.add_argument('--notes',default='');p.add_argument('--stop',default='');p.add_argument('--role',default='');p.add_argument('--date');p.add_argument('--url');p.add_argument('--dx',type=int,default=0);p.add_argument('--dy',type=int,default=0);p.add_argument('--x',type=float,default=.5);p.add_argument('--y',type=float,default=.7);p.add_argument('--key',default='up');p.add_argument('--step',type=int,default=45);p.add_argument('--wait',type=float,default=3.5);a=p.parse_args()
    if a.action=='status':print(json.dumps(parse_url(read_url())))
    elif a.action=='capture':capture(a.label,a.notes,a.stop,a.role,a.date)
    elif a.action=='navigate':navigate(a.url,a.wait);print(json.dumps(parse_url(read_url())))
    elif a.action=='drag':drag(a.dx,a.dy);print(json.dumps(parse_url(read_url())))
    elif a.action=='click':
        h,t,r=focus();pg.click(r.left+(r.right-r.left)*a.x,r.top+(r.bottom-r.top)*a.y);time.sleep(a.wait);print(json.dumps(parse_url(read_url())))
    elif a.action=='key':
        assert a.key in ('up','down','left','right','+','-');h,t,r=focus();pg.click(r.left+(r.right-r.left)*.6,r.top+(r.bottom-r.top)*.35);pg.press(a.key);time.sleep(a.wait);print(json.dumps(parse_url(read_url())))
    elif a.action=='sweep':pilot_batch(a.stop or a.label,a.step)
    elif a.action=='gallery-check':check_gallery()
    elif a.action=='viewport-check':
        im,title,rect=grab();im.save(BASE/'viewport-check.png');print(json.dumps({'title':title,'file':str(BASE/'viewport-check.png')}))
if __name__=='__main__':
    with driver_lock():main()
