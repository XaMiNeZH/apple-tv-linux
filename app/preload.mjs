import { contextBridge } from "electron";

contextBridge.exposeInMainWorld("tvweb", {
  appName: "TV Web",
});
