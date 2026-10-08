import { isAbsolute } from 'node:path';

/** 本地剪辑进程的最小环境；不继承宿主凭据、代理密码或解释器注入变量。 */
export function childEnvironment(source: NodeJS.ProcessEnv = process.env): NodeJS.ProcessEnv {
  const result: NodeJS.ProcessEnv = {};
  for (const key of ['PATH', 'HOME', 'TMPDIR', 'LANG', 'LC_ALL', 'LC_CTYPE']) {
    if (typeof source[key] === 'string') { result[key] = source[key]; }
  }
  // 模型目录是已有显式路径配置；不接受任意 FILMCRAFT_* 扩展环境。
  const data = source.FILMCRAFT_DATA_DIR;
  if (typeof data === 'string' && isAbsolute(data) && !/[\u0000-\u001f]/u.test(data)) {
    result.FILMCRAFT_DATA_DIR = data;
  }
  return result;
}
