Sublime-nRepeat
===============

A port of the repeat functionality of the universal-argument from Emacs to SublimeText3.

## WARNING
Do NOT have any text selected when using the command provided in this plugin, as the selection will be overwritten!

## Installation
**The easiest way to install this plugin is through the [Package Control Plugin](https://sublime.wbond.net/installation)**. Open the Command Palette (`ctrl+shift+p` on Windows/Linux and `cmd+shift+p` on OS X) and type `Package Control: Install Package`. Confirm with `Enter` and type `nRepeat`. Again confirm with `Enter` and the plugin will be installed. Upon finished installation you should see a short message about this plugin.

If you want to install the plugin manually instead, navigate to the `Packages` folder:

* **Windows:** `%APPDATA%/Sublime Text 3/Packages`
* **OS X:**    `~/Library/Application Support/Sublime Text 3/Packages`
* **Linux:**   `~/.config/sublime-text-3/Packages`

Either directly clone this repository via `git clone https://github.com/bfrascher/Sublime-nRepeat.git` or download the repository as a zip file and extract it here into a new folder `nRepeat`.

## Version
This is the initial version of this plugin. Apart from the problem with selected regions (see warning above), it is working well for me with SublimeText3 Build 3059 (x64), but I wasn't able to test it extensively. So there might be bugs!

## Usage
Type `alt+r` and then enter the number of times you want the next input to be repeated by simply typing in the digits. The first command or non-digit after typing `alt+r` will be the repeated input. If you want to repeat a digit, simply type `alt+r` again, followed by the digit to be repeated.

You don't need to input a number, any non-digit input after the first `alt+r` will be repeated 4 times. You can chain this by typing multiple `alt+r` in succession. The non-digit input will then be repeated 4^n times, where n is the number of `alt+r` entered.
