# Hebrew/Arabic semantic tokenizer utlizing root based words.
The tokenizer assumes that all words in Hebrew and Arabic can be decomposed into a representation consisting of four subclasses of letters: Prefix, Root, Infix, and Suffix.
The motivation is to utilize the unique structure of Hebrew/Arabic, where identifying the root allows placing all other letters as "prefixes," "suffixes," or "infixes."


לדוגמא:
יתכנסו
<ית><כנס><ו>
הודעה:
<הו><ידע><ה>



Such decomposition allows for the complete preservation of all semantic contexts in a low-dimensional representation. Small dimensions enable training a Hebrew/Arabic language engine using relatively less data compared to alternatives. The first alternative is, of course, representing each letter by its own token, which is a high-dimensional representation that loses semantic connections and requires a lot of data for training purposes.

# The input space size and its reduction.

Estimated number of possible permutations:

| Location     |  #uniques      | #bits  |  possibilites  |
| :----------- | :------------: |  ----- | :------------: |  
| prefix       |   16           |   4    | ה, מ, א, ת, י, ת, נ, ני, הו, יו, תו, נו, או, לו, לי, הת, נת, ית, ו, |
| roots        |   10648         | 15     | Let's assume 3 letters roots with 22 options per letter using 5 bits per word as upper bound        |
| middle       |   2            | 2      | י, ו
| suffix       |   16           | 4      | תי, תם, תן, נו, ן, ונה, ה, ים, ות, נה, ת, י,                |

With approximately 16 million possible combinations (25 bits), each Hebrew word can be accommodated within a single 32-bit unsigned integer. The remaining 7 bits (128 values) can be utilized for special single character tokens, such as numerals, punctuation, and possibly English characters too.

## Bits oredering from MSB to LSB

| 3rd letter in root | 2nd letter in root | 1st letter in root | infix | prefix | suffix | special chars |
| :----------------- | :----------------- | :----------------- | :---- | :----- | :----- | :------------ |
| 5                  | 5                  | 5                  | 2     | 4      | 4      | 7             |





## Code Usage
shoreshnizer.py has a __main__ script to allow testing and viewing results. The script also creates html tags for color display of words breakdowns. See [html example](samples/1.html) here.



#### License
The code is licensed under MIT, granting you the freedom to use it freely, including for commercial purposes. Feel free to utilize the code as you wish and consider contributing to the development of language models running on edge devices.


![דוגמאת לפירוק](images/shorechnizer2b.png)
