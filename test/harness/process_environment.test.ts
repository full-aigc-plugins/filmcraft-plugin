import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { childEnvironment } from '../../src/support/process_environment.ts';

test('editor child environment retains operational settings and excludes host secrets and code injection', () => {
  const source={PATH:'/usr/bin:/bin',HOME:'/owned/home',TMPDIR:'/owned/temp',LANG:'zh_CN.UTF-8',LC_CTYPE:'UTF-8',
    OPENAI_API_KEY:'OWNED_TEST_CANARY',HTTP_PROXY:'https://OWNED_TEST_CANARY@proxy.invalid',
    PYTHONPATH:'/owned/injection',DYLD_INSERT_LIBRARIES:'/owned/injection.dylib',NODE_OPTIONS:'--require /owned/injection'};
  assert.deepEqual(childEnvironment(source),{PATH:source.PATH,HOME:source.HOME,TMPDIR:source.TMPDIR,LANG:source.LANG,LC_CTYPE:source.LC_CTYPE});
});

test('local model directory remains explicit configuration without forwarding arbitrary FilmCraft variables', () => {
  assert.equal(childEnvironment({FILMCRAFT_DATA_DIR:'/owned/models'}).FILMCRAFT_DATA_DIR,'/owned/models');
  assert.equal(childEnvironment({FILMCRAFT_DATA_DIR:'OWNED_TEST_CANARY'}).FILMCRAFT_DATA_DIR,undefined);
  assert.equal(childEnvironment({FILMCRAFT_API_KEY:'OWNED_TEST_CANARY'}).FILMCRAFT_API_KEY,undefined);
});

test('actual child cannot observe excluded host keys or inherited command-line injection', () => {
  const env=childEnvironment({...process.env,OPENAI_API_KEY:'OWNED_TEST_CANARY',NODE_OPTIONS:'--require /owned/absent.js',PYTHONPATH:'/owned/injection'});
  const code='if(process.env.OPENAI_API_KEY||process.env.NODE_OPTIONS||process.env.PYTHONPATH)process.exit(7);process.stdout.write("isolated-env")';
  const run=spawnSync(process.execPath,['-e',code],{env,encoding:'utf8'});
  assert.equal(run.status,0,run.stderr);assert.equal(run.stdout,'isolated-env');
});


test('process identity probe also excludes inherited host secrets and injection', async () => {
  const { mkdtempSync, writeFileSync, rmSync } = await import('node:fs');
  const { tmpdir } = await import('node:os');
  const { join } = await import('node:path');
  const { processIdentity } = await import('../../src/harness/process_identity.ts');
  const directory = mkdtempSync(join(tmpdir(), 'filmcraft-probe-env-'));
  const shim = join(directory, 'python-observer');
  const keys = ['OPENAI_API_KEY', 'HTTP_PROXY', 'PYTHONPATH', 'NODE_OPTIONS'];
  const before = Object.fromEntries(keys.map(key => [key, process.env[key]]));
  try {
    writeFileSync(shim, '#!/usr/bin/env python3\nimport os,sys\nassert not any(key in os.environ for key in '+JSON.stringify(keys)+')\nos.execvp("python3", ["python3", *sys.argv[1:]])\n', { mode: 0o700 });
    for (const key of keys) { process.env[key] = 'OWNED_TEST_CANARY'; }
    assert.equal(processIdentity(process.pid, shim)?.pid, process.pid);
  } finally {
    for (const key of keys) { if (before[key] === undefined) { delete process.env[key]; } else { process.env[key] = before[key]; } }
    rmSync(directory, { recursive: true, force: true });
  }
});
