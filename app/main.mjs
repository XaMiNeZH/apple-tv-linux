import { app, BrowserWindow, Menu, shell, nativeImage } from "electron";
import path from "node:path";
import { fileURLToPath } from "node:url";

const APP_ID = "xyz.xaminezh.TvWeb";
const APP_NAME = "TV Web";
const APPLE_TV_URL = "https://tv.apple.com";
const __dirname = path.dirname(fileURLToPath(import.meta.url));

const ALLOWED_HOSTS = new Set([
  "tv.apple.com",
  "www.apple.com",
  "apple.com",
  "account.apple.com",
  "idmsa.apple.com",
  "gsa.apple.com",
  "secure.store.apple.com",
  "buy.tv.apple.com",
  "play-edge.itunes.apple.com",
  "uts-api.itunes.apple.com",
  "amp-api.music.apple.com",
]);

function hostAllowed(urlString) {
  try {
    const { hostname } = new URL(urlString);
    if (ALLOWED_HOSTS.has(hostname)) {
      return true;
    }
    return (
      hostname.endsWith(".apple.com") ||
      hostname.endsWith(".cdn-apple.com") ||
      hostname.endsWith(".mzstatic.com") ||
      hostname.endsWith(".icloud.com")
    );
  } catch {
    return false;
  }
}

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
  app.commandLine.appendSwitch(
    "enable-features",
    "VaapiVideoDecodeLinuxGL,VaapiIgnoreDriverChecks,AcceleratedVideoDecodeLinuxGL,PlatformHEVCDecoderSupport",
  );
  app.commandLine.appendSwitch("ignore-gpu-blocklist");
}

function createMenu() {
  const isLinux = process.platform === "linux";
  const template = [
    ...(isLinux
      ? [
          {
            label: APP_NAME,
            submenu: [
              { role: "about" },
              { type: "separator" },
              { role: "quit" },
            ],
          },
        ]
      : []),
    {
      label: "View",
      submenu: [
        { role: "reload" },
        { role: "togglefullscreen" },
        { type: "separator" },
        { role: "toggleDevTools" },
      ],
    },
    {
      label: "Window",
      submenu: [{ role: "minimize" }, { role: "close" }],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

function attachNavigation(win) {
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (!hostAllowed(url)) {
      shell.openExternal(url);
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
      },
    };
  });

  win.webContents.on("will-navigate", (event, url) => {
    if (!hostAllowed(url) && !url.startsWith("file:")) {
      event.preventDefault();
      shell.openExternal(url);
    }
  });

  win.webContents.on("did-fail-load", (_event, code, desc, url, isMain) => {
    if (!isMain || code === -3) {
      return;
    }
    const detail = encodeURIComponent(`${desc} (${url})`);
    win.loadFile(path.join(__dirname, "error.html"), {
      query: { detail },
    });
  });
}

async function createMainWindow() {
  const win = new BrowserWindow({
    width: 1360,
    height: 860,
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
    },
  });

  win.setMenuBarVisibility(false);
  attachNavigation(win);

  win.once("ready-to-show", () => {
    win.show();
  });

  await win.loadFile(path.join(__dirname, "splash.html"));
  win.show();
  await win.loadURL(APPLE_TV_URL);
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
    const win = BrowserWindow.getAllWindows()[0];
    if (!win) {
      return;
    }
    if (win.isMinimized()) {
      win.restore();
    }
    win.focus();
  });

  app.whenReady().then(async () => {
    createMenu();
    await createMainWindow();
  });

  app.on("window-all-closed", () => {
    app.quit();
  });
}
