import { extname } from 'node:path';
import { isObject } from '../support/json.ts';

/** 将损失声明逐项绑定到已重新读取的清单文件；缺失历史身份保持 unknown。 */
export function exchangeLossStatus(declaration: unknown, report: unknown,
  files: Record<string, { sha256: string }>, packagedInputs: ReadonlySet<string>): 'match' | 'unknown' | 'conflict' {
  if (declaration === undefined || !Object.hasOwn(files, 'exchange-loss.json')) { return 'unknown'; }
  if (!isObject(declaration) || declaration.path !== 'exchange-loss.json'
    || declaration.sha256 !== files['exchange-loss.json'].sha256 || !isObject(report)
    || report.schema !== 'craft-exchange-loss/v1' || report.pluginId !== 'filmcraft'
    || report.acceptance !== 'technical-observations-only') { return 'conflict'; }
  function bound(value: unknown, location?: string) {
    return isObject(value) && typeof value.location === 'string'
      && (location === undefined || value.location === location)
      && Object.hasOwn(files, value.location) && value.sha256 === files[value.location].sha256;
  }
  if (!bound(report.native, 'project.fcproj') || !bound(report.inspection, 'native.json')
    || !Array.isArray(report.outputs)) { return 'conflict'; }
  const formats = new Set(['png', 'jpg', 'jpeg', 'webp', 'mp4', 'srt', 'svg', 'psd', 'pdf', 'tif']);
  const seen = new Set<string>();
  for (const output of report.outputs) {
    if (!bound(output) || seen.has(output.location) || !formats.has(output.format)
      || extname(output.location).slice(1).toLowerCase() !== output.format
      || output.role !== 'derivative' || output.nativeSubstitute !== false
      || !Array.isArray(output.changes) || !isObject(output.observations) || !Array.isArray(output.warnings)) { return 'conflict'; }
    seen.add(output.location);
    const codes = new Set<string>();
    for (const change of output.changes) {
      if (!isObject(change) || typeof change.code !== 'string' || codes.has(change.code)
        || !['lost', 'observed', 'unknown'].includes(change.status)
        || typeof change.reason !== 'string' || change.reason.trim().length === 0) { return 'conflict'; }
      codes.add(change.code);
      // 文件摘要不能证明字体或效果外观等价，格式声明不得替代视觉验收。
      if (['font-appearance', 'font-portability', 'effect-fidelity'].includes(change.code)
        && change.status !== 'unknown') { return 'conflict'; }
    }
    const required: Record<string, string> = { 'native-editing-model': 'lost' };
    if (['png', 'jpg', 'jpeg', 'webp', 'mp4'].includes(output.format)) {
      Object.assign(required, { 'editable-layers-paths-text': 'lost', 'effect-keyframe-parameters': 'lost', 'font-appearance': 'unknown' });
    }
    if (output.format === 'mp4') { Object.assign(required, { 'alpha-channel': 'lost', 'editable-timeline': 'lost' }); }
    if (output.format === 'srt') { required['subtitle-styling'] = 'lost'; }
    if (Object.entries(required).some(([code, status]) => !output.changes.some((change: any) => change.code === code && change.status === status))) { return 'conflict'; }
    if (!output.changes.some((change: any) => change.code === 'native-editing-model' && change.status === 'lost')) { return 'conflict'; }
  }
  // 每个约定导出都须有损失记录，不能通过删掉 outputs 隐藏有损交换。
  for (const name of Object.keys(files)) {
    if (formats.has(extname(name).slice(1).toLowerCase()) && !packagedInputs.has(name) && !seen.has(name)) { return 'conflict'; }
  }
  return 'match';
}
