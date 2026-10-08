import {HarnessError,isObject} from '../support/json.ts';
export type ClipTiming={reason:'ticks_require_decimal_string'|'ticks_out_of_range'|'ticks_not_exact'|'clip_out_of_range'|'invalid_clip_speed';clipIds:string[]};
/** 只公开精确十进制片段身份和封闭原因，不接收路径或任意原生异常文本。 */
export function validateClipTiming(value:unknown):ClipTiming|undefined{
 if(!isObject(value)||Object.keys(value).sort().join(',')!=='clipIds,reason'
  ||!['ticks_require_decimal_string','ticks_out_of_range','ticks_not_exact','clip_out_of_range','invalid_clip_speed'].includes(value.reason as string)
  ||!Array.isArray(value.clipIds)||value.clipIds.length===0
  ||!value.clipIds.every(id=>typeof id==='string'&&/^[1-9][0-9]{0,19}$/.test(id)&&BigInt(id)<=18446744073709551615n)){return;}
 return structuredClone(value) as ClipTiming;
}
/** 保留当前片段拒绝身份，不能提升为原生已成功执行。 */
export class ClipTimingRefusal extends HarnessError{
 clipTiming:ClipTiming;
 constructor(detail:ClipTiming){super('clip_timing_failed');this.clipTiming=detail;}
}
