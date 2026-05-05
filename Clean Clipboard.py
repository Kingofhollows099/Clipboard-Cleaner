import pyperclip
import csv
import io
import re
import unicodedata
import tkinter as tk
from rapidfuzz import fuzz

# --- Default Config ---
defaultFuzzyThreshhold = 85

# --- Regex codes ---
whitespaceRegex = re.compile(r"\s+")
newlineRegex = re.compile(r"\r\n|\r|\n")
digitRegex = re.compile(r"\d")
quantifierRegex = re.compile(r"\s*\(?\s*[xX]\s*\d+\s*\)?|\s*\(\s*\d+\s*\)", re.IGNORECASE)

def tidy(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).replace("\u00A0", " ")
    s = whitespaceRegex.sub(" ", s)
    return s.strip()

def testForDigits(s: str) -> bool: # Returns True if input has digits in it, otherwise False
    return bool(digitRegex.search(s))

def splitToList(s: str): # Takes in comma-sperated-values and returns the input converted into a list
    if "," in s:
        parts = [tidy(p) for p in s.split(",") if p.strip()]
        if parts:
            return parts
    return [s]

def convertToTitleCase(s: str) -> str: # Takes in any string and returns it with every word capitalized
    words = s.split()
    result_words = []
    for w in words:
        if testForDigits(w) or w.isupper():
            result_words.append(w)
        else:
            result_words.append(w.capitalize())
    return " ".join(result_words)


def processClipboard(
    # Default toggles
    splitCommaEnabled = True,
    dedupEnabled      = True,
    fuzzyEnabled      = True,
    titleCaseEnabled  = True,
    alphSortEnabled   = True,
    dequantifyEnabled = True,
    fuzzyThreshhold = defaultFuzzyThreshhold,
):
    text = pyperclip.paste() # Gets user's clipboard
    if not text:
        return "⚠  Clipboard is empty."

    reader = csv.reader(io.StringIO(text), delimiter="\t")

    items = []
    for row in reader:
        for cell in row:
            if not cell: # If blank, skip
                continue
            for part in newlineRegex.split(cell): # Splits clipboard text by newlines
                part = tidy(part)
                if not part:
                    continue
                if splitCommaEnabled:
                    for subpart in splitToList(part): # Splits clipboard text by commas if enabled
                        items.append(subpart)
                else:
                    items.append(part)
                    
    # Remove blank lines
    items = [item for item in items if item.strip()] # lol

    if dequantifyEnabled:
        # Matches (X2), x2, X 2, (x 2), (5), ( 5 ), x 7, etc.
        items = [tidy(quantifierRegex.sub("", item)) for item in items]

    # Remove any items that became empty after dequantify
    items = [item for item in items if item]

    if dedupEnabled: # Scans through every item in the list and compares it to every value in unique. If there's no mathc, adds that value to unique. Otherwise, skips.
        unique = []
        existingValues = set()
        for item in items:
            normalItem = item.lower().replace("''", "")
            if testForDigits(item) or not fuzzyEnabled:
                if normalItem in existingValues:
                    continue
                existingValues.add(normalItem)
                unique.append(item)
            else:
                isDuplicate = False
                for existing in unique:
                    if testForDigits(existing):
                        continue
                    score = fuzz.token_sort_ratio(normalItem, existing.lower())
                    if score >= fuzzyThreshhold:
                        isDuplicate = True
                        break
                if not isDuplicate:
                    existingValues.add(normalItem)
                    unique.append(item)
    else:
        unique = list(items)

    if titleCaseEnabled: # Applies titlecase
        unique = [convertToTitleCase(u) for u in unique]

    if alphSortEnabled: # Applies Alph sorting
        unique = sorted(unique, key=lambda x: x.lower())

    out = "\n".join(unique) # Sets the output text to every list value after the operations, with each item on a newline.
    pyperclip.copy(out) # Copies output text to clipboard
    return f"✓  {len(items)} -> {len(unique)} items copied to clipboard."


# --- Tooltips -----------------------------------------------------------

