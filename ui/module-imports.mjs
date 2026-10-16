// 只重写 ESM 依赖；WASM import-object 的同名字串必须原样保留。
export async function rewriteImports(source, resolve) {
 const imports=[...source.matchAll(/(?:from\s*|import\s*)["'](\.[^"']+)["']/g)];
 for(const match of imports){
  const url=await resolve(match[1]);
  source=source.replace(match[0],match[0].replace(match[1],url));
 }
 return source;
}
