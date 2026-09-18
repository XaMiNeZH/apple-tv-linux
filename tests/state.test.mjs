import assert from "node:assert/strict";
import { mkdtempSync, readFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import {
  DEFAULT_STATE,
  normalizeState,
  readState,
  writeState,
} from "../app/state.mjs";

test("uses safe defaults for missing or malformed state", () => {
  const directory = mkdtempSync(path.join(tmpdir(), "tvweb-state-"));
  assert.deepEqual(readState(path.join(directory, "missing.json")), DEFAULT_STATE);
  assert.deepEqual(normalizeState({ window: { width: "wide" } }), DEFAULT_STATE);
});

test("bounds persisted window sizes", () => {
  const state = normalizeState({
    completedFirstRun: true,
    window: { width: 100, height: 9000, maximized: true },
  });
  assert.deepEqual(state, {
    completedFirstRun: true,
    window: { width: 900, height: 4320, maximized: true },
  });
});

test("writes normalized state atomically", () => {
  const directory = mkdtempSync(path.join(tmpdir(), "tvweb-state-"));
  const filePath = path.join(directory, "nested", "state.json");
  const written = writeState(filePath, {
    completedFirstRun: true,
    window: { width: 1280, height: 720, maximized: false },
  });
  assert.deepEqual(readState(filePath), written);
  assert.equal(JSON.parse(readFileSync(filePath, "utf8")).window.width, 1280);
});
