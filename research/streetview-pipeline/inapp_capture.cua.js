// Run in cua_repl after binding surveyTab with cua.getTab and reading browser docs.
// Uses visible Google Maps pages only; no hidden imagery APIs or browser internals.
var captureFs = await import('node:fs/promises');
var surveyCrypto = await import('node:crypto');
var surveyDir = 'C:/Users/sam/pharmacie-cod-map/references/streetview-capture/authored-route-2026-10-11';
var surveyRoute = JSON.parse(await captureFs.readFile(surveyDir+'/route.json','utf8'));
var surveyLedger = JSON.parse(await captureFs.readFile(surveyDir+'/ledger.json','utf8'));
async function captureSurveyView(i,v,revision='r2') {
  const stop=surveyRoute.observation_stops[i],view=stop.views[v];
  const file=stop.id+'-'+['ahead','right','back','left'][v]+'-'+revision+'.jpg';
  if(surveyLedger.some(e=>e.file===file))return;
  await surveyTab.goto(view.url);
  await surveyTab.getAXState({emit:false});
  let loadError=null;
  try {
    await surveyTab.playwright.waitForURL('**/maps/@52.**',{timeoutMs:8000});
    await surveyTab.playwright.getByRole('button',{name:'Show location on map',exact:true}).waitFor({state:'visible',timeoutMs:8000});
  } catch(e) {loadError=String(e).slice(0,400);}
  const ax=await surveyTab.getAXState({emit:false});
  const dom=await surveyTab.playwright.domSnapshot();
  const jpg=await surveyTab.screenshot({fullPage:false});
  const actual=String(ax).match(/URL: "([^"]+)"/)?.[1]||await surveyTab.url();
  await captureFs.writeFile(surveyDir+'/'+file,jpg,{flag:'wx'});
  const entry={stop_id:stop.id,stop_index:i,view_index:v,requested:view,
    requested_position:stop.position,chainage_m:stop.chainage_m,actual_url:actual,
    title:await surveyTab.title(),file,sha256:surveyCrypto.createHash('sha256').update(jpg).digest('hex'),
    dom,ax,loadError,captured_utc:new Date().toISOString(),visual_review:'pending'};
  surveyLedger.push(entry);
  await captureFs.writeFile(surveyDir+'/ledger.json',JSON.stringify(surveyLedger,null,2));
  return entry;
}
// Use at most three stops (12 views) per call, keeping calls under 60 seconds.
// Each image is immutable. Retry failures with revision r3, r4, etc.
// Native Tab.url() may lag; the accessibility header records the resolved URL.
// A resolved URL/control is insufficient proof: inspect contact sheets and retry black views.
