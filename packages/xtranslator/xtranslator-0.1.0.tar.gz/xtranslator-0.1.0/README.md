# XTranslator

XTranslator is a package that allows you to detect the language of a given text and translate it into various languages. With its simple and intuitive interface, you can easily integrate language detection and translation capabilities into your applications.

## Installation

To install XTranslator, simply run the following command:

```
pip install xtranslator
```

## Usage

To use XTranslator in your project, follow these steps:

1. Import the XTranslator package into your code:

```python
import xtranslator
```

2. Detect the language of a text:

```python
from xtranslator import detect
text = "Hello, my nam is XTranslator"
detector = "fasttext"
print(detect(text, detector))
```

3. Translate text into another language:

```python
from xtranslator import translate
text = "Hello, world!"
translator = "google"
model_name = "google"
dest_language = "sk"
detector = "fasttext"
print(translate(text, dest_language, translator, model_name, detector))
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the [GitHub repository](https://github.com/ivanvykopal/xtranslator).

## License

XTranslator is licensed under the [MIT License](https://opensource.org/licenses/MIT).
