Moire
=====

Moire is a simple multipurpose markup.

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
| `\tt {text}` | `text` |

#### Links ####

| Example Moire code | Markdown rendering |
|---|---|
| `\href {http://example.com} {external link}` | [external link](http://example.com) |
| `\href {#example-section} {internal link}` | [internal link](#example-section) |

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
    {{\th {Header 1}} {\th {Header 2}}}
    {{Cell 1, 1} {Cell 1, 2}}
    {{Cell 2, 1} {Cell 2, 2}}
```

Markdown rendering:

| <NO TAG> | <NO TAG> |
|---|---|
| Cell 1, 1 | Cell 1, 2 |
| Cell 2, 1 | Cell 2, 2 |

Conversion Moire code into other formats
----------------------------------------

You can convert your Moire file to other formats using Python 3.9:

```bash
python converter.py -i <Moire input file> -f <format> -o <output file> <other options>
```

E.g., this file is generated from Moire code using this command:

```bash
python3.9 converter.py -i doc/manual/readme.moi -o README.md -f DefaultMarkdown
```

### Options ###

`-i` or `--input`—input file in *Moire* format;

`-o` or `--output`—output file;

`-t` or `--to`—format of output file. May be `html`, `text` or `markdown`;

`-s` or `--scheme`—scheme file name.

Example section
---------------

