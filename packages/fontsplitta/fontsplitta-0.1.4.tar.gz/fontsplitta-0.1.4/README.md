# fontsplitta

`fontsplitta` is a command-line tool that splits web fonts and generates CSS.

It creates web fonts that are divided into specific Unicode ranges, similar to Google Fonts.

By properly splitting large fonts such as Japanese fonts, it aims to reduce transfer size and improve user experience.

## Requirements

- Python 3

## Getting Started

Install from PyPI:

```console
pip install fontsplitta
```

Generate `unicode_ranges.txt` using Google Fonts' CSS:

```console
fontsplitta get-unicode-ranges-from-google-fonts
```

Split fonts and generate CSS:

```console
fontsplitta split FONT_FILE
```

## Using a custom CSS template file

If you want to modify the output CSS, you can create a new `font-face.css.template` file:

```
@font-face {
  font-family: "${font_family}";
  font-style: ${font_style};
  font-weight: ${font_weight};
  src: url(http://localhost:8080/output/${font_filename}) format("${font_format}");
  unicode-range: ${unicode_range};
}
```

Basically, you should use your environment's hostname in the `src` section.

And then,

```console
fontsplitta split FONT_FILE --css_template=YOUR_CSS_TEMPLATE
```

## Using custom unicode ranges

If you want to use custom unicode ranges, you can use the `--unicode_ranges_file` option:

```console
fontsplitta split FONT_FILE --unicode_ranges_file=YOUR_UNICODE_RANGES_FILE
```

You can generate the unicode ranges using your web page contents.

## Test with local web server

```console
fontsplitta test-server
```
