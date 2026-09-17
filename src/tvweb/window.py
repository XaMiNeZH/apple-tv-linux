"""libadwaita first-run and preferences window."""

from __future__ import annotations

import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, GLib, Gtk

from tvweb import APP_ID, APP_NAME, APPLE_TV_URL, __version__
from tvweb.browsers import Browser, detect_browsers, pick_browser
from tvweb.config import Config, profile_dir, save_config
from tvweb.launcher import launch

_DISCLAIMER = (
    "Unofficial wrapper. Not affiliated with Apple. "
    "Playback quality matches the Linux web player, not the Windows or macOS apps."
)


class PreferencesWindow(Adw.ApplicationWindow):
    def __init__(self, application: Adw.Application, config: Config) -> None:
        super().__init__(application=application, title=APP_NAME)
        self.set_default_size(520, 520)
        self._config = config
        self._browsers = detect_browsers()
        self._browser_ids = [browser.id for browser in self._browsers]

        toast = Adw.ToastOverlay()
        toolbar = Adw.ToolbarView()
        header = Adw.HeaderBar()
        header.set_title_widget(Adw.WindowTitle(title=APP_NAME, subtitle="tv.apple.com"))
        toolbar.add_top_bar(header)

        if not self._browsers:
            toolbar.set_content(self._empty_state())
        else:
            toolbar.set_content(self._preferences())

        toast.set_child(toolbar)
        self.set_content(toast)
        self._toasts = toast
 mar        about = Gio.SimpleAction.new("about", None)
        about.connect("activate", self._on_about)
        self.add_action(about)
        header.pack_end(
            Gtk.MenuButton(
                icon_name="open-menu-symbolic",
                menu_model=self._menu(),
            )
        )

    def _menu(self) -> Gio.Menu:
        menu = Gio.Menu()
        menu.append("About TV Web", "win.about")
        menu.append("Quit", "app.quit")
        return menu

    def _empty_state(self) -> Gtk.Widget:
        page = Adw.StatusPage(
            icon_name="video-display-symbolic",
            title="No supported browser found",
            description=(
                "Install Google Chrome, Microsoft Edge, or Firefox so tv.apple.com "
                "can use Widevine. Fedora Chromium often cannot play protected video."
            ),
        )
        return page

    def _preferences(self) -> Gtk.Widget:
        page = Adw.PreferencesPage()
        page.set_title("Setup")

        launch_group = Adw.PreferencesGroup(
            title="Watch",
            description=_DISCLAIMER,
        )
        open_row = Adw.ActionRow(
            title="Open Apple TV on the web",
            subtitle=APPLE_TV_URL,
        )
        open_button = Gtk.Button(label="Open", valign=Gtk.Align.CENTER)
        open_button.add_css_class("suggested-action")
        open_button.connect("clicked", self._on_open)
        open_row.add_suffix(open_button)
        open_row.set_activatable_widget(open_button)
        launch_group.add(open_row)
        page.add(launch_group)

        browser_group = Adw.PreferencesGroup(
            title="Browser",
            description="Chrome or Edge open an app window. Firefox uses a dedicated profile.",
        )
        names = Gtk.StringList.new([self._label_for(b) for b in self._browsers])
        self._browser_row = Adw.ComboRow(title="Engine", model=names)
        selected = 0
        preferred = pick_browser(self._browsers, self._config.browser_id)
        if preferred:
            selected = self._browser_ids.index(preferred.id)
        self._browser_row.set_selected(selected)
        self._browser_row.connect("notify::selected", self._on_browser_changed)
        browser_group.add(self._browser_row)

        self._drm_row = Adw.ActionRow(
            title="Protected playback",
            subtitle="",
        )
        browser_group.add(self._drm_row)
        page.add(browser_group)

        video_group = Adw.PreferencesGroup(title="Video")
        self._hw_row = Adw.SwitchRow(
            title="Hardware decoding",
            subtitle="VAAPI flags for Chrome/Edge, Firefox VAAPI pref in this profile",
            active=self._config.hardware_decode,
        )
        video_group.add(self._hw_row)
        page.add(video_group)

        clamp = Adw.Clamp(maximum_size=640, child=page)
        self._refresh_drm_row()
        return clamp

    def _label_for(self, browser: Browser) -> str:
        suffix = "" if browser.drm_likely else " (Widevine unlikely)"
        return f"{browser.name} ({browser.id}){suffix}"

    def _selected_browser(self) -> Browser:
        index = int(self._browser_row.get_selected())
        return self._browsers[index]

    def _on_browser_changed(self, *_args: object) -> None:
        self._refresh_drm_row()

    def _refresh_drm_row(self) -> None:
        browser = self._selected_browser()
        if browser.drm_likely:
            self._drm_row.set_subtitle(
                "This browser usually plays tv.apple.com on Linux (web quality)."
            )
        else:
            self._drm_row.set_subtitle(
                "Fedora Chromium often lacks Widevine. Prefer Chrome, Edge, or Firefox."
            )

    def _persist(self) -> Config:
        browser = self._selected_browser()
        config = Config(
            browser_id=browser.id,
            hardware_decode=self._hw_row.get_active(),
            completed_first_run=True,
        )
        save_config(config)
        self._config = config
        return config

    def _on_open(self, *_args: object) -> None:
        config = self._persist()
        browser = self._selected_browser()
        try:
            launch(
                browser,
                profile=profile_dir(browser.id),
                hardware_decode=config.hardware_decode,
                replace_process=False,
            )
        except OSError as exc:
            self._toasts.add_toast(Adw.Toast(title=f"Could not open browser: {exc}"))
            return
        self.get_application().quit()

    def _on_about(self, *_args: object) -> None:
        dialog = Adw.AboutDialog(
            application_name=APP_NAME,
            application_icon=APP_ID,
            developer_name="Ahmed Amine EZ-ZAHERY",
            version=__version__,
            comments=_DISCLAIMER,
            website="https://github.com/XaMiNeZH/apple-tv-linux",
            issue_url="https://github.com/XaMiNeZH/apple-tv-linux/issues",
            license_type=Gtk.License.MIT_X11,
        )
        dialog.present(self)


def run_preferences(config: Config, argv: list[str]) -> int:
    app = Adw.Application(application_id=APP_ID)

    def on_activate(application: Adw.Application) -> None:
        window = PreferencesWindow(application, config)
        window.present()

    def on_quit(_action: Gio.SimpleAction, _param: GLib.Variant | None) -> None:
        app.quit()

    app.connect("activate", on_activate)
    quit_action = Gio.SimpleAction.new("quit", None)
    quit_action.connect("activate", on_quit)
    app.add_action(quit_action)
    app.set_accels_for_action("app.quit", ["<Control>q"])
    return app.run(argv)
