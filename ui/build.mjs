import {build} from 'esbuild';
import {mkdir,copyFile} from 'node:fs/promises';
await mkdir('dist',{recursive:true});
await build({entryPoints:['web-adapter.mjs'],outfile:'dist/adapter.mjs',bundle:true,platform:'node',format:'esm',target:'node24',banner:{js:'import {createRequire as __createRequire} from "node:module"; const require=__createRequire(import.meta.url);'},legalComments:'linked'});
await build({entryPoints:['web-panel.mjs'],outfile:'dist/web-panel.js',bundle:true,platform:'browser',format:'esm',target:'chrome120',legalComments:'linked'});
await build({entryPoints:['web-connect.mjs'],outfile:'dist/web-connect.js',bundle:true,platform:'browser',format:'esm',target:'chrome120',legalComments:'linked'});
await copyFile('editor.lock.json','dist/config.json');
