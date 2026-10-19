// Behavioral contracts for the browser enhancement, using Node's built-in runner.
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { readFileSync } = require('node:fs');
const { runInNewContext } = require('node:vm');
const { resolve } = require('node:path');

function submit(message, answer, alreadyPrevented = false) {
  let listener;
  const prompts = [];
  runInNewContext(readFileSync(resolve(__dirname, '../../core/static/core/actions.js'), 'utf8'), {
    document: { addEventListener(type, callback) { assert.equal(type, 'submit'); listener = callback; } },
    window: { confirm(text) { prompts.push(text); return answer; } },
  });
  const event = {
    target: { getAttribute(name) { assert.equal(name, 'data-confirm'); return message; } },
    defaultPrevented: alreadyPrevented,
    preventDefault() { this.defaultPrevented = true; },
  };
  listener(event);
  return { cancelled: event.defaultPrevented, prompts };
}

test('dismissing cancellation keeps the booking by stopping submission', () => {
  assert.deepEqual(submit('Cancel your booking?', false), { cancelled: true, prompts: ['Cancel your booking?'] });
});
test('accepting cancellation permits the existing CSRF-protected form submission', () => {
  assert.deepEqual(submit('Cancel your booking?', true), { cancelled: false, prompts: ['Cancel your booking?'] });
});
test('ordinary forms and previously prevented submissions do not prompt', () => {
  assert.deepEqual(submit(null, false), { cancelled: false, prompts: [] });
  assert.deepEqual(submit('Cancel?', false, true), { cancelled: true, prompts: [] });
});
