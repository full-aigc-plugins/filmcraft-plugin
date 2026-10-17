import {rewriteImports} from './module-imports.mjs';
import {App,PostMessageTransport} from '@modelcontextprotocol/ext-apps';
import {startConnector} from './web-connect.mjs';
const app=new App({name:'Craft editor panel',version:'0.1.0'},{});
await app.connect(new PostMessageTransport(window.parent,window.parent));
// 使用官方支持的 WebGL 模式，使嵌入面板可稳定重绘与截图。
const panelUrl=new URL(location.href);panelUrl.searchParams.set('webgl','');history.replaceState(null,'',panelUrl);

const prefix=`ui://${panelSettings.application}/assets/`, cache=new Map();
async function asset(path){
 path=path.replace(/^\.\//,'').split('?')[0];
 if(!cache.has(path))cache.set(path,(async()=>{
  const key=encodeURIComponent(path);
  const meta=JSON.parse((await app.readServerResource({uri:prefix+'meta/'+key})).contents[0].text);
  const bytes=new Uint8Array(meta.bytes);let offset=0;
  for(let i=0;i<meta.parts;i++){
   const chunk=(await app.readServerResource({uri:prefix+'chunk/'+key+'/'+i})).contents[0];
   const data=Uint8Array.from(atob(chunk.blob),c=>c.charCodeAt(0));bytes.set(data,offset);offset+=data.length;
  }
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),b=>b.toString(16).padStart(2,'0')).join('');
  if(hash!==meta.sha256)throw Error('Editor asset checksum mismatch');
  return {bytes,mime:meta.mime};
 })());
 return cache.get(path);
}
const originalFetch=window.fetch.bind(window);
window.fetch=async(input,options)=>{
 const url=new URL(input instanceof Request?input.url:input,location.href);
 if(url.protocol==='blob:'||url.protocol==='data:')return originalFetch(input,options);
 if(url.origin!==location.origin)throw Error('External editor fetch is not supported');
 const base=new URL('.',location.href).pathname;
 const path=url.pathname.startsWith(base)?url.pathname.slice(base.length):url.pathname.replace(/^\//,'');
 try{const data=await asset(path);return new Response(data.bytes,{headers:{'Content-Type':data.mime}});}catch(e){return new Response(String(e),{status:404});}
};
const modules=new Map();
async function moduleUrl(path){
 path=new URL(path,'https://editor.invalid/').pathname.slice(1);
 if(!modules.has(path))modules.set(path,(async()=>{
  let source=new TextDecoder().decode((await asset(path)).bytes);
  source=await rewriteImports(source,async relative=>moduleUrl(new URL(relative,'https://editor.invalid/'+path).pathname.slice(1)));
  return URL.createObjectURL(new Blob([source],{type:'text/javascript'}));
 })());
 return modules.get(path);
}
window.__craftImport=async path=>import(await moduleUrl(path));
try{
 await import(URL.createObjectURL(new Blob([panelSettings.source],{type:'text/javascript'})));
 void startConnector(panelSettings.application,async(route,args)=>{
  const result=await app.callServerTool({name:'_panel_'+route,arguments:args});
  if(result.isError)throw Error(result.content?.find(c=>c.type==='text')?.text||'Panel operation failed');
  const value=result.structuredContent??JSON.parse(result.content[0].text);return value&&Object.hasOwn(value,'value')?value.value:value;
 });
}catch(e){const status=document.getElementById('status')||document.getElementById('loading')||document.body;status.textContent='Editor failed to load: '+e.message;throw e;}
