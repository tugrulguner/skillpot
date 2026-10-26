import test from 'node:test';
import assert from 'node:assert/strict';
import { groupRows } from './transform.mjs';

test('groups two fixture rows sharing an identifier into one record', () => {
  assert.deepEqual(groupRows([
    { id: 'demo-1', item: 'apples' },
    { id: 'demo-1', item: 'pears' },
  ]), [{ id: 'demo-1', items: ['apples', 'pears'] }]);
});

test('rejects malformed rows rather than producing a success result', () => {
  assert.throws(() => groupRows([{ id: '', item: 'apples' }]), /non-empty/);
  assert.throws(() => groupRows('not rows'), /array/);
});
