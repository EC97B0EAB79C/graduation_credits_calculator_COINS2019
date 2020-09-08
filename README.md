# graduation_credits_calculator_COINS2019
 Graduation credits calculator for University of Tsukuba COINS 2019
 
## WARNING
This calculator is not ready to be called perfect, please only use this for assistance.
Since there are only a few test cases, sending your case with the method mention below is appreciated. If you find some special cases that are unimplemented, please send your case as a sample.
 
## How To Use
 1. Download your grades from [Twins](https://twins.tsukuba.ac.jp/) -> 成績 -> 成績照会 -> ダウンロード, with format of CSV
 2. Move the file (usually named SIRS*_STNB*.csv with *_STNB* replaced with your student id) to the same directory with GCC_COINS2019.py(.\GCC_COINS2019\GCC_COINS2019)
 3. The setting has been set for undergraduate CS major for the University of Tsukuba.
 4. Run command
 ```
 .\GCC_COINS2019.py --fname .\SIRS_STNB.csv
 ```
 
 ## Sending Cases
 If you find any unimplemented case sending your case with an explanation is appreciated.
 Please send your grade CSV file with your **Student ID, NAME DELETED** and **ALL GRADES changed to 'P' for passed courses and 'D' for failed ones** and send to dokkaebi@coins.tsukuba.ac.jp.
 
 ## Technology
 Graduation credits calculator is bases on 
 * python 3.7
 * SQLite3
 * Regular Expression
 
 This program reads your grade CSV file, checks for passed courses, read graduation requirement DB according to your department, classify your passed courses, calculates total units fulfilled, and show the result.
 