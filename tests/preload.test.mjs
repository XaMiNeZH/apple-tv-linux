import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { fileURLToPath } from "node:url";
import vm from "node:vm";

test("sandboxed preload exposes the narrow IPC bridge", async () => {
  const calls = [];
  let exposed;
  const context = {
    require(moduleName) {
      assert.equal(moduleName, "electron");
      return {
        contextBridge: {
          exposeInMainWorld(name, api) {
            exposed = { name, api };
          },
        },
        ipcRenderer: {
          invoke(...args) {
            calls.push(args);
            return Promise.resolve(true);
          },
        },
      };
    },
  };
  const source = readFileSync(
    fileURLToPath(new URL("../app/preload.mjs", import.meta.url)),
    "utf8",
  );

  vm.runInNewContext(source, context);
  assert.equal(exposed.name, "tvweb");
  await exposed.api.completeFirstRun();
  await exposed.api.navigate("home");
  await exposed.api.openHelp("project");
  assert.deepEqual(calls, [
    ["tvweb:first-run:complete"],
    ["tvweb:navigate", "home"],
    ["tvweb:open-help", "project"],
  ]);
});
