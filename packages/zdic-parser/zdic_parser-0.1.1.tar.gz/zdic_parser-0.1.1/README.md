# ZDic Parser Tool

A very simple Python library to scrape and parse Chinese character data from [ZDic](https://www.zdic.net/) using BeautifulSoup.

> This library was developed and tested with **Python 3.12**, but it may work on other versions as well.

## Prerequisites

- **Python 3.12** (recommended, but may work on older versions)
- **pip** (Python package manager)

## Installation

To install the package, run:

```
pip install zdic-parser
```

## Usage
The library provides a class called **`ZDicCharacterParser`**, which is used to fetch character data from ZDic.  
The two key methods in this class are:

- **`search()`** → **Synchronous (Blocking)**
- **`search_async()`** → **Asynchronous (Non-blocking)**

## **Method Parameters**
Both **`search()`** and **`search_async()`** accept the following parameters:

| Parameter   | Type  | Default      | Description                                                                                        |
|-------------|-------|--------------|----------------------------------------------------------------------------------------------------|
| `character` | `str` | **Required** | The Chinese character to search for.                                                               |
| `mode`      | `str` | `"s"`        | Determines whether to return information in **Simplified ("s")** or **Traditional ("t")** Chinese. |
| `timeout`   | `int` | `5`          | The request timeout (in seconds).                                                                  |

### **Notes**
- The **`mode` parameter only affects the returned content**, such as definitions being in **Simplified ("s")** or **Traditional ("t")** Chinese.
- **You can search for both Simplified and Traditional characters** regardless of the `mode` selected.

### Synchronous search example

To perform a character search synchronously, we can use `search()`:
```python
from zdic_parser import ZDicCharacterParser

# Example character to search
example = "你"

# Create an instance of the parser
parser = ZDicCharacterParser()

# Perform the search (defaults to Simplified Chinese mode)
parser.search(example)
```

### Asynchronous search example
To perform a character search asynchronously, we use `search_async()`:
```python
import asyncio
from zdic_parser import ZDicCharacterParser

# Example character to search
example = "你"

async def main():
    # Create an instance of the parser
    parser = ZDicCharacterParser()
    
    # Perform the asynchronous search
    await parser.search_async(example)
    
    # Print results
    print(parser.character_info)
    print(parser.definitions)

# Run the asynchronous function
asyncio.run(main())
```
This is useful if we wish to parse multiple characters:

```python
import asyncio
from zdic_parser import ZDicCharacterParser

# List of characters to search
characters = ["你", "干", "吗"]


async def create_coroutines(character):
    parser = ZDicCharacterParser()
    await parser.search_async(character)
    return parser


async def main():
    tasks = [create_coroutines(char) for char in characters]
    parsers = await asyncio.gather(*tasks)

    # Print results / Do something with the results 
    for parser in parsers:
        print(parser.character_info)


# Run the asynchronous function
asyncio.run(main())
```

### 

## Methods and Fields

Below is a list of the fields the `ZDicCharacterParser` class contains:

| Field            | Data Type | Description                                              |
|------------------|-----------|----------------------------------------------------------|
| `character_info` | `dict`    | Contains detailed information about a Chinese character. |
| `definitions`    | `dict`    | Contains definitions of the character.                   |


### `character_info` structure
| Key                        | Data Type        | Description                         |
|----------------------------|------------------|-------------------------------------|
| `img_src`                  | `str` (optional) | SVG of the character.               |
| `pinyin`                   | `str` (optional) | Pinyin representation.              |
| `zhuyin`                   | `str` (optional) | Zhuyin (Bopomofo) notation.         |
| `radical`                  | `str` (optional) | Radical component.                  |
| `non_radical_stroke_count` | `int` (optional) | Stroke count excluding the radical. |
| `total_stroke_count`       | `int` (optional) | Total stroke count.                 |
| `simple_trad`              | `str` (optional) | Simplified and traditional forms.   |
| `variant_characters`       | `str` (optional) | Alternative character forms.        |
| `unicode`                  | `str` (optional) | Unicode representation.             |
| `character_structure`      | `str` (optional) | Structural composition.             |
| `stroke_order`             | `str` (optional) | Stroke order data.                  |
| `wubi`                     | `str` (optional) | Wubi input method code.             |
| `cangjie`                  | `str` (optional) | Cangjie input method code.          |
| `zhengma`                  | `str` (optional) | Zhengma input method code.          |
| `fcorners`                 | `int` (optional) | Four-corner input method code.      |

### `definitions` structure
| Key           | Data Type | Description                         |
|---------------|-----------|-------------------------------------|
| `simple_defs` | `dict`    | Basic definitions of the character. |

The `ZDicCharacterParser` class provides getters for all the aforementioned keys for convenience:

| Method                           | Returns           | Description                                        |
|----------------------------------|-------------------|----------------------------------------------------|
| `get_img_src()`                  | `str` (optional)  | SVG of the character.                              |
| `get_pinyin()`                   | `str` (optional)  | Pinyin representation of the character.            |
| `get_zhuyin()`                   | `str` (optional)  | Zhuyin (Bopomofo) notation.                        |
| `get_radical()`                  | `str` (optional)  | Radical component of the character.                |
| `get_non_radical_stroke_count()` | `int` (optional)  | Stroke count excluding the radical.                |
| `get_total_stroke_count()`       | `int` (optional)  | Total number of strokes in the character.          |
| `get_simple_trad()`              | `str` (optional)  | Simplified and traditional forms of the character. |
| `get_variant_characters()`       | `str` (optional)  | Alternative character forms.                       |
| `get_unicode()`                  | `str` (optional)  | Unicode representation of the character.           |
| `get_character_structure()`      | `str` (optional)  | Structural composition of the character.           |
| `get_stroke_order()`             | `str` (optional)  | Stroke order data.                                 |
| `get_wubi()`                     | `str` (optional)  | Wubi input method code.                            |
| `get_cangjie()`                  | `str` (optional)  | Cangjie input method code.                         |
| `get_zhengma()`                  | `str` (optional)  | Zhengma input method code.                         |
| `get_fcorners()`                 | `int` (optional)  | Four-corner input method code.                     |
| `get_simple_defs()`              | `dict` (optional) | Basic definitions of the character.                |


### **多音字** (Polyphonic Characters)
If a searched character is a **多音字** (polyphonic character), all available **Pinyin** and **Zhuyin** pronunciations will be returned as a **comma-separated string**:

```python
from zdic_parser import ZDicCharacterParser

# Example character to search
example = "和"

# Create an instance of the parser
parser = ZDicCharacterParser()

# Perform the search (defaults to Simplified Chinese mode)
parser.search(example)

print(parser.get_pinyin())  # Expected output: "hé, hè, huó, huò, hú"
print(parser.get_zhuyin())  # Expected output: "ㄏㄜˊ, ㄏㄜˋ, ㄏㄨㄛˊ, ㄏㄨㄛˋ, ㄏㄨˊ"
print(parser.get_variant_characters())  # Expected output: "咊, 咼, 惒, 盉, 訸, 鉌, 龢, 𤧗, 𥤉, 𧇮, 㕿, 𠰓"
```

## Static Methods
`ZDicCharacterParser` also provides static methods prefixed with `fetch` to fetch specific bits of information without the need to instantiate a `ZDicCharacterParser` object. 

| Method                                   | Returns           | Description                                        |
|------------------------------------------|-------------------|----------------------------------------------------|
| `async fetch_img_src()`                  | `str` (optional)  | SVG of the character.                              |
| `async fetch_pinyin()`                   | `str` (optional)  | Pinyin representation of the character.            |
| `async fetch_zhuyin()`                   | `str` (optional)  | Zhuyin (Bopomofo) notation.                        |
| `async fetch_radical()`                  | `str` (optional)  | Radical component of the character.                |
| `async fetch_non_radical_stroke_count()` | `int` (optional)  | Stroke count excluding the radical.                |
| `async fetch_total_stroke_count()`       | `int` (optional)  | Total number of strokes in the character.          |
| `async fetch_simple_trad()`              | `str` (optional)  | Simplified and traditional forms of the character. |
| `async fetch_variant_characters()`       | `str` (optional)  | Alternative character forms.                       |
| `async fetch_unicode()`                  | `str` (optional)  | Unicode representation of the character.           |
| `async fetch_character_structure()`      | `str` (optional)  | Structural composition of the character.           |
| `async fetch_stroke_order()`             | `str` (optional)  | Stroke order data.                                 |
| `async fetch_wubi()`                     | `str` (optional)  | Wubi input method code.                            |
| `async fetch_cangjie()`                  | `str` (optional)  | Cangjie input method code.                         |
| `async fetch_zhengma()`                  | `str` (optional)  | Zhengma input method code.                         |
| `async fetch_fcorners()`                 | `int` (optional)  | Four-corner input method code.                     |
| `async fetch_simple_defs()`              | `dict` (optional) | Basic definitions of the character.                |

```python
import asyncio
from zdic_parser import ZDicCharacterParser

# List of characters to search
characters = ["你", "干", "吗"]


async def create_coroutines(character):
    pinyin = await ZDicCharacterParser.fetch_pinyin(character)
    return pinyin


async def main():
    tasks = [create_coroutines(char) for char in characters]
    results = await asyncio.gather(*tasks)

    # Print results / Do something with the results 
    for result in results:
        print(result)


# Run the asynchronous function
asyncio.run(main())
```

> **Important Consideration:**  
> When the `search` (or `search_async`) method is called, an HTTP request is sent to the corresponding ZDic page. The HTML is then scraped for information and collated.  
>
> However, **not all information is always available** for every character. To indicate this, all methods are marked as returning **optional values (`None` when unavailable)**.
> 
> For example, consider the character **[𫵷](https://www.zdic.net/hans/%F0%AB%B5%B7)**. The only available information includes:
> - `radical`
> - `non_radical_stroke_count`
> - `total_stroke_count`
> - `unicode`
> - `character_structure`
> - `cangjie`
> 
> In this case, calling any other getter method (e.g., `get/fetch_pinyin()`, `get/fetch_zhuyin()`) will return `None`, since that data does not exist on the page.


## Exceptions 

The parser relies on the **relatively static nature** of ZDic's dictionary entries to extract the necessary information. However, if the **structure of the site changes**, the parsing algorithm may **break**.

In such cases, an `ElementIsMissingException` will be thrown. This exception indicates that one of the following issues has occurred:

- The **element's selector has changed**.
- The **website has been updated**.
- The **page URL is incorrect**.

### How to Handle This Exception
If you encounter an `ElementIsMissingException`:
1. **Check if ZDic's website structure has changed**.
2. **Verify the page URL** to ensure it's correct.
3. **Update the parser functions** inside `src/utils.py` to match the new structure.


I will try my best to consistently monitor for any drastic changes to zdic's page layout and release updates accordingly


