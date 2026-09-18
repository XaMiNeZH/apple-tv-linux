import assert from "node:assert/strict";
import test from "node:test";

import { isAppleUrl, isExternalWebUrl } from "../app/navigation.mjs";

test("allows trusted Apple HTTPS hosts", () => {
  assert.equal(isAppleUrl("https://tv.apple.com/us/show/example"), true);
  assert.equal(isAppleUrl("https://account.apple.com/sign-in"), true);
  assert.equal(isAppleUrl("https://images.cdn-apple.com/poster.jpg"), true);
});

test("rejects lookalike hosts and non-HTTPS URLs", () => {
  assert.equal(isAppleUrl("https://apple.com.example.org"), false);
  assert.equal(isAppleUrl("https://evilapple.com"), false);
  assert.equal(isAppleUrl("http://tv.apple.com"), false);
  assert.equal(isAppleUrl("file:///etc/passwd"), false);
});

test("only recognizes HTTP and HTTPS as external web links", () => {
  assert.equal(isExternalWebUrl("https://example.org"), true);
  assert.equal(isExternalWebUrl("http://example.org"), true);
  assert.equal(isExternalWebUrl("mailto:test@example.org"), false);
  assert.equal(isExternalWebUrl("javascript:alert(1)"), false);
});
