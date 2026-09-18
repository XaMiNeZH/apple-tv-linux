import {
  app,
  BrowserWindow,
  ipcMain,
  Menu,
  nativeImage,
  shell,
} from "electron";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { isAppleUrl, isExternalWebUrl } from "./navigation.mjs";
import { readState, writeState } from "./state.mjs";

const APP_ID = "xyz.xaminezh.TvWeb";
const APP_NAME = "TV Web";
const APPLE_TV_URL = "https://tv.apple.com";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

let mainWindow = null;
let stateFile = "";
let appState = null;
let saveTimer = null;

function iconPath() {
  return path.join(
    __dirname,
    "..",
    "data",
    "icons",
    "hicolor",
    "scalable",
    "apps",
    "xyz.xaminezh.TvWeb.svg",
  );
}

function applyLinuxFlags() {
  app.commandLine.appendSwitch("ozone-platform-hint", "auto");
  if (process.env.TVWEB_ENABLE_VAAPI !== "1") {
    return;
  }
  app.commandLine.appendSwitch(
    "enable-features",
    "VaapiVideoDecodeLinuxGL,VaapiIgnoreDriverChecks,AcceleratedVideoDecodeLinuxGL,PlatformHEVCDecoderSupport",
  );
  app.commandLine.appendSwitch("ignore-gpu-blocklist");
}

function showAbout() {
  app.showAboutPanel();
}

function navigate(action) {
  if (!mainWindow || mainWindow.isDestroyed()) {
    return false;
  }
  const contents = mainWindow.webContents;
  if (action === "home") {
    void contents.loadURL(APPLE_TV_URL).catch(() => {});
    return true;
  }
  if (action === "back" && contents.canGoBack()) {
    contents.goBack();
    return true;
  }
  if (action === "forward" && contents.canGoForward()) {
    contents.goForward();
    return true;
  }
  if (action === "reload") {
    contents.reload();
    return true;
  }
  return false;
}

function openProjectPage(page) {
  const pages = {
    project: "https://github.com/XaMiNeZH/apple-tv-linux",
    issues: "https://github.com/XaMiNeZH/apple-tv-linux/issues",
  };
  const url = pages[page];
  if (!url) {
    return false;
  }
  void shell.openExternal(url);
  return true;
}

