# Moire

Moire (pronounced as /mwɑɹ/) is a lightweight markup language designed for clear, structured, and portable text formatting. It aims to combine the simplicity of Markdown, the rigor of TeX, and the broad applicability of HTML — while avoiding their common pitfalls.

Moire is built to be general-purpose: write once, convert anywhere — web, print, documentation, ebooks, slides, or other formats — without getting trapped in one domain or ecosystem.

Why not other markup languages?


  *  Unlike many markup languages, Moire is designed for **general-purpose** text formatting, not tied to a specific output like web pages, PDFs, or technical documentation. 
  *  Unlike HTML or Wiki markup, Moire uses a **concise, consistent, and disambiguated tag system** — avoiding both the verbosity of HTML and the ambiguity of Markdown. 
  *  Unlike TeX, Moire is **simple** and **beginner-friendly**. For example, you can define a table without worrying about its styling or placement. 

## Writing on Moire

### Default formatter

#### Headers

There are 6 possible header levels: `\1`, `\2`, ..., `\6` with syntax `\<header level> {<header name>} {<header label>}`. E.g.: `\2 {Section 3} {section-3}`.

#### Formatting

|  | Example Moire code | Rendering |
|---|---|---|
| Emphasized | `\e {text}` | *text* |
| Strong emphasized | `\s {text}` | **text** |
| Inline code | `\c {text}` | `text` |
| Deleted | `\del {text}` | <del>text</del> |
| Subscript | `\sub {text}` | <sub>text</sub> |
| Superscript | `\super {text}` | <sup>text</sup> |

#### Links

| Example Moire code | Rendering |
|---|---|
| `\ref {http://example.com} {external link}` | [external link](http://example.com) |
| `\ref {#example-section} {internal link}` | [internal link](#example-section) |

#### Lists

Example Moire code:

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

Requirements: Python 3.12.

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

