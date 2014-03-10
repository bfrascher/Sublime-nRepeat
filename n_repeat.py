# (C) 2014 by Benedikt Rascher-Friesenhausen
# github: bfrascher
#
# This plugin aims to implement the repeat functionality of the universal-argument in Emacs.
# Program behaviour:
# On running 'repeat' all user entered digits are saved in a string 'number_string', appending the new digit
# to the right. The first non-digit or command (other than 'repeat') entered will then be
# repeated 'int(number_string)' times.
# If instead 'repeat' is run again any next input will be repeated 'int(number_string)' times (except for 'repeat').
# If yet another 'repeat' is run, the command forgets all about 'number_string' and starts over.
# If only 'repeat' has been run when a non-digit or command is entered, then the input is
# repeated '4^call_count' times, where call_count is the number of 'repeat' calls.
#
# Visualisation:
# 1) 'repeat -> digits... -> repeat -> repeat' becomes 'repeat'
# 2) 'repeat -> digits... -> repeat -> digit/non-digit-command' repeats digit/non-digit-command digits... times
# 3) 'repeat... (n times) -> non-digit/command' repeats non-digit/command 4^n times
# 4) 'repeat -> digits... -> non-digit/command' repeats non-digit/command digits... times

# WARNING -- DO NOT HAVE A REGION SELECTED WHEN RUNNING THIS COMMAND
# As I haven't found a way to intercept user input, before it is entered into the view, this plugin
# will copy the last inserted character and then delete it from the view. That means, if you have
# a region selected, that region will be overwritten by the first character input after this command
# and then deleted.

import sublime, sublime_plugin

# the states the listener can be in
# while listening: waits for command 'repeat' and ignores all other commands
# while paused   : redirects all commands to 'repeat_empty', preventing
#                  them from being executed (will only be active for a couple of ms
#                  and should only affect commands issued from this plugin)
# while running  : reads the times to repeat from the user input and finally repeats
#                  the last command/character the given number of times
STATE_LISTENING = 0
STATE_RUNNING   = STATE_LISTENING + 1
STATE_PAUSED    = STATE_RUNNING   + 1

# defining digits
DIGITS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

# maximum number of possible repeats
# prevents sublime from becoming unresponsive
MAX_REPEATS = 1000000

class NRepeatCommand(sublime_plugin.EventListener):
    def __init__(self):
        # the view that called our command
        self.calling_view = None
        # the current command execution state
        self.state = STATE_LISTENING
        # the number inserted by the user while running
        self.number_string = ""
        # the number of calls of this command in a row
        self.call_count = 0

    def extract_inserted_char(self):
        # the inserted char is the same at every position
        # so we only have to read it from one of them
        pos = self.calling_view.sel()[0].begin()
        region = sublime.Region(pos, pos-1)
        char = self.calling_view.substr(region)
        # delete the char, as we have read it
        self.calling_view.run_command("left_delete")
        return char

    def get_repeats(self):
        if self.number_string != "":
            repeats = int(self.number_string)
        else:
            repeats = 4**self.call_count
        return min(repeats, MAX_REPEATS)

    # returning 'repeat_empty' prevents on_modified from being called
    # on commands, that should only affect this plugin
    def on_text_command(self, view, command_name, args):
        if self.state == STATE_PAUSED:
            return "repeat_empty", args
        elif self.state == STATE_RUNNING:
            if command_name == "cancel":
                # reset
                self.__init__()
            elif command_name == "n_repeat":
                self.call_count += 1
                if self.call_count >= 3 and self.number_string != "":
                    self.number_string = ""
                    self.call_count = 1
            else:
                repeats = self.get_repeats()
                # preventing on_modified to be called on these modifications
                self.state = STATE_PAUSED
                for i in range(repeats):
                        self.calling_view.run_command(command_name, args)
                # reset
                self.__init__()
            return "repeat_empty", args
        else: #self.state == STATE_LISTENING
            # this command has been called
            if command_name == "n_repeat":
                self.calling_view = view
                self.state = STATE_RUNNING
                self.call_count = 1
                return "repeat_empty", args

    def on_modified(self, view):
        if self.state == STATE_RUNNING:
            if self.calling_view == view:
                # we are modifying the view and don't want to
                # react to it
                self.state = STATE_PAUSED
                char = self.extract_inserted_char()
                if (char in DIGITS) and (self.call_count < 2):
                    self.number_string += char
                    # ignore leading 0
                    if self.number_string == "0":
                        self.number_string = ""
                    # extracted the digit from the view
                    # now we want to catch all events again
                    self.state = STATE_RUNNING
                    self.call_count = 1
                else:
                    repeats = self.get_repeats()
                    # insert char repeat times at each position
                    for pos in self.calling_view.sel():
                        self.calling_view.run_command("repeat_insert",{"pos": str(pos.begin()), "s": char*repeats})
                    # reset
                    self.__init__()

# THIS COMMAND IS INTENDED TO BE CALLED INTERNALLY ONLY
# RepeatEmptyCommand is a TextCommand that does nothing.
# This is important, on_modified is not called, when running it.
# So we can redirect all commands here, when we don't want the view
# to get modified (espacially for RepeatCommand itself).
class RepeatEmtpyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        return

# THIS COMMAND IS INTENDED TO BE CALLED INTERNALLY ONLY
# RepeatInsCommand inserts the given string 's' at the
# given position 'pos' into 'self.view'.
class RepeatInsertCommand(sublime_plugin.TextCommand):
    def run(self, edit, pos, s):
        self.view.insert(edit, int(pos), s)