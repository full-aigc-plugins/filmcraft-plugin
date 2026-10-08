import { createHash } from 'node:crypto';

/** 领域错误保留稳定代码；不把状态缺失解释成成功。 */
export class HarnessError extends Error {
  code: string;
  constructor(code: string, detail = '') {
    super(code + (detail ? ': ' + detail : '')); this.name = 'HarnessError'; this.code = code;
  }
}
export function check(condition: unknown, code: string, detail = ''): asserts condition {
  if (!condition) { throw new HarnessError(code, detail); }
}
export function sha256(bytes: string | Uint8Array): string {
  return createHash('sha256').update(bytes).digest('hex');
}
export function isHash(value: unknown): value is string {
  return typeof value === 'string' && /^[a-f0-9]{64}$/.test(value);
}
export function isObject(value: unknown): value is Record<string, any> {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}
/** 只规范化已验证的身份对象；原生回执原字节另存，避免重写大整数。 */
export function stableJson(value: unknown): string {
  function sort(item: any): any {
    if (item === null || typeof item === 'string' || typeof item === 'boolean') { return item; }
    if (typeof item === 'number') {
      check(Number.isFinite(item) && (!Number.isInteger(item) || Number.isSafeInteger(item)), 'unsafe_json_number');
      return item;
    }
    if (Array.isArray(item)) { return item.map(sort); }
    check(isObject(item), 'invalid_json_value');
    const result = Object.create(null);
    for (const key of Object.keys(item).sort()) { result[key] = sort(item[key]); }
    return result;
  }
  return JSON.stringify(sort(value));
}

/** 严格解析单个 JSON；拒绝重复键，原生非安全整数以原文字符串投影。 */
export function parseJson(text: string): any {
  check(Buffer.byteLength(text) <= 16 * 1024 * 1024, 'json_too_large');
  let position = 0, entries = 0;
  function whitespace() { while (/[\x20\x09\x0a\x0d]/.test(text[position] ?? '\0')) { position++; } }
  function string(): string {
    const start = position++; let escaped = false;
    while (position < text.length) {
      const char = text[position++];
      check(char.charCodeAt(0) >= 32, 'invalid_json_string');
      if (!escaped && char === '"') {
        try { return JSON.parse(text.slice(start, position)); }
        catch { throw new HarnessError('invalid_json_string'); }
      }
      if (!escaped && char === '\\') { escaped = true; } else { escaped = false; }
    }
    throw new HarnessError('invalid_json_string');
  }
  function value(depth: number): any {
    check(depth <= 100 && ++entries <= 200_000, 'json_resource_limit'); whitespace();
    const char = text[position];
    if (char === '"') { return string(); }
    if (char === '{') {
      position++; whitespace(); const result = Object.create(null);
      if (text[position] === '}') { position++; return result; }
      while (true) {
        whitespace(); check(text[position] === '"', 'invalid_json_object'); const key = string();
        check(!Object.hasOwn(result, key), 'duplicate_json_key', key);
        whitespace(); check(text[position++] === ':', 'invalid_json_object'); result[key] = value(depth + 1);
        whitespace(); const end = text[position++]; if (end === '}') { return result; }
        check(end === ',', 'invalid_json_object');
      }
    }
    if (char === '[') {
      position++; whitespace(); const result = [];
      if (text[position] === ']') { position++; return result; }
      while (true) {
        result.push(value(depth + 1)); whitespace(); const end = text[position++];
        if (end === ']') { return result; } check(end === ',', 'invalid_json_array');
      }
    }
    for (const [token, result] of [['true', true], ['false', false], ['null', null]] as const) {
      if (text.startsWith(token, position)) { position += token.length; return result; }
    }
    const match = /^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?/.exec(text.slice(position));
    check(match, 'invalid_json_number'); position += match[0].length;
    const numeric = Number(match[0]);
    if (!Number.isFinite(numeric) || Number.isInteger(numeric) && !Number.isSafeInteger(numeric)) { return match[0]; }
    return numeric;
  }
  const result = value(0); whitespace(); check(position === text.length, 'invalid_json_trailing_data'); return result;
}
