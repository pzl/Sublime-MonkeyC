MonkeyC
===============

This is a [Sublime Text](http://www.sublimetext.com/) language definition and plugin for the [MonkeyC](http://developer.garmin.com/connect-iq/monkey-c/) language. MonkeyC is a [Garmin](http://www.garmin.com/)-developed language for the [ConnectIQ](http://developer.garmin.com/connect-iq/overview) platform, that runs on many of their devices, like smart watches.

When you download and set up the [Connect IQ SDK](https://developer.garmin.com/connect-iq/sdk/) this plugin will also allow you to build Connect IQ projects, Simulate and test them, and package for releasing and uploading.

**File Extension**: `.mc`


Installation
------------

1. Using [Package Control](http://wbond.net/sublime_packages/package_control), install "MonkeyC"

Or.

1. Open the Sublime Text Packages folder on your computer
2. clone this repo

### Configuration

Once installed, you should go to `Preferences > Package Settings > MonkeyC > Settings` and put in the path to your Connect IQ SDK ([download](https://developer.garmin.com/connect-iq/sdk/) if you haven't already). And put in the path to your developer key. If you don't have a key and just want to generate one, you can use `Tools > MonkeyC > Generate Developer Key` to have this plugin make one, and update your key path for you.



Features
---------

### Editing

- **Syntax Highlighting**: including special coloring for CIQ modules in the Toybox namespace. Includes advanced syntax highlighting for `.jungle` files

![MonkeyC syntax coloring](http://pzl.github.io/Sublime-MonkeyC/images/mc-highlight.png) ![Jungle syntax coloring](http://pzl.github.io/Sublime-MonkeyC/images/jungle-highlight.png)


- **Autocomplete**: for language keywords like `instanceof`, `break` and full snippets for things like `module`s and `class`es. Autocompletes device names, qualifiers, and languages in jungle files.

![MonkeyC autocomplete](http://pzl.github.io/Sublime-MonkeyC/images/mc-autocomplete.png) ![Jungle autocomplete](http://pzl.github.io/Sublime-MonkeyC/images/jungle-autocomplete.png)

- **Comment-Toggle**: Select some lines and hit `Ctrl-/` to toggle comments on or off. Works in `.mc` and `.jungle`. (use `Ctrl-Shift-/` for block comments)
- **Go-To Symbols**: Adds module, class, and function names to the Sublime symbol list, as well as `(:annotations)`. Hit `Ctrl-r` to search symbols in current file, or `Ctrl-Shift-r` to search symbols in the whole project.

### Building (when connected with the SDK)

- **Compile**: You can compile connect iq apps (Applications, watch faces, data fields) and Barrels (modules).
- **Simulate**: The plugin can launch and connect to the simulator for you
- **Test**: Run assertions (through the simulator) and unit tests, similar to **Run No Evil** from the official Eclipse Plug-in.
- **Package**: Compile a `.iq` app ready for uploading and publishing to the Connect IQ Store
- **Side-load**: Build for a device, to side-load it onto a device locally
- **Key Generation**: Don't have a developer key? Go to `Tools > MonkeyC > Generate Developer Key` and now you do! (uses `openssl` to make an RSA key, formatted properly)
- **App ID Generation**: Each Connect IQ App needs a special ID (UUID). The plugin can generate random UUIDs for you, and update your `manifest.xml` automatically



Versions
--------

### 3.0.0

Major syntax rules overhaul. Includes autocomplete, snippets, jungle file syntax, go-to symbols (module, class, function names as well as annotations), comment-toggling (Ctl-/), and much much better coloring and other-plugin support. See the [Release Notes](messages/3.0.0.txt) for full details.

### 2.1.0

Updates to include new packages in Connect IQ 3.0.0 (beta)

### 2.0.0
Updates to include (some? most?) language features as of SDK 2.4.4

### 1.0.0
Initial release, contains most language features as of SDK 1.2.5

---

**Sublime Text 2**

This package is currently not supported on ST2, as it uses `.sublime-syntax` files, a new feature in ST3. 


Contributing
------------

Please use the github issues page for this repo for requests, bugs, and before starting pull requests to plan work.


---
 
This repository and code are not affiliated with or supported by Garmin in any way. MonkeyC is a product and language developed by Garmin.