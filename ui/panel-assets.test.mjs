import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtemp,mkdir,writeFile,symlink,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {panelAsset,panelHtml} from './panel-assets.mjs';
test('panel resources stay inside the packaged editor and preserve bytes',async()=>{
 const dir=await mkdtemp(join(tmpdir(),'craft-panel-'));
 try{
  await mkdir(join(dir,'editor'));await writeFile(join(dir,'editor/app.js'),'hello');await writeFile(join(dir,'outside'),'private');await symlink(join(dir,'outside'),join(dir,'editor/link'));
  const prefix='ui://craft/assets/';const meta=await panelAsset(join(dir,'editor'),prefix+'meta/app.js',prefix);assert.equal(JSON.parse(meta.contents[0].text).bytes,5);
  const chunk=await panelAsset(join(dir,'editor'),prefix+'chunk/app.js/0',prefix);assert.equal(Buffer.from(chunk.contents[0].blob,'base64').toString(),'hello');
  await assert.rejects(panelAsset(join(dir,'editor'),prefix+'meta/..%2Foutside',prefix),/outside editor/);
  await assert.rejects(panelAsset(join(dir,'editor'),prefix+'meta/link',prefix),/outside editor/);
 }finally{await rm(dir,{recursive:true});}
});
test('official startup module is wrapped without an external iframe',()=>{
 for(const code of ['import init, * as ec from "./effectcraft_web.js";','import init, { start, command } from "./lightcraft_web.js";','const wasm = await import("./filmcraft_web.js" + v);']){
  const html=panelHtml('<html><body><canvas></canvas><script type="module">'+code+'</script></body></html>','BOOT','craft');
  assert.ok(html.includes('__craftImport'));assert.ok(!html.includes('<iframe'));assert.ok(html.includes('<canvas>'));
 }
});

test('classic upstream bootstrap survives panel wrapping',()=>{
 const html=panelHtml('<body><script>window.filmcraftLoad={};</script><script type="module">const wasm=await import("./filmcraft_web.js"+v);</script></body>','BOOT','filmcraft');
 assert.ok(html.includes('<script>window.filmcraftLoad={};</script>'));
 assert.equal((html.match(/type="module"/g)||[]).length,1);
});
