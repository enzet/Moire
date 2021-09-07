Moire
=====

Moire (pronounced as /mwɑː/) is a simple extendable multipurpose markup language.

Writing on Moire
----------------

### Default formatter ###

#### Headers ####

There are 6 possible header levels: `\1`, `\2`, ..., `\6` with syntax `\<header level> {<header name>} {<header label>}`. E.g.: `\2 {Section 3} {section-3}`.

#### Formatting ####

Italic (`\i`), bold (`\b`), underlined (`\u`), subscript (`\sub`), superscript (`\super`).

| Example Moire code | Markdown rendering |
|---|---|
| `\i {text}` | *text* |
| `\b {text}` | **text** |
| `\m {text}` | `text` |

#### Links ####

| Example Moire code | Markdown rendering |
|---|---|
| `\ref {http://example.com} {external link}` | [external link](http://example.com) |
| `\ref {#example-section} {internal link}` | [internal link](#example-section) |

#### Lists ####

Example Moire code:

```moire
\list
    {Item 1,}
    {item 2.}
```

Markdown rendering:

  * Item 1,
  * item 2.

#### Tables ####

Example Moire code:

```moire
\table
    {{Header 1} {Header 2}}
    {{Cell 1, 1} {Cell 1, 2}}
    {{Cell 2, 1} {Cell 2, 2}}
```

Markdown rendering:

| Header 1 | Header 2 |
|---|---|
| Cell 1, 1 | Cell 1, 2 |
| Cell 2, 1 | Cell 2, 2 |

Installation
------------

Requirements: Python 3.9.

```bash
pip install .
```

Conversion Moire code into other formats
----------------------------------------

Convert Moire file to other formats:

```bash
moire -i <Moire input file> -f <format> -o <output file> <other options>
```

E.g., this file is generated from Moire code using this command:

```bash
moire -i doc/readme.moi -o README.md -f DefaultMarkdown
```

Example section
---------------

