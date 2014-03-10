Sublime-nRepeat
===============

A port of the repeat functionality of the universal-argument from Emacs to SublimeText3.

# WARNING
Do NOT use this plugin, while you have selected a region in the editor, as it will be overwritten!

## Version
This is the initial version of this plugin. Apart from the problem with selected regions (see warning above), it worked well for me with SublimeText3 Build 3059 (x64), but I wasn't able to test it extensively. So beware of bugs!

## Usage
Type `alt+r` and then enter the number of times you want the next input to be repeated by simply typing in the digits. The first command or non-digit after typing `alt+r` will be the repeated input. If you want to repeat a digit, simply type `alt+r` again, followed by the digit to be repeated.

You don't need to input a number, any non-digit input after the first `alt+r` will be repeated 4 times. You can chain this by typing multiple `alt+r` in succession. The non-digit input will then be repeated 4^n times, where n is the number of `alt+r` entered.