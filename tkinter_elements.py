import tkinter as tk

class AutocompleteText(tk.Text):
    def __init__(self, *args, **kwargs):
        self.callback = kwargs.pop("autocomplete", None)
        super().__init__(*args, **kwargs)

        # bind on key release, which will happen after tkinter
        # inserts the typed character
        self.bind("<Any-KeyRelease>", self._autocomplete)

        # special handling for tab, which needs to happen on the
        # key _press_
        self.bind("<Tab>", self._handle_space)

    def _handle_space(self, event):
        pass

    def _autocomplete(self, event):
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


def get_matches(word):
    # For illustrative purposes, pull possible matches from
    # what has already been typed. You could just as easily
    # return a list of pre-defined keywords.
    words = text.get("1.0", "end-1c").split()
    matches = [x for x in words if x.startswith(word)]
    return matches
