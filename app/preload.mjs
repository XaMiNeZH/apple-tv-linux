// Sandboxed Electron preloads run as classic scripts, even with an .mjs suffix.
// Electron provides this restricted require function inside the preload sandbox.
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("tvweb", {
  appName: "TV Web",
  completeFirstRun: () => ipcRenderer.invoke("tvweb:first-run:complete"),
  navigate: (action) => ipcRenderer.invoke("tvweb:navigate", action),
  openHelp: (page) => ipcRenderer.invoke("tvweb:open-help", page),
});
