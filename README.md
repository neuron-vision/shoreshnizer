# Hebrew/Arabic semantic tokenizer utilizing root based words.
The tokenizer assumes that a large number of words in Hebrew and Arabic can be decomposed into a representation consisting of four subclasses of letters (clusters): Prefix, Root, Infix, and Suffix (Abbreviated as PRIS).
The initial step for the tokenizer involves identifying the indices of the root letters, which then enables the deterministic clustering of all the remaining letters. To avoid ambiguity that can only be resolved within a specific context, the tokenizer should refrain from assigning explicit roles, such as time, body, or בניין, to each clustered letter.



# Motivation

This decomposition method ensures that the full semantic context is retained in a compact representation. By using a low-dimensional approach, it becomes feasible to train a Hebrew/Arabic language model with a smaller amount of data compared to other options. The primary alternative approach involves representing each letter as an individual token, resulting in a high-dimensional representation that lacks semantic connections and necessitates a larger training dataset. However, for cases that don't conform to this approach, we can still resort to character-based tokens, which is the default fallback method for non-English languages.

# Intuition
When teaching children to read unfamiliar words, we encourage them to begin by guessing the word's root. The root of a word holds the majority of the information within the sentence. Once the root is determined, we can then comprehend how the non-root letters contribute to the overall meaning of the sentence.



# PRIS Abbreviation Key: 
|  Cluster Mark  |  Cluster name        |  Allowed length  | Remarks  |
|  ------------  |  ------------        |  --------------- | ---------|
| <\P>           | Prefix               |   0..6           |          |
| <\R1>          | 1st root letter      |   0..1           | First root letter might drop |
| <\I1>          | Infix letter         |   0..2           |     יו    |
| <\R2>          | 2nd letter           |   1              |           |
| <\I2>          | Infix letter         |   0..2           |   יו      |
| <\R3>          | 3ed root letter      |   1              |           |
| <\S>           | Suffix               |   0..7           | לכנה      |


Total: 48 possible legal indices arrangements


# Examples:

| Word | P         | R1 | I1 | R2 | I2 | R3 | S         |  Root Prediction Result |
| :------------: | :-:       | :-: | :-: |  :-: | :-: | :------------: | :-: | :-: | 
|ולכשהתפוצצויותיהם | ולכשהת | פ   | ו   | צ |  | צ   | ויותיהם | 6, 8, 9 |
| יתכנסו |  ית | כ | | נ | | ס | ו | 2, 3, 4 |
| הודעה | הו |  | | ד | | ע | ה | 2, 2, 3 |

# Assumptions
1. Cluster break-down lowers the theoretical numbers of combinations from
> number_of_roots^number_of_prefix^number_of_suffix^number_of_infix 

to 

> number_of_roots * number_of_prefix * number_of_suffix * number_of_infix 

which can fit every word into 32/64 bit.

2. A good tokenizer is a quantization function which reduces dimensionality with minimum signal loss and should be estimated by reconstruction loss.

3. The tokenizer may occasionally split the same root into two different roots due to uncommon linguistic variations. While this is an acceptable error, it results in a slight increase in the size of the dimensionality. However, it is still preferable to the alternative of incorrectly grouping together two unrelated roots.


4. The tokenizer, on its own, lacks the ability to classify clusters beyond the root (prefix, infix, suffix) due to the absence of contextual information. Therefore, it is necessary to delegate this task to the neural network, which can effectively utilize the tokens and employ contextual understanding for accurate classification.



# The input space size and its reduction.

The approximate count of potential permutations:


| Cluster     |  #uniques      | #bits  |  possibilities  |
| :----------- | :------------: |  ----- | :------------: |  
| P       |   16           |   4    | ה, מ, א, ת, י, ת, נ, ני, הו, יו, תו, נו, או, לו, לי, הת, נת, ית, ו, |
| R        |   10648         | 15     | Let's assume 3 letters roots with 22 options per letter using 5 bits per letter as an upper bound        |
| I       |   2            | 2      | י, ו
| S       |   16           | 4      | תי, תם, תן, נו, ן, ונה, ה, ים, ות, נה, ת, י,                |

Given the existence of around 16 million potential combinations (25 bits), it is feasible to represent  Hebrew/Arabic words with roots by using 32-bit unsigned integer. This leaves an additional 7 bits (128 values) that can be allocated for special single character tokens, including numerals, punctuation, and potentially even English characters. We will need to use the other 32 bits (in a 64 bit register) for nouns which cannot be represented by root based decomposition.

## Bits ordering from MSB to LSB

| R1 | R2 | R3 | I | P | S | special chars |
| :----------------- | :----------------- | :----------------- | :---- | :----- | :----- | :------------ |
| 5                  | 5                  | 5                  | 2     | 4      | 4      | 7             |



## Identified challenges:
1. At present, our support is limited to 3-letter roots.
2. Our current support is limited to the Hebrew language until we have Arabic speakers involved in the project.
3. The representation for nouns is not yet supported and will require a transition from the current 32-bit representation to a 64-bit representation.
4. Quantization of prefixes and suffixes requires real data to achieve optimal performance.
5. We still need to establish a training process for the autoencoder to measure reconstruction error.
6. The current root predictor is a temporary solution and will require a substantial dictionary for future training.
7. Our current support for special characters is restricted to 128 characters, and expanding from 32 bits to 64 bits will enable accommodating all of them.

# Related Publications:

| Name          | Description       | Link   |
| :-----------  | :------------:    |  ----- |
| SHOROSHIM     | An extremely comprehensive English-language thesaurus of over thirty-three hundred Hebrew verb roots (Shoroshim) from all historical periods dating from the Biblical through modern times.              |  [PDF](https://halakhah.com/rst/shoroshim.pdf) |



## Code Usage

The rootenizer.py file includes a main script that enables testing and viewing of results. Additionally, the script generates HTML tags for displaying word breakdowns with color formatting. You can refer to the [html example](samples/1.html) to see a demonstration.

For developer documentation, please consult the [Code README](rootenizer/README.md) It provides detailed information and instructions for developers working with the code.

## License
The code is licensed under MIT, granting you the freedom to use it freely, including for commercial purposes. Feel free to utilize the code as you wish and consider contributing to the development of language models running on edge devices.


![דוגמאת לפירוק](images/shorechnizer2b.png)
