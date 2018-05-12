MonkeyC
===============

This is a [Sublime Text](http://www.sublimetext.com/) language definition and plugin for the [MonkeyC](http://developer.garmin.com/connect-iq/monkey-c/) language. MonkeyC is a [Garmin](http://www.garmin.com/)-developed language for the [ConnectIQ](http://developer.garmin.com/connect-iq/overview) platform, that runs on many of their devices, like smart watches.

When you download and set up the [Connect IQ SDK](https://developer.garmin.com/connect-iq/sdk/) this plugin will also allow you to build Connect IQ projects, Simulate and test them, and package for releasing and uploading to the Connect IQ Store.

**File Extension**: `.mc`


Installation
------------

1. Using [Package Control](http://wbond.net/sublime_packages/package_control), install "MonkeyC"

Or.

1. Open the Sublime Text Packages folder on your computer
2. clone this repo

### Configuration

Once installed, you should go to `Preferences > Package Settings > MonkeyC > Settings` and put in the path to your Connect IQ SDK ([download](https://developer.garmin.com/connect-iq/sdk/) if you haven't already). And put in the path to your developer key. If you don't have a key and just want to generate one, you can use `Tools > MonkeyC > Generate Developer Key` (or "MonkeyC: Generate Developer Key" from the Command Palette) to have this plugin make one, and update your key path for you.

You can override these settings on a per-project basis, by having a top-level key (monkeyc) in your `.sublime-project` file (Project > Edit Project) that looks like this:

```
{
    "folders": [ ... ],
    "monkeyc": {
        "sdk": "/path/to/other/SDK",
        "key": "~/specific/key/for/project"
    }
}
```

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

- **Compile**: You can compile connect iq apps (Applications, watch faces, data fields) and Barrels (modules). You can use the Sublime Build system (`ctrl-b` or the Command Palette: "MonkeyC: Build ...")
- **Simulate**: The plugin can launch and connect to the simulator for you. ("MonkeyC: Simulate")
- **Test**: Run assertions (through the simulator) and unit tests, similar to **Run No Evil** from the official Eclipse Plug-in. ("MonkeyC: Test" -- this will re-compile your project with the `-t` test flag, and run the simulator with the `-t` test flag)
- **Package**: Compile a `.iq` app ready for uploading and publishing to the Connect IQ Store ("MonkeyC: Package for Release". This strips debug and test information, includes any `:release` labels)
- **Side-load**: Build for a device, to side-load it onto a device locally ("MonkeyC: Build for Device" in command palette)
- **Key Generation**: Don't have a developer key? Go to `Tools > MonkeyC > Generate Developer Key` (or the Command Palette) and now you do! (uses `openssl` to make an RSA key, formatted properly)
- **App ID Generation**: Each Connect IQ App needs a special ID (UUID). The plugin can generate random UUIDs for you, and update your `manifest.xml` automatically


If you wanted to customize any of these actions, or make them key-bindings, they are available as sublime commands:

#### monkey_build

*compiles* your project. Accepts the following arguments:

- **do** _string_ (optional): `"release"`,`"test"` or `"custom"`. 
    - `release` applies the `-r -e` flags to the compiler, and makes the default file extension `.iq`
    - `test` applies the `-t` flag for applications. For barrels, it runs the `barreltest` command to run unit tests
    - `custom` prompts the user with the command to use right before running, allowing edits
- **name** _string_ (optional): the file name of the generated app. Defaults to the project folder name
- **device** _string_ (optional): adds `-d <device>` as a compiler option. Use the string `"prompt"` to have the plugin ask for device selection each time (based on the supported devices in your `manifest.xml` file)
- **sdk** _string_ (optional): adds `-s <sdk>` as a compiler option to target an SDK. Use the string `"prompt"` to have the plugin determine the supported SDK targets for the given device (a device is required).
- **flags** _list_ (optional): Any additional flags or command-line arguments you wish to specify. E.g. `run_command("monkey_build",{"flags":["-r"]})` to run a simple compile with the release flag (disables asserts, debug things).

#### monkey_simulate

runs the Connect IQ simulator. (Implicitly triggers a `monkey_build` for simulation device) Accepts the following arguments:

- **device** _string_ REQUIRED: the device to simulate on. Use the string "prompt" to have the plugin ask you for a device each time, based on your list in `manifest.xml`.
- **tests** _boolean_ (optional): If true, runs the unit tests in the project. Assertions are run regardless, unless it is a release build.


#### monkey_generate

Small helper creators. Like developer keys, or app IDs. Accepts the following arguments:

- **gen** _string_ REQUIRED: `key` to make a developer key, and update your settings with it. `uuid` to make a new App ID and update your `manifest.xml` with it


Versions
--------

### 3.1.0

Adds SDK integration. Compiles, simulates, and runs unit tests. See the [Release Notes](messages/3.1.0.txt) for full details.

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