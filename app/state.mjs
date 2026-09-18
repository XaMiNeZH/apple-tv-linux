import {
  mkdirSync,
  readFileSync,
  renameSync,
  writeFileSync,
} from "node:fs";
import path from "node:path";

export const DEFAULT_STATE = Object.freeze({
  completedFirstRun: false,
  window: {
    width: 1360,
    height: 860,
    maximized: false,
  },
});

function integerInRange(value, fallback, minimum, maximum) {
  if (!Number.isInteger(value)) {
    return fallback;
  }
  return Math.min(Math.max(value, minimum), maximum);
}

export function normalizeState(value) {
  const state = value && typeof value === "object" ? value : {};
  const windowState =
    state.window && typeof state.window === "object" ? state.window : {};

  return {
    completedFirstRun: state.completedFirstRun === true,
    window: {
      width: integerInRange(
        windowState.width,
        DEFAULT_STATE.window.width,
        900,
        7680,
      ),
      height: integerInRange(
        windowState.height,
        DEFAULT_STATE.window.height,
        560,
        4320,
      ),
      maximized: windowState.maximized === true,
    },
  };
}

export function readState(filePath) {
  try {
    return normalizeState(
      JSON.parse(readFileSync(filePath, { encoding: "utf8" })),
    );
  } catch {
    return normalizeState(null);
  }
}

export function writeState(filePath, value) {
  const state = normalizeState(value);
  mkdirSync(path.dirname(filePath), { recursive: true });
  const temporaryPath = `${filePath}.tmp`;
  writeFileSync(temporaryPath, `${JSON.stringify(state, null, 2)}\n`, {
    encoding: "utf8",
    mode: 0o600,
  });
  renameSync(temporaryPath, filePath);
  return state;
}
