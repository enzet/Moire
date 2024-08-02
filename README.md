# Moire

Moire (pronounced as /mwɑɹ/) is a simple extendable multipurpose markup language.

## Writing on Moire

### Default formatter

#### Headers

There are 6 possible header levels: `\1`, `\2`, ..., `\6` with syntax `\<header level> {<header name>} {<header label>}`. E.g.: `\2 {Section 3} {section-3}`.

#### Formatting

|  | Example Moire code | Rendering |
|---|---|---|
| Italic | `\i {text}` | *text* |
| Bold | `\b {text}` | **text** |
| Monospaced | `\m {text}` | `text` |
| Strikethrough | `\strike {text}` | ~~text~~ |
| Subscript | `\sub {text}` | <sub>text</sub> |
| Superscript | `\super {text}` | <sup>text</sup> |

#### Links

| Example Moire code | Rendering |
|---|---|
| `\ref {http://example.com} {external link}` | [external link](http://example.com) |
| `\ref {#example-section} {internal link}` | [internal link](#example-section) |

#### Lists

Example Moire code:

*italic **bold italic*** **italic *bold italic***

```moire
\list
    {Item 1,}
    {item 2.}
```

Rendering:


  * Item 1,
  * item 2.

#### Tables

Example Moire code:

```moire
\table
    {{Header 1} {Header 2}}
    {{Cell 1, 1} {Cell 1, 2}}
    {{Cell 2, 1} {Cell 2, 2}}
```

Rendering:

| Header 1 | Header 2 |
|---|---|
| Cell 1, 1 | Cell 1, 2 |
| Cell 2, 1 | Cell 2, 2 |

## Installation

Requirements: Python 3.8.

```bash
pip install .
```

## Conversion Moire code into other formats

Convert Moire file to other formats:

```bash
    moire -i <Moire input file> -f <format> -o <output file> <other options>
```

E.g., this file is generated from Moire code using this command:

```bash
moire -i doc/readme.moi -o README.md -f DefaultMarkdown
```

## Example section

