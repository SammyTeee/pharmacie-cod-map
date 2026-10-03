"""Verify local catalogue/gallery in our own headless Chrome profile, not Firefox."""
from pathlib import Path
import json,subprocess,time,urllib.request,base64
import websocket
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'build/street-catalogue-check';OUT.mkdir(parents=True,exist_ok=True)
def run():
    profile=OUT/f'chrome-profile-{time.time_ns()}';profile.mkdir()
    log=(OUT/'chrome.log').open('w')
    proc=subprocess.Popen([r'C:\Program Files\Google\Chrome\Application\chrome.exe','--headless=new','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--remote-allow-origins=http://localhost',f'--user-data-dir={profile}','about:blank'],stdout=log,stderr=log,creationflags=subprocess.CREATE_NO_WINDOW)
    ws=None
    try:
        port_file=profile/'DevToolsActivePort'
        for _ in range(60):
            if port_file.exists():break
            time.sleep(.25)
        port=int(port_file.read_text().splitlines()[0])
        targets=json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list'))
        target=next(t for t in targets if t['type']=='page')
        ws=websocket.create_connection(target['webSocketDebuggerUrl'],origin='http://localhost',timeout=15)
        serial=0
        def call(method,params={}):
            nonlocal serial
            serial+=1;ws.send(json.dumps({'id':serial,'method':method,'params':params}))
            while True:
                result=json.loads(ws.recv())
                if result.get('id')==serial:
                    assert 'error' not in result,result
                    return result.get('result',{})
        def evaluate(code):
            result=call('Runtime.evaluate',{'expression':code,'returnByValue':True,'awaitPromise':True})
            assert 'exceptionDetails' not in result,result
            return result['result'].get('value')
        call('Page.enable');call('Emulation.setDeviceMetricsOverride',{'width':1500,'height':1100,'deviceScaleFactor':1,'mobile':False})
        def navigate(path):
            call('Page.navigate',{'url':path.as_uri()})
            for _ in range(40):
                if evaluate('document.readyState')=='complete':break
                time.sleep(.2)
            time.sleep(.3)
        def screenshot(name):
            result=call('Page.captureScreenshot',{'format':'png','captureBeyondViewport':False})
            (OUT/name).write_bytes(base64.b64decode(result['data']))
        navigate(ROOT/'docs/street-catalogue/index.html')
        map_result=evaluate("(()=>{const total=document.querySelectorAll('.card').length;s=document.querySelector('#search');s.value='B001';s.dispatchEvent(new Event('input'));const search=document.querySelectorAll('.card').length;const taraj=document.querySelector('.card').textContent.includes('Taraj');s.value='';const k=document.querySelector('#kind');k.value='street-feature';k.dispatchEvent(new Event('change'));const features=document.querySelectorAll('.card').length;k.value='';k.dispatchEvent(new Event('change'));const svg=document.querySelector('svg'),old=svg.getAttribute('viewBox');svg.dispatchEvent(new WheelEvent('wheel',{deltaY:-100,clientX:500,clientY:500,cancelable:true}));const zoom=old!==svg.getAttribute('viewBox');document.querySelector('#reset').click();const reset=JSON.stringify(old.split(' ').map(Number))===JSON.stringify(svg.getAttribute('viewBox').split(' ').map(Number));return {total,search,taraj,features,zoom,reset,markers:svg.querySelectorAll('[data-id]').length};})()")
        assert map_result=={'total':68,'search':1,'taraj':True,'features':17,'zoom':True,'reset':True,'markers':68},map_result
        screenshot('numbered-map.png')
        navigate(ROOT/'docs/street-catalogue/entries/B010.html')
        dossier=evaluate("({title:document.querySelector('h1').textContent,images:document.images.length,broken:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).length})")
        assert 'Newton Fallowell' in dossier['title'] and dossier['images']==4 and dossier['broken']==0,dossier
        screenshot('individual-dossier.png')
        navigate(ROOT/'references/streetview-capture/taraj-to-pharmacie/index.html')
        gallery=evaluate("(async()=>{const total=document.querySelectorAll('article').length,s=document.querySelector('#search'),v=document.querySelector('#roles');s.value='route-010';s.dispatchEvent(new Event('input'));const searched=document.querySelectorAll('article').length;v.value='left-frontage-detail';v.dispatchEvent(new Event('change'));const filtered=document.querySelectorAll('article').length;s.value='';v.value='';s.dispatchEvent(new Event('input'));const input=document.querySelector('[data-field=label]');const id=input.dataset.id;input.value='temporary-ui-check';input.dispatchEvent(new Event('input',{bubbles:true}));draw();const persisted=document.querySelector('[data-field=label]').value==='temporary-ui-check';let content;const create=URL.createObjectURL,click=HTMLAnchorElement.prototype.click;URL.createObjectURL=b=>{content=b.text();return create(b)};HTMLAnchorElement.prototype.click=()=>{};document.querySelector('#save').click();const exported=JSON.parse(await content);URL.createObjectURL=create;HTMLAnchorElement.prototype.click=click;const exportWorks=exported[id].label==='temporary-ui-check';return {total,searched,filtered,persisted,exportWorks};})()")
        assert gallery['total']==296 and gallery['searched']>=12 and gallery['filtered']==1 and gallery['persisted'] and gallery['exportWorks'],gallery
        screenshot('label-gallery.png')
        result={'map':map_result,'dossier':dossier,'gallery':gallery,'isolated_profile':str(profile),'firefox_inputs_sent':False}
        (OUT/'ui-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
    finally:
        if ws:ws.close()
        proc.terminate()
        try:proc.wait(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)
        log.close()
if __name__=='__main__':run()
