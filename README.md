# Clipboard Cleaner
A small utility for cleaning up lists. Copy something, click run, get a cleaned-up version back on your clipboard. Designed for working with spreadsheet data but works on anything list-like.

## Requirements
(Only applies if you're running the python file rather than the exe)
```
pip install pyperclip rapidfuzz
```

## How It Works
1. Reads whatever is in your clipboard
2. Applies whichever operations you have enabled, in this order:
   - Split on commas → Dequantify → Deduplicate → Title Case → Sort Alphabetically
3. Copies the result back to your clipboard

Input can be plain text (one item per line), comma-separated values, or tab-separated data copied directly from a spreadsheet.

## Example

You copy:
```
Apple, Orange
Bannana
apple
Pineapple (x2)
```

With all features enabled, you get:
```
Apple
Bannana
Orange
Pineapple
```

---

## Operations

### ✂ Split on Commas
Splits comma-separated values into individual items.

```
One, Two, Three  →  One
                     Two
                     Three
```

---

### x2 Dequantify
Removes quantity suffixes from items.

Supported formats: `x2`, `X2`, `(x2)`, `(x 2)`, `(2)`, `x 50`, etc.

```
Glorp (x50)  →  Glorp
Oompta x10   →  Oompta
```

---

### 🧹 Deduplicate
Removes exact duplicate items (case-insensitive).

```
Soda   →  Soda
Soda      Tea
Tea       Water
Water
```

Works together with Fuzzy Match to also catch near-duplicates — see below.

---

### Aa Title Case
Capitalizes the first letter of each word. Leaves all-uppercase words (like acronyms) and words containing numbers unchanged.

```
not a thing      →  Not A Thing
a thing              A Thing
kind of a Thing      Kind Of A Thing
RGB LED              RGB LED
```

---

### 🔤 Sort Alphabetically
Sorts items A–Z, case-insensitively.

```
George    →  Brandon
Brandon      George
Henry        Henry
```

---

### ~% Fuzzy Match
Catches near-duplicates that exact deduplication would miss — useful for typos, minor punctuation differences, or inconsistent spacing.

The number to the right of the button is the **similarity threshold** (0–100). An incoming item is treated as a duplicate if its similarity score against any already-accepted item meets or exceeds this value.

- **85** (default) — catches clear typos and small differences, e.g. `Bannana` vs `Banana`
- **Higher values** (90–100) — stricter; only collapses very close matches
- **Lower values** (70–80) — more aggressive; may collapse items that are actually distinct

When a duplicate is found, the **first-seen version** of the item is kept and the new one is discarded.

Items containing numbers are excluded from fuzzy matching and are always deduplicated by exact match only. This prevents part numbers, quantities, or codes from being incorrectly collapsed.

---

AI usage: Claude was used to modify the readme, as well as to debug.
