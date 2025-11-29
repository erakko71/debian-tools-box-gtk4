# Debian Tools Box (GTK4)

Debian Tools Box is a small GTK4 desktop application that provides graphical shortcuts for common Debian tasks – especially for new users who are not comfortable with the terminal (yet).

It does **not** try to replace the command line or any existing tools.  
Instead, it offers a simple, safe front-end for everyday actions that users already know they need.

> Note: The app was originally built with a Finnish UI, but can be translated to other languages.  
> English strings are gradually being added.

---

## Features

Current version: **v1.0.0**

- **System update**
  - Run APT update/upgrade
  - Run Flatpak updates
  - Show basic status information

- **Application install helpers**
  - Common multimedia tools
  - Utilities and desktop tools
  - (Exact lists may vary between releases)

- **Fixes & troubleshooting**
  - A small collection of common “one click” fixes
  - Designed to be safe and explicit about what is being run

- **System info**
  - Basic information about the system environment

- **GTK4-based UI**
  - Clean layout, clear labels, large buttons
  - Designed for beginners and non-technical users

---

## Installation

### 1. From .deb package (recommended for normal users)

1. Download the latest `.deb` from the **Releases** page.
2. Install it:

   ```bash
   sudo dpkg -i debian-tools-box-gtk4_1.0.0_all.deb
   sudo apt -f install
git clone https://github.com/erakko71/debian-tools-box-gtk4.git
cd debian-tools-box-gtk4

python3 src/debian_tools_box_gtk4.py
