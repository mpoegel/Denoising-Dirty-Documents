# Denoising Dirty Documents
[Kaggle Competition Homepage](https://www.kaggle.com/c/denoising-dirty-documents)

### Objective
Clean the images of text (remove wrinkles, coffee stains, etc) to make them more readable by OCR.

### Data
The data for this competition can be obtained through [Kaggle](https://www.kaggle.com/c/denoising-dirty-documents/data).

### Analysis

#### No Clean Benchmark
| Measure     | Value            |
| :---------- | :--------------- |
| test_error  | 0.20031          |

#### Threshold
Threshold = Median

| Measure     | Value            |
| :---------- | :--------------- |
| threshold   | 0.8627           |
| train_error | 0.1464           |
| test_error  | 0.19025          |

Threshold = Median - Standard Deviation:

| Measure     | Value            |
| :---------- | :--------------- |
| threshold   | 0.645289077544   |
| train_error | 0.00452361737533 |
| test_error  | 0.13335          |