class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text   = text
        self.tw     = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.attributes("-topmost", True)
        self.tw.wm_geometry(f"+{x}+{y}")
        tk.Label(
            self.tw, text=self.text,
            bg="#2b2b3b", fg="#dddddd",
            font=("Segoe UI", 8),
            relief="flat", padx=7, pady=4,
            justify="left",
        ).pack()

    def _hide(self, event=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None


# --- GUI -------------------------------------------------------------

class ClipboardCleanerApp(tk.Tk):
    # Colors
    backgroundCLR        = "#181825"
    OnBtnBackgroundCLR   = "#e94560"
    OffBtnBackgroundCLR  = "#252535"
    OnBtnForegroundCLR   = "#ffffff"
    OffBtnForegroundCLR  = "#44445a"
    statusBG             = "#11111b"
    statusTextCLR        = "#e94560"
    dividerCLR           = "#2a2a3e"

    def __init__(self):
        super().__init__()
        self.title("Clipboard Cleaner")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.configure(bg=self.backgroundCLR)

        self.splitComma       = tk.BooleanVar(value=True)
        self.deduplicate      = tk.BooleanVar(value=True)
        self.fuzzy            = tk.BooleanVar(value=True)
        self.titleCase        = tk.BooleanVar(value=True)
        self.alphSort         = tk.BooleanVar(value=True)
        self.dequantify       = tk.BooleanVar(value=True)
        self.fuzzyThreshhold  = tk.IntVar(value=defaultFuzzyThreshhold)

        self._btns = {}
        self._buildUI()

    def _buildUI(self):
        bar = tk.Frame(self, 
                       bg = self.backgroundCLR, 
                       padx = 6, 
                       pady = 6)
        bar.pack(fill = "x")

        # (display text, font, value, tooltip)
        # font: "emoji" uses Segoe UI Emoji 14, "label" uses Consolas 11 bold
        toggles = [
            ("scissor", "emoji", "\u2702", self.splitComma,
             "Split on commas\nExpands 'a, b, c' into separate items"),
            
            ("dequantify", "label", "x2", self.dequantify,
             "Dequantify\nRemove quantifiers like x2 or (x3) from text"),
            
            ("dedup",   "emoji", "\U0001F9F9", self.deduplicate,
             "Deduplicate\nRemoves duplicate entries"),
            
            ("case",    "label", "Aa", self.titleCase,
             "Title Case\nCapitalises the first letter of each word"),
            
            ("sort",    "emoji", "\U0001F524", self.alphSort,
             "Sort A to Z\nAlphabetically sorts the output"),
            
            ("fuzzy",   "label", "~%", self.fuzzy,
             "Fuzzy match\nCollapses near-identical text as duplicates\n(uses the threshold number to the right)"),
        ]

        emojiFont = ("Segoe UI Emoji", 13) # Emoji is one size smaller, because if it's not then their buttons get too large.
        labelFont = ("Consolas", 14, "bold")

        for _key, ftype, icon, var, tip in toggles:
            f = emojiFont if ftype == "emoji" else labelFont
            button = tk.Button(
                bar,
                text   = icon,
                font   = f,
                width  = 2,
                relief = "flat",
                cursor = "hand2",
                padx   = 3, 
                pady   = 3,
                command = lambda v = var: self._toggle(v),
            )
            button.pack(side="left", padx=2)
            self._btns[id(var)] = (button, var)
            self._refreshButton(var)
            Tooltip(button, tip)

        # dividerCLR
        tk.Frame(bar, bg = self.dividerCLR, width=1).pack(
            side = "left", 
            fill = "y", 
            padx = 7, 
            pady = 3
        )

        # Fuzzy spinbox
        spin = tk.Spinbox(
            bar,
            from_               = 0, 
            to                  = 100,
            textvariable        = self.fuzzyThreshhold,
            width               = 3,
            font                = ("Consolas", 11, "bold"),
            bg                  = self.OffBtnBackgroundCLR, 
            fg                  = self.OnBtnBackgroundCLR,
            buttonbackground    = self.OffBtnBackgroundCLR,
            relief              = "flat",
            highlightthickness  = 1,
            highlightbackground = "#333355",
            insertbackground    = self.OnBtnBackgroundCLR,
        )
        spin.pack(side="left", padx=(0, 5))
        spin.bind("<MouseWheel>", self._scrollChangeFuzzy)
        spin.bind("<Button-4>",   self._scrollChangeFuzzy)
        spin.bind("<Button-5>",   self._scrollChangeFuzzy)
        Tooltip(spin, "Fuzzy threshold  (0 - 100)\nScroll or type to adjust.\nHigher = stricter duplicate detection.")

        # dividerCLR
        tk.Frame(bar, bg=self.dividerCLR, width=1).pack(
            side = "left", 
            fill = "y", 
            padx = 7, 
            pady = 3
        )

        # Run button
        run = tk.Button(
            bar,
            text             = "\u25b6",
            font             = ("Segoe UI Emoji", 14),
            bg               = self.OnBtnBackgroundCLR, 
            fg               = "white",
            activebackground = self.OnBtnBackgroundCLR, activeforeground="white",
            relief           = "flat", 
            cursor           = "hand2",
            padx             = 6, 
            pady             = 3,
            command          = self._run,
        )
        run.pack(side = "left", padx = (0, 2))
        Tooltip(run, "Clean clipboard\nProcess and copy result to clipboard")

        # Status bar
        self.statusText = tk.StringVar(value="Ready.")
        tk.Label(
            self,
            textvariable = self.statusText,
            bg           = self.statusBG, 
            fg           = self.OnBtnBackgroundCLR,
            font         = ("Consolas", 8),
            anchor       = "w", 
            padx         = 8, 
            pady         = 3,
        ).pack(fill="x")

    def _toggle(self, var: tk.BooleanVar):
        var.set(not var.get())
        self._refreshButton(var)

    def _refreshButton(self, var: tk.BooleanVar):
        button, v = self._btns[id(var)]
        if v.get():
            button.config(
                bg = self.OnBtnBackgroundCLR, 
                fg = self.OnBtnForegroundCLR,
                activebackground = self.OnBtnBackgroundCLR, 
                activeforeground = "white",
            )
        else:
            button.config(
                bg = self.OffBtnBackgroundCLR, 
                fg = self.OffBtnForegroundCLR,
                activebackground = self.OffBtnBackgroundCLR, 
                activeforeground = self.OffBtnForegroundCLR,
            )

    def _scrollChangeFuzzy(self, event):
        if   event.num == 4: delta =  1
        elif event.num == 5: delta = -1
        else: delta = 1 if event.delta > 0 else -1
        self.fuzzyThreshhold.set(max(0, min(100, self.fuzzyThreshhold.get() + delta)))

    def _run(self):
        self.statusText.set("Processing...")
        self.update_idletasks()
        msg = processClipboard(
            # These all update the toggle variables to match the buttons
            splitCommaEnabled = self.splitComma.get(),
            dedupEnabled      = self.deduplicate.get(),
            fuzzyEnabled      = self.fuzzy.get(),
            titleCaseEnabled  = self.titleCase.get(),
            alphSortEnabled   = self.alphSort.get(),
            dequantifyEnabled = self.dequantify.get(),
            fuzzyThreshhold   = self.fuzzyThreshhold.get(),
        )
        self.statusText.set(msg)


if __name__ == "__main__":
    app = ClipboardCleanerApp()
    app.mainloop()
