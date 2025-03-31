"""CSC111 Project 2 WikiMap Team

Module Description
==================
Module contains custom tkinter elements for use in apps.


Copyright and Usage Information
===============================
This file is Copyright (c) 2025 CSC111 WikiMap Team
"""

import tkinter as tk

class AutocompleteText(tk.Text):
    """
    A tkinter Text widget with autocomplete functionality.

    This class code is wholly created by Bryan Oakley in his post:
    https://stackoverflow.com/questions/71770128/tkinter-text-autofill

    Oakley, Bryan. “Tkinter Text Autofill.” Stack Overflow, 1 Feb. 1967,
    stackoverflow.com/questions/71770128/tkinter-text-autofill.
    Accessed 30 Mar. 2025.
    """

    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("autocomplete", None)
        super().__init__(*args, **kwargs)

        # bind on key release, which will happen after tkinter
        # inserts the typed character
        self.bind("<Any-KeyRelease>", self._autocomplete)

        # special handling for tab, which needs to happen on the
        # key _press_
        self.bind("<Tab>", self._handle_tab)

    def _handle_tab(self, event):
        """Handles when the user presses tab."""
        # see if any text has the "autocomplete" tag
        tag_ranges = self.tag_ranges("autocomplete")
        if tag_ranges:
            # move the insertion cursor to the end of
            # the selected text, and then remove the "sel"
            # and "autocomplete" tags
            self.mark_set("insert", tag_ranges[1])
            self.tag_remove("sel", "1.0", "end")
            self.tag_remove("autocomplete", "1.0", "end")

            # prevent the default behavior of inserting a literal tab
            return "break"

    def _autocomplete(self, event):
        """Handles the autocompletion off the text box, given a callable function event."""
        if event.char and self.callback:
            # get word preceeding the insertion cursor
            word = self.get("insert-1c wordstart", "insert-1c wordend")

            matches = self.callback(word)

            if matches:
                # autocomplete on the first match
                remainder = matches[0][len(word):]

                # remember the current insertion cursor
                insert = self.index("insert")

                # insert at the insertion cursor the remainder of
                # the matched word, and apply the tag "sel" so that
                # it is selected. Also, add the "autocomplete" text
                # which will make it easier to find later.
                self.insert(insert, remainder, ("sel", "autocomplete"))

                # move the cursor back to the saved position
                self.mark_set("insert", insert)
