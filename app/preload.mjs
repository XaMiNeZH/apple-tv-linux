import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("tvweb", {
  appName: "TV Web",
  completeFirstRun: () => ipcRenderer.invoke("tvweb:first-run:complete"),
  navigate: (action) => ipcRenderer.invoke("tvweb:navigate", action),
  openHelp: (page) => ipcRenderer.invoke("tvweb:open-help", page),
});
