#!/usr/bin/env python3
import gi, sys, shutil, subprocess
gi.require_version('Gtk','4.0')
gi.require_version('Adw','1')
gi.require_version('Gdk','4.0')
from gi.repository import Gtk, Adw, Gdk

APP_ID = 'fi.erakko.DebianToolsBoxGTK4'

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_default_size(900, 520)
        self.set_title('Debian Tools Box GTK4 (v1.0.0)')

        # CSS: 11 pt semibold labels in headerbar buttons
        css = Gtk.CssProvider()
        css.load_from_data(b'''
        headerbar button label {
            font-size: 11pt;
            font-weight: 600;
        }
        ''')
        display = Gdk.Display.get_default()
        if display is not None:
            Gtk.StyleContext.add_provider_for_display(
                display, css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

        self.view_stack = Adw.ViewStack()

        toolbar = Adw.ToolbarView()
        self.set_content(toolbar)

        header = Adw.HeaderBar()
        toolbar.add_top_bar(header)

        # Custom tab buttons
        tab_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        tab_box.set_halign(Gtk.Align.CENTER)
        tab_box.set_hexpand(True)
        header.set_title_widget(tab_box)

        self.btn_tab_tools = Gtk.ToggleButton(label='Työkalut')
        self.btn_tab_install = Gtk.ToggleButton(label='Asennukset')
        self.btn_tab_monitor = Gtk.ToggleButton(label='Järjestelmän valvonta')

        for b in (self.btn_tab_tools, self.btn_tab_install, self.btn_tab_monitor):
            b.set_can_focus(True)

        self.btn_tab_tools.set_active(True)

        tab_box.append(self.btn_tab_tools)
        tab_box.append(self.btn_tab_install)
        tab_box.append(self.btn_tab_monitor)

        self.btn_tab_tools.connect('clicked', self.on_tab_tools)
        self.btn_tab_install.connect('clicked', self.on_tab_install)
        self.btn_tab_monitor.connect('clicked', self.on_tab_monitor)

        toolbar.set_content(self.view_stack)

        # Shared log buffer
        self.log_buffer = Gtk.TextBuffer()

        # Build pages with full functionality
        self._build_tools_page()
        self._build_install_page()
        self._build_monitor_page()

        self.log('Tervetuloa Debian Tools Box GTK4 v1.0.0:een.\n\n')

    # Tab handlers
    def on_tab_tools(self, _btn):
        self.view_stack.set_visible_child_name('tools')
        self.btn_tab_tools.set_active(True)
        self.btn_tab_install.set_active(False)
        self.btn_tab_monitor.set_active(False)

    def on_tab_install(self, _btn):
        self.view_stack.set_visible_child_name('install')
        self.btn_tab_tools.set_active(False)
        self.btn_tab_install.set_active(True)
        self.btn_tab_monitor.set_active(False)

    def on_tab_monitor(self, _btn):
        self.view_stack.set_visible_child_name('monitor')
        self.btn_tab_tools.set_active(False)
        self.btn_tab_install.set_active(False)
        self.btn_tab_monitor.set_active(True)

    # Utility: log + run_term
    def log(self, text: str):
        end = self.log_buffer.get_end_iter()
        self.log_buffer.insert(end, text)

    def run_term(self, cmd: str):
        term = shutil.which('x-terminal-emulator') or shutil.which('gnome-terminal')
        if not term:
            self.log('Virhe: ei päätettä (x-terminal-emulator / gnome-terminal).\n')
            return
        self.log(f'Ajetaan komento päätteessä:\n  {cmd}\n\n')
        full = cmd + "; echo; echo 'Paina Enter sulkeaksesi tämän ikkunan...'; read _"
        try:
            subprocess.Popen([term, '-e', 'bash', '-lc', full])
        except Exception as e:
            self.log(f'Virhe komennon käynnistyksessä: {e}\n')

    # --- Page 1: Työkalut ---
    def _build_tools_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.view_stack.add_titled(box, 'tools', 'Työkalut')

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left.set_margin_start(12); left.set_margin_end(12)
        left.set_margin_top(12); left.set_margin_bottom(12)
        box.append(left)

        self.btn_update = Gtk.Button(label='Päivitä järjestelmä (APT)')
        self.btn_clean  = Gtk.Button(label='Siivoa järjestelmä')
        self.btn_flat   = Gtk.Button(label='Päivitä Flatpak-sovellukset')
        self.btn_info   = Gtk.Button(label='Järjestelmän tiedot (perus)')
        self.btn_status = Gtk.Button(label='Järjestelmäinfo (laaja)')
        self.btn_fix    = Gtk.Button(label='Järjestelmäkorjaus')

        for b in (self.btn_update, self.btn_clean, self.btn_flat,
                  self.btn_info, self.btn_status, self.btn_fix):
            b.set_hexpand(True)
            left.append(b)

        frame = Gtk.Frame()
        frame.set_margin_top(12); frame.set_margin_bottom(12); frame.set_margin_end(12)
        box.append(frame)

        scrolled = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        frame.set_child(scrolled)
        tv = Gtk.TextView(buffer=self.log_buffer, editable=False, monospace=True)
        scrolled.set_child(tv)

        # Connect signals
        self.btn_update.connect('clicked', self.on_update)
        self.btn_clean.connect('clicked', self.on_clean)
        self.btn_flat.connect('clicked', self.on_flat)
        self.btn_info.connect('clicked', self.on_info)
        self.btn_status.connect('clicked', self.on_status)
        self.btn_fix.connect('clicked', self.on_fix)

    # --- Page 2: Asennukset ---
    def _build_install_page(self):
        outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.view_stack.add_titled(outer, 'install', 'Asennukset')

        left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        left.set_margin_start(12); left.set_margin_end(12)
        left.set_margin_top(12); left.set_margin_bottom(12)
        outer.append(left)

        lbl = Gtk.Label(label='Valitse ohjelmakategoria, jonka haluat asentaa:',
                        xalign=0)
        left.append(lbl)

        self.btn_install_browsers = Gtk.Button(label='Selaimet')
        self.btn_install_multi    = Gtk.Button(label='Multimedia')
        self.btn_install_graphics = Gtk.Button(label='Grafiikka')
        self.btn_install_tools    = Gtk.Button(label='Työkalut')

        for b in (self.btn_install_browsers,
                  self.btn_install_multi,
                  self.btn_install_graphics,
                  self.btn_install_tools):
            b.set_hexpand(True)
            left.append(b)

        frame = Gtk.Frame()
        frame.set_margin_top(12); frame.set_margin_bottom(12); frame.set_margin_end(12)
        outer.append(frame)

        scrolled = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        frame.set_child(scrolled)
        tv = Gtk.TextView(buffer=self.log_buffer, editable=False, monospace=True)
        scrolled.set_child(tv)

        # Signals
        self.btn_install_browsers.connect('clicked', self.install_browsers)
        self.btn_install_multi.connect('clicked', self.install_multimedia)
        self.btn_install_graphics.connect('clicked', self.install_graphics)
        self.btn_install_tools.connect('clicked', self.install_tools)

    # --- Page 3: Järjestelmän valvonta ---
    def _build_monitor_page(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(12); box.set_margin_bottom(12)
        box.set_margin_start(12); box.set_margin_end(12)
        self.view_stack.add_titled(box, 'monitor', 'Järjestelmän valvonta')

        info = Gtk.Label(
            label='Järjestelmän valvonta (alpha7)\n'
                  'Tähän tulee myöhemmin live-tilastoja (muisti, CPU, levy, GPU).\n'
                  'Voit jo nyt avata laajan systeminfo-raportin alla olevasta napista.',
            xalign=0
        )
        info.set_wrap(True)
        box.append(info)

        btn_sysinfo = Gtk.Button(label='Avaa laaja systeminfo-raportti päätteenä')
        box.append(btn_sysinfo)

        frame = Gtk.Frame()
        box.append(frame)
        scrolled = Gtk.ScrolledWindow(hexpand=True, vexpand=True)
        frame.set_child(scrolled)
        tv = Gtk.TextView(buffer=self.log_buffer, editable=False, monospace=True)
        scrolled.set_child(tv)

        btn_sysinfo.connect('clicked', self.on_monitor_sysinfo)

    # --- Core actions ---
    def on_update(self, _): self.run_term('sudo apt update && sudo apt full-upgrade')
    def on_clean(self,  _): self.run_term('sudo apt autoremove -y && sudo apt autoclean -y')
    def on_flat(self,   _): self.run_term("if command -v flatpak >/dev/null 2>&1; then flatpak update; else echo 'Flatpak ei ole asennettuna.'; fi")

    def on_info(self,   _):
        self.run_term("if command -v neofetch >/dev/null 2>&1; then neofetch; else echo 'neofetch puuttuu'; echo; uname -a; echo; lsb_release -a 2>/dev/null || cat /etc/os-release; fi")

    def on_status(self, _):
        dlg = Adw.MessageDialog(transient_for=self, modal=True,
                                heading='Järjestelmäinfo (laaja)',
                                body='Valitse tarkistus tai työkalu:')
        dlg.add_response('mem','Näytä muistin käyttö (free -h)')
        dlg.add_response('disk','Näytä levytila (df -h)')
        dlg.add_response('nvidia','Tarkista NVIDIA-ajuri')
        dlg.add_response('aptlog','Näytä päivitysloki (APT history)')
        dlg.add_response('gsoft','Avaa GNOME Software')
        dlg.add_response('sysinfo','Laaja systeminfo-raportti')
        dlg.add_response('cancel','Peruuta')
        dlg.set_close_response('cancel')
        dlg.connect('response', self.on_status_resp)
        dlg.show()

    def on_status_resp(self, dlg, resp):
        dlg.destroy()
        if resp == 'mem':
            self.run_term('free -h')
        elif resp == 'disk':
            self.run_term("echo 'Levytila (df -h):'; df -h | sort -k6")
        elif resp == 'nvidia':
            cmd = (
                "echo 'Tarkistetaan NVIDIA-ajurin tila...'; "
                "if command -v nvidia-smi >/dev/null 2>&1; then "
                "  nvidia-smi; "
                "else "
                "  echo 'nvidia-smi ei käytettävissä. Tarkistetaan lspci:'; "
                "  echo; lspci | grep -i nvidia || echo 'Ei NVIDIA-laitetta lspci-listassa.'; "
                "fi"
            )
            self.run_term(cmd)
        elif resp == 'aptlog':
            cmd = (
                "echo 'Viimeisimmät APT-päivitykset (/var/log/apt/history.log):'; "
                "echo; sudo tail -n 200 /var/log/apt/history.log || echo 'Ei voitu lukea history.log-tiedostoa.'"
            )
            self.run_term(cmd)
        elif resp == 'gsoft':
            cmd = (
                "if command -v gnome-software >/dev/null 2>&1; then "
                "  echo 'Avataan GNOME Software...'; "
                "  gnome-software & "
                "else "
                "  echo 'GNOME Software ei ole asennettuna tässä järjestelmässä.'; "
                "fi"
            )
            self.run_term(cmd)
        elif resp == 'sysinfo':
            cmd = (
                "echo 'Järjestelmäinfo (hostnamectl):'; hostnamectl || echo 'hostnamectl ei saatavilla'; "
                "echo; echo 'Levyosiot (lsblk):'; lsblk; "
                "echo; echo 'Muistin käyttö (free -h):'; free -h; "
                "echo; echo 'Levytila (df -h):'; df -h | sort -k6"
            )
            self.run_term(cmd)
        else:
            self.log('Järjestelmäinfo (laaja) peruutettu.\n')

    def on_fix(self, _):
        dlg = Adw.MessageDialog(transient_for=self, modal=True,
                                heading='Järjestelmäkorjaus',
                                body='Valitse korjattava asia:')
        dlg.add_response('bt','Korjaa Bluetooth / audio (PipeWire)')
        dlg.add_response('icons','Korjaa ikonit ja GTK-teemat')
        dlg.add_response('apt','Korjaa APT-lukitus / asennus')
        dlg.add_response('cancel','Peruuta')
        dlg.set_close_response('cancel')
        dlg.connect('response', self.on_fix_resp)
        dlg.show()

    def on_fix_resp(self, dlg, resp):
        dlg.destroy()
        if resp == 'bt':
            cmd = ("echo 'Käynnistetään PipeWire/äänipalvelut...' ; "
                   "systemctl --user restart pipewire.service pipewire-pulse.service wireplumber.service 2>/dev/null || true ; "
                   "echo ; echo 'Valmis.'")
            self.run_term(cmd)
        elif resp == 'icons':
            cmd = ("echo 'Päivitetään ikonivälimuisti...' ; "
                   "gtk-update-icon-cache -f /usr/share/icons/* 2>/dev/null || true ; "
                   "sudo update-icon-caches /usr/share/icons/* 2>/dev/null || true ; "
                   "echo ; echo 'Valmis.'")
            self.run_term(cmd)
        elif resp == 'apt':
            cmd = ("echo 'Korjataan APT-lukituksia...' ; "
                   "sudo rm -f /var/lib/dpkg/lock* /var/lib/apt/lists/lock /var/cache/apt/archives/lock ; "
                   "sudo dpkg --configure -a ; sudo apt install -f ; "
                   "echo ; echo 'Valmis.'")
            self.run_term(cmd)
        else:
            self.log('Järjestelmäkorjaus peruutettu.\n')

    # Monitor page button
    def on_monitor_sysinfo(self, _):
        cmd = (
            "echo 'Järjestelmäinfo (hostnamectl):'; hostnamectl || echo 'hostnamectl ei saatavilla'; "
            "echo; echo 'Levyosiot (lsblk):'; lsblk; "
            "echo; echo 'Muistin käyttö (free -h):'; free -h; "
            "echo; echo 'Levytila (df -h):'; df -h | sort -k6"
        )
        self.run_term(cmd)

    # Install categories
    def install_browsers(self, _):
        dlg = Adw.MessageDialog(transient_for=self, modal=True,
                                heading='Selaimet',
                                body='Valitse selain:')
        dlg.add_response('brave','Brave-selain')
        dlg.add_response('chromium','Chromium-selain')
        dlg.add_response('cancel','Peruuta')
        dlg.set_close_response('cancel')
        dlg.connect('response', self.on_browsers_resp)
        dlg.show()

    def on_browsers_resp(self, dlg, resp):
        dlg.destroy()
        if resp == 'brave':
            self.run_term('sudo apt install -y brave-browser')
        elif resp == 'chromium':
            self.run_term('sudo apt install -y chromium')
        else:
            self.log('Selaimen asennus peruutettu.\n')

    def install_multimedia(self, _):
        dlg = Adw.MessageDialog(transient_for=self, modal=True,
                                heading='Multimedia',
                                body='Valitse ohjelma:')
        dlg.add_response('vlc','VLC-mediasoitin')
        dlg.add_response('mpv','MPV-mediasoitin')
        dlg.add_response('codecs','Multimedia-codecit (täysi paketti)')
        dlg.add_response('cancel','Peruuta')
        dlg.set_close_response('cancel')
        dlg.connect('response', self.on_multi_resp)
        dlg.show()

    def on_multi_resp(self, dlg, resp):
        dlg.destroy()
        if resp == 'vlc':
            self.run_term('sudo apt install -y vlc')
        elif resp == 'mpv':
            self.run_term('sudo apt install -y mpv')
        elif resp == 'codecs':
            cmd = ('sudo apt install -y '
                   'gstreamer1.0-libav '
                   'gstreamer1.0-plugins-good '
                   'gstreamer1.0-plugins-bad '
                   'gstreamer1.0-plugins-ugly '
                   'ffmpeg libdvd-pkg'
                   ' && sudo dpkg-reconfigure libdvd-pkg')
            self.run_term(cmd)
        else:
            self.log('Multimedian asennus peruutettu.\n')

    def install_graphics(self, _):
        dlg = Adw.MessageDialog(transient_for=self, modal=True,
                                heading='Grafiikka',
                                body='Valitse ohjelma:')
        dlg.add_response('gimp','GIMP-kuvankäsittely')
        dlg.add_response('gthumb','gThumb-kuvakatselin')
        dlg.add_response('flameshot','Flameshot-kuvakaappaustyökalu')
        dlg.add_response('cancel','Peruuta')
        dlg.set_close_response('cancel')
        dlg.connect('response', self.on_graphics_resp)
        dlg.show()

    def on_graphics_resp(self, dlg, resp):
        dlg.destroy()
        if resp == 'gimp':
            self.run_term('sudo apt install -y gimp')
        elif resp == 'gthumb':
            self.run_term('sudo apt install -y gthumb')
        elif resp == 'flameshot':
            self.run_term('sudo apt install -y flameshot')
        else:
            self.log('Grafiikkaohjelmien asennus peruutettu.\n')

    def install_tools(self, _):
        dlg = Adw.MessageDialog(transient_for=self, modal=True,
                                heading='Työkalut',
                                body='Valitse työkalu:')
        dlg.add_response('timeshift','Timeshift')
        dlg.add_response('gparted','GParted')
        dlg.add_response('htop','htop')
        dlg.add_response('cancel','Peruuta')
        dlg.set_close_response('cancel')
        dlg.connect('response', self.on_tools_resp)
        dlg.show()

    def on_tools_resp(self, dlg, resp):
        dlg.destroy()
        if resp == 'timeshift':
            self.run_term('sudo apt install -y timeshift')
        elif resp == 'gparted':
            self.run_term('sudo apt install -y gparted')
        elif resp == 'htop':
            self.run_term('sudo apt install -y htop')
        else:
            self.log('Työkalujen asennus peruutettu.\n')

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APP_ID)
    def do_activate(self, *args):
        win = self.props.active_window
        if not win:
            win = MainWindow(self)
        win.present()

def main():
    Adw.init()
    app = App()
    return app.run(sys.argv)

if __name__ == '__main__':
    raise SystemExit(main())
