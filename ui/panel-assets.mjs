import {readFile,realpath} from 'node:fs/promises';
import {resolve,sep,extname} from 'node:path';
import {createHash} from 'node:crypto';
const CHUNK=1024*1024;
export async function panelAsset(root, uri, prefix) {
 const tail=uri.slice(prefix.length), match=/^(meta|chunk)\/([^/]+)(?:\/(\d+))?$/.exec(tail);
 if(!uri.startsWith(prefix)||!match)throw Error('Unknown panel resource');
 const path=decodeURIComponent(match[2]), base=await realpath(root), file=await realpath(resolve(base,path));
 if(!file.startsWith(base+sep))throw Error('Asset outside editor');
 const bytes=await readFile(file);
 if(bytes.length>256*1024*1024)throw Error('Asset exceeds 256 MiB');
 if(match[1]==='meta') {
  const mime={'.js':'text/javascript','.wasm':'application/wasm','.png':'image/png','.svg':'image/svg+xml','.woff2':'font/woff2','.ttf':'font/ttf'}[extname(file)]||'application/octet-stream';
  return {contents:[{uri,mimeType:'application/json',text:JSON.stringify({bytes:bytes.length,parts:Math.ceil(bytes.length/CHUNK),sha256:createHash('sha256').update(bytes).digest('hex'),mime})}]};
 }
 const part=Number(match[3]);if(!Number.isSafeInteger(part)||part*CHUNK>=bytes.length)throw Error('Invalid asset chunk');
 return {contents:[{uri,mimeType:'application/octet-stream',blob:bytes.subarray(part*CHUNK,(part+1)*CHUNK).toString('base64')}]};
}
export function panelHtml(html, boot, application) {
 const modules=[...html.matchAll(/<script\b[^>]*type=["']module["'][^>]*>([\s\S]*?)<\/script>/gi)].map(m=>m[1]);
 if(modules.length!==1)throw Error('Unsupported upstream module layout');
 let source=modules[0];
 source=source.replace(/import\s+(\w+),\s*\*\s+as\s+(\w+)\s+from\s+["']([^"']+)["'];/g,(_,init,ns,path)=>`const ${ns}=await window.__craftImport(${JSON.stringify(path)}); const ${init}=${ns}.default;`);
 source=source.replace(/import\s+(\w+),\s*\{([^}]+)\}\s+from\s+["']([^"']+)["'];/g,(_,init,names,path)=>`const {default:${init},${names}}=await window.__craftImport(${JSON.stringify(path)});`);
 source=source.replace(/import\((["']\.\/[^"']+\.js["'])(?:\s*\+\s*\w+)?\)/g,'window.__craftImport($1)');
 // 面板没有 PWA 生命周期；不在宿主协议域注册 service worker。
 source=source.replace(/if\s*\("serviceWorker" in navigator/g,'if (false && "serviceWorker" in navigator');
 const settings=JSON.stringify({application,source}).replaceAll('<','\\u003c');
 return html.replace(/<script\b[^>]*type=["']module["'][^>]*>[\s\S]*?<\/script>/gi,'').replace(/<link\b[^>]*>/gi,'').replace('</body>',()=>`<script type="module">const panelSettings=${settings};\n${boot.replaceAll('</script','<\\/script')}</script></body>`);
}
