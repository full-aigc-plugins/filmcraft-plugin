import {test} from 'node:test';
import assert from 'node:assert/strict';
import {rewriteImports} from './module-imports.mjs';
test('ESM URL conversion preserves the WASM import-object keys',async()=>{
 const source=`import * as host from './snippets/host.js';\nconst imports={'./snippets/host.js':host};`;
 const output=await rewriteImports(source,async()=> 'blob:module');
 assert.match(output,/from 'blob:module'/);
 assert.match(output,/'\.\/snippets\/host.js':host/);
});
