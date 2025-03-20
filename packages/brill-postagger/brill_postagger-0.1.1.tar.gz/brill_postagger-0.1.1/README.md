# Brill Postagger

A Python package that uses the Brill Tagging algorithm for part-of-speech tagging, available for several languages. It utilizes the NLTK library for tokenization and tagging.

Models have been trained with [UniversalDependencies](https://github.com/UniversalDependencies) datasets

## Installation

To install the package, you can use pip:

```bash
pip install brill_postagger
```

## Usage

To use the Brill Postagger, first download the corresponding pre-trained model, then use it to tag sentences in various languages.

Example usage:

```python
from brill_postagger import BrillPostagger

# Initialize the tagger for Portuguese (pt)
tagger = BrillPostagger.from_pretrained("pt")

# Tag a sentence
result = tagger.tag("como está o tempo lá fora?")
print(result)
```

### Supported Languages

The following languages are supported, each corresponding to a pre-trained model:

- Catalan (`ca`)
- Danish (`da`)
- German (`de`)
- English (`en`)
- Spanish (`es`)
- Basque (`eu`)
- French (`fr`)
- Galician (`gl`)
- Italian (`it`)
- Dutch (`nl`)
- Portuguese (`pt`)

### Contributing

If you'd like to contribute to the project, please feel free to submit issues or pull requests. Contributions are always welcome!

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
