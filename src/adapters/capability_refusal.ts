import { HarnessError, isHash, isObject } from '../support/json.ts';

/** 跨进程能力拒绝的最小安全投影；不包含路径、原生文本或参数文档。 */
export type CapabilityDiagnostic = {
  schema: 'filmcraft-capability-refusal/v1'; subject: string;
  status: 'missing' | 'unknown' | 'drift' | 'mismatch'; expected: string | null; observed: string | null;
  snapshot: {mode: 'headless' | 'bridge' | null; platform: string | null; runtimeVersion: string | null;
    runtimeSha256: string | null; parametersSha256: string | null; catalogSha256: string | null};
};
/** 验证 Python 回复，额外字段和路径字符串一律不能进入公共错误。 */
export function validateCapabilityDiagnostic(value: unknown): CapabilityDiagnostic | undefined {
  const keys=(v:Record<string,unknown>,expected:string[])=>Object.keys(v).sort().join('|')===expected.sort().join('|');
  const token=(v:unknown)=>typeof v==='string'&&/^[A-Za-z0-9_.:@+\-]{1,128}$/.test(v);
  if(!isObject(value)||!keys(value,['schema','subject','status','expected','observed','snapshot'])
    ||value.schema!=='filmcraft-capability-refusal/v1'||!token(value.subject)
    ||!['missing','unknown','drift','mismatch'].includes(value.status as string)
    ||![value.expected,value.observed].every(v=>v===null||token(v))||!isObject(value.snapshot)){return;}
  const s=value.snapshot;
  if(!keys(s,['mode','platform','runtimeVersion','runtimeSha256','parametersSha256','catalogSha256'])
    ||![null,'headless','bridge'].includes(s.mode as any)
    ||![s.platform,s.runtimeVersion].every(v=>v===null||token(v))
    ||![s.runtimeSha256,s.parametersSha256,s.catalogSha256].every(v=>v===null||isHash(v))){return;}
  return structuredClone(value) as CapabilityDiagnostic;
}
/** 保留稳定拒绝码，并仅携带经过验证的可公开差异。 */
export class CapabilityRefusal extends HarnessError {
  diagnostic?: CapabilityDiagnostic;
  constructor(code:string,diagnostic:unknown){
    super(code);
    const value=validateCapabilityDiagnostic(diagnostic);
    const statuses:Record<string,string>={capability_missing:'missing',capability_unknown:'unknown',
      capability_contract_drift:'drift',capability_identity_mismatch:'mismatch'};
    if(value&&statuses[code]===value.status){this.diagnostic=value;}
  }
}
