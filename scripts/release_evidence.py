#!/usr/bin/env python3
"""分层发行证据结构与当前身份门禁；可信收集器仍须实际执行并核实原始日志。"""
import re
from pathlib import Path

CHECKS={'python','node','fixed-source','metadata','protocol'}
LAYERS={'source','ci','fixed-install','real-media','host','platform'}


def validate_workflow(text,entry):
 if entry not in text or any(word in text for word in ('hashFiles','continue-on-error')):raise ValueError('required_workflow_conditional')
 if any(line.strip()!='if: always()' for line in text.splitlines() if re.match(r'^\s*if:',line)):raise ValueError('required_workflow_conditional')


def validate_checks(rows):
 ids=[r.get('id') for r in rows]
 if len(ids)!=len(set(ids)) or set(ids)!=CHECKS:raise ValueError('required_check_missing_or_duplicate')
 if any(r.get('status')!='PASS' or r.get('executed') is not True for r in rows):raise ValueError('required_check_not_executed')


def trace_index(root):
 root=Path(root);text=(root/'openspec/changes/establish-v1-plugin/tasks.md').read_text()
 table=text.split('### 验收索引与交付记录',1)[1].split('### P0',1)[0]
 known=set()
 for path in (root/'openspec/changes/establish-v1-plugin/specs').glob('*/spec.md'):
  known.update(re.findall(r'^#### Scenario: (\S+)',path.read_text(),re.M))
 groups=[]
 for line in table.splitlines():
  if not line.startswith('| ') or 'FC-' not in line:continue
  parts=[x.strip() for x in line.strip('|').split('|')]
  ids=re.findall(r'FC-[A-Z]+-\d{3}-[A-Z0-9-]+',parts[1])
  start,end=re.fullmatch(r'9\.(\d+)—9\.(\d+)',parts[2]).groups()
  if not ids or not set(ids).issubset(known):raise ValueError('optimization_scenario_unknown')
  groups.append({'name':parts[0],'scenarios':ids,'tasks':['9.'+str(n) for n in range(int(start),int(end)+1)]})
 if not groups or len([s for g in groups for s in g['scenarios']])!=len({s for g in groups for s in g['scenarios']}):raise ValueError('optimization_index_invalid')
 return groups


def validate_trace(rows,groups,identity,required_layers=None):
 scenarios={s for g in groups for s in g['scenarios']};keys=[]
 if {r.get('scenario') for r in rows}!=scenarios:raise ValueError('optimization_scenario_missing_or_unknown')
 for row in rows:
  keys.append(tuple(row.get(k) for k in ('scenario','layer','host','platform','mode')))
  if row.get('layer') not in LAYERS or row.get('identity')!=identity:raise ValueError('release_identity_mismatch')
  if row.get('status') not in ('PASS','FAIL','NOT_RUN'):raise ValueError('release_status_invalid')
  if row['status']=='NOT_RUN':
   if row.get('executed') is not False or not row.get('reason'):raise ValueError('not_run_reason_required')
   continue
  if (row.get('executed') is not True or not row.get('host') or not row.get('platform') or not row.get('mode')
    or not row.get('expected') or not row.get('actual') or not isinstance(row.get('inputHashes'),dict) or not row['inputHashes']
    or any(not re.fullmatch('[a-f0-9]{64}',str(v)) for v in row['inputHashes'].values())
    or not re.fullmatch('[a-f0-9]{64}',str(row.get('candidateSha256','')))):
   raise ValueError('execution_or_candidate_evidence_missing')
  log=row.get('log',{})
  if log.get('identity')!=identity or not log.get('path') or not re.fullmatch('[a-f0-9]{64}',str(log.get('sha256',''))):raise ValueError('log_identity_mismatch')
  if any(log.get(key)!=row.get(key) for key in ('candidateSha256','inputHashes','host','platform','mode')):raise ValueError('log_candidate_or_context_mismatch')
  if row['layer']=='real-media' and (row.get('mediaProvenance')!='real' or not row.get('licenseOrAuthorization')):raise ValueError('real_media_not_proven')
 if len(keys)!=len(set(keys)):raise ValueError('duplicate_execution_record')
 if required_layers:
  for scenario in scenarios:
   if {r['layer'] for r in rows if r['scenario']==scenario}!=set(required_layers):raise ValueError('execution_layer_missing')
 return {'scenarios':len(scenarios),'records':len(rows),'pass':sum(r['status']=='PASS' for r in rows),
         'fail':sum(r['status']=='FAIL' for r in rows),'notRun':sum(r['status']=='NOT_RUN' for r in rows)}