function createMenu() {
  const isLinux = process.platform === "linux";
  const viewItems = [
    {
      label: "Apple TV Home",
      accelerator: "CommandOrControl+Shift+H",
      click: () => navigate("home"),
    },
    { type: "separator" },
    {
      label: "Back",
      accelerator: "Alt+Left",
      click: () => navigate("back"),
    },
    {
      label: "Forward",
      accelerator: "Alt+Right",
      click: () => navigate("forward"),
    },
    {
      label: "Reload",
      accelerator: "CommandOrControl+R",
      click: () => navigate("reload"),
    },
    { type: "separator" },
    { role: "resetZoom" },
    { role: "zoomIn" },
    { role: "zoomOut" },
    { type: "separator" },
    { role: "togglefullscreen" },
  ];
  if (!app.isPackaged) {
    viewItems.push({ type: "separator" }, { role: "toggleDevTools" });
  }

  const template = [
    ...(isLinux
      ? [
          {
            label: APP_NAME,
            submenu: [
              { label: `About ${APP_NAME}`, click: showAbout },
              { type: "separator" },
              { role: "quit" },
            ],
          },
        ]
      : []),
    {
      label: "View",
      submenu: viewItems,
    },
    {
      label: "Window",
      submenu: [{ role: "minimize" }, { role: "close" }],
    },
    {
      role: "help",
      submenu: [
        { label: "Project Website", click: () => openProjectPage("project") },
        { label: "Report an Issue", click: () => openProjectPage("issues") },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

function isLocalAppPage(urlString) {
  try {
    if (!urlString.startsWith("file:")) {
      return false;
    }
    const localPath = fileURLToPath(urlString);
    return (
      localPath === __dirname ||
      localPath.startsWith(`${__dirname}${path.sep}`)
    );
  } catch {
    return false;
  }
}

function guardNavigation(event, url) {
  if (isAppleUrl(url) || isLocalAppPage(url)) {
    return;
  }
  event.preventDefault();
  if (isExternalWebUrl(url)) {
    void shell.openExternal(url);
  }
}

function attachNavigation(win) {
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (!isAppleUrl(url)) {
      if (isExternalWebUrl(url)) {
        void shell.openExternal(url);
      }
      return { action: "deny" };
    }
    return {
      action: "allow",
      overrideBrowserWindowOptions: {
        width: 520,
        height: 760,
        autoHideMenuBar: true,
        title: APP_NAME,
        icon: iconPath(),
        backgroundColor: "#0b1526",
        webPreferences: {
          contextIsolation: true,
          nodeIntegration: false,
          sandbox: true,
          partition: "persist:tvweb",
          plugins: true,
          spellcheck: false,
        },
      },
    };
  });

  win.webContents.on("did-create-window", (childWindow) => {
    childWindow.setMenuBarVisibility(false);
    attachNavigation(childWindow);
  });

  win.webContents.on("will-navigate", guardNavigation);
  win.webContents.on("will-redirect", guardNavigation);

  win.webContents.on("did-fail-load", (_event, code, desc, url, isMain) => {
    if (!isMain || code === -3 || !isExternalWebUrl(url)) {
      return;
    }
    const detail = encodeURIComponent(`${desc} (${url})`);
    void win.loadFile(path.join(__dirname, "error.html"), {
      query: { detail },
    });
  });

  win.webContents.on("page-title-updated", (event, title) => {
    if (!isAppleUrl(win.webContents.getURL())) {
      return;
    }
    event.preventDefault();
    win.setTitle(title ? `${title} — ${APP_NAME}` : APP_NAME);
  });
}

function saveWindowState(win) {
  if (!stateFile || !appState || win.isDestroyed()) {
    return;
  }
  const bounds = win.getNormalBounds();
  appState = writeState(stateFile, {
    ...appState,
    window: {
      width: bounds.width,
      height: bounds.height,
      maximized: win.isMaximized(),
    },
  });
}

function scheduleWindowStateSave(win) {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => saveWindowState(win), 250);
}

function registerIpc() {
  ipcMain.handle("tvweb:first-run:complete", async (event) => {
    if (!event.sender.getURL().includes("/first-run.html")) {
      throw new Error("First-run setup is not active");
    }
    appState = writeState(stateFile, {
      ...appState,
      completedFirstRun: true,
    });
    await event.sender.loadURL(APPLE_TV_URL);
    return true;
  });

  ipcMain.handle("tvweb:navigate", (_event, action) => {
    if (!["home", "back", "forward", "reload"].includes(action)) {
      return false;
    }
    return navigate(action);
  });

  ipcMain.handle("tvweb:open-help", (_event, page) =>
    openProjectPage(page),
  );
}

async function createMainWindow() {
  const windowState = appState.window;
  const win = new BrowserWindow({
    width: windowState.width,
    height: windowState.height,
    minWidth: 900,
    minHeight: 560,
    show: false,
    title: APP_NAME,
    icon: nativeImage.createFromPath(iconPath()),
    autoHideMenuBar: true,
    backgroundColor: "#0b1526",
    webPreferences: {
      preload: path.join(__dirname, "preload.mjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      partition: "persist:tvweb",
      plugins: true,
      spellcheck: false,
    },
  });

  mainWindow = win;
  win.setMenuBarVisibility(false);
  attachNavigation(win);
  win.on("resize", () => scheduleWindowStateSave(win));
  win.on("maximize", () => scheduleWindowStateSave(win));
  win.on("unmaximize", () => scheduleWindowStateSave(win));
  win.on("close", () => {
    clearTimeout(saveTimer);
    saveWindowState(win);
  });
  win.on("closed", () => {
    if (mainWindow === win) {
      mainWindow = null;
    }
  });

  await win.loadFile(path.join(__dirname, "splash.html"));
  if (windowState.maximized) {
    win.maximize();
  }
  win.show();
  if (appState.completedFirstRun) {
    await win.loadURL(APPLE_TV_URL).catch(() => {});
  } else {
    await win.loadFile(path.join(__dirname, "first-run.html"));
  }
  return win;
}

applyLinuxFlags();
app.setName(APP_NAME);
app.setAppUserModelId(APP_ID);

const gotLock = app.requestSingleInstanceLock();
if (!gotLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    const win = mainWindow;
    if (!win) {
      void createMainWindow();
      return;
    }
    if (win.isMinimized()) {
      win.restore();
    }
    win.focus();
  });

  app.whenReady().then(async () => {
    app.setAboutPanelOptions({
      applicationName: APP_NAME,
      applicationVersion: app.getVersion(),
      version: `Version ${app.getVersion()}`,
      copyright: "MIT — unofficial, not affiliated with Apple",
      website: "https://github.com/XaMiNeZH/apple-tv-linux",
      iconPath: iconPath(),
    });
    stateFile = path.join(app.getPath("userData"), "state.json");
    appState = readState(stateFile);
    registerIpc();
    createMenu();
    await createMainWindow();
  });

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      void createMainWindow();
    }
  });

  app.on("window-all-closed", () => {
    app.quit();
  });
}
