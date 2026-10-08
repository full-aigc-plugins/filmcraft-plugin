import {HarnessError,isObject} from '../support/json.ts';
export type AssetIssue={alias:string;origin:'plan'|'source';reason:'missing_file'|'digest_mismatch'|'invalid_path'};
/** 清单只包含素材别名与固定原因；拒绝任意路径、扩展字段和畸形诊断。 */
export function validateAssetIssues(value:unknown):AssetIssue[]|undefined{
 if(!Array.isArray(value)||value.length===0){return;}
 if(!value.every(row=>isObject(row)&&Object.keys(row).sort().join(',')==='alias,origin,reason'
  &&typeof row.alias==='string'&&/^[a-zA-Z][\p{L}\p{N}_-]*$/u.test(row.alias)
  &&['plan','source'].includes(row.origin as string)&&['missing_file','digest_mismatch','invalid_path'].includes(row.reason as string))){return;}
 return structuredClone(value) as AssetIssue[];
}
/** 保留安装前拒绝状态，并向宿主公开完整、已验证的问题别名清单。 */
export class AssetPreflightRefusal extends HarnessError{
 assetIssues:AssetIssue[];
 constructor(issues:AssetIssue[]){super('asset_preflight_failed');this.assetIssues=issues;}
}
