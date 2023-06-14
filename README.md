# Hebrew/Arabic semantic tokenizer utilizing root based words.
The tokenizer assumes that most words in Hebrew and Arabic can be decomposed into a representation consisting of four subclasses of letters: Prefix, Root, Infix, and Suffix.
The motivation is to utilize the unique structure of Hebrew/Arabic, where identifying the root allows clustering all other letters to "prefix", "suffix", "infix".


For example:

1. יתכנסו:
<ית><כנס><ו>
2. הודעה:
<הו><ידע><ה>


This decomposition method ensures that the full semantic context is retained in a compact representation. By using a low-dimensional approach, it becomes feasible to train a Hebrew/Arabic language model with a smaller amount of data compared to other options. The primary alternative approach involves representing each letter as an individual token, resulting in a high-dimensional representation that lacks semantic connections and necessitates a larger training dataset. However, for cases that don't conform to this approach, we can still resort to character-based tokens, which is the default fallback method for non-English languages.

# Assumptions
1. Cluster break down lowers the theoretical numbers of combinations from
> number_of_roots^number_of_prefix^number_of_suffix^number_of_infix 

to 

> number_of_roots * number_of_prefix * number_of_suffix * number_of_infix 

which can fit every word into 32/64 bit.

2. A good tokenizer is a quantization function which reduces dimensionality with minimum signal loss and should be estimated by reconstruction loss.

3. The tokenizer might separate same root to 2 different roots due to language unusual roots which is an acceptable error thats leads to a slight increase in dimensionality size but is not as bad as grouping 2 unrelated roots together. 

4. The tokenizer alone cannot classify clusters other than the root (prefix, infix, suffix) due to missing context. This task should be left to the neural network that will use the tokens.


# The input space size and its reduction.

Estimated number of possible permutations:

| Location     |  #uniques      | #bits  |  possibilities  |
| :----------- | :------------: |  ----- | :------------: |  
| prefix       |   16           |   4    | ה, מ, א, ת, י, ת, נ, ני, הו, יו, תו, נו, או, לו, לי, הת, נת, ית, ו, |
| roots        |   10648         | 15     | Let's assume 3 letters roots with 22 options per letter using 5 bits per word as upper bound        |
| infix       |   2            | 2      | י, ו
| suffix       |   16           | 4      | תי, תם, תן, נו, ן, ונה, ה, ים, ות, נה, ת, י,                |

With approximately 16 million possible combinations (25 bits), each Hebrew word can be accommodated within a single 32-bit unsigned integer. The remaining 7 bits (128 values) can be utilized for special single character tokens, such as numerals, punctuation, and possibly English characters too.

## Bits ordering from MSB to LSB

| 3rd letter in root | 2nd letter in root | 1st letter in root | infix | prefix | suffix | special chars |
| :----------------- | :----------------- | :----------------- | :---- | :----- | :----- | :------------ |
| 5                  | 5                  | 5                  | 2     | 4      | 4      | 7             |



## Known pitfalls.
1. We only support 3 letters-roots for now.
2. We only support Hebrew for now until arabic speakers will join the project.
3. Support for nouns is still missing and will need to utilize 64bit instead of current 32bit representation.
4. Prefix and Suffix quantization needs real data to perform optimally.
5. Training process for auto encoder to measure reconstruction error is still missing.
6. Root predictor is only a place holder for now and will need a large dictionary for future training.
7. Current special charters support is limited to only 128 charters and increasing from 32 bits to 64 bits will allow accommodating all of them. 




## Code Usage
rootenizer.py has a __main__ script to allow testing and viewing results. The script also creates html tags for color display of words breakdowns. See [html example](samples/1.html) here.
See [Code README](src/README.md) for developers documentation.


#### License
The code is licensed under MIT, granting you the freedom to use it freely, including for commercial purposes. Feel free to utilize the code as you wish and consider contributing to the development of language models running on edge devices.


![דוגמאת לפירוק](images/shorechnizer2b.png)
