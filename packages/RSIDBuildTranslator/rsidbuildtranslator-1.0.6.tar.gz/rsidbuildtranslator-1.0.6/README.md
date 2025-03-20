# RSIDBuildTranslator

RSIDBuildTranslator is a tool that annotates genetic data with rsIDs, or chromosome and position from GRCh37 or GRCh38, using whichever is available in your data. The database used in this tool is based on GTEx v10 whole genome sequencing variants from 953 individuals, and has a coverage of roughly 48.5M variants. 

This tool can be used on tabular data; for example GWAS summary statistics. It requires only 1 column with rsIDs, or 2 columns with genomic positions in either build GRCh37 or GRCh38 to work.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Examples](#examples)



## Installation

The latest version can be installed using pip, and requires Python version >=3.12.

`pip install RSIDBuildTranslator`

## Usage

Once installed, you can call the program from the command line for viewing all options available.

`RSIDBuildTranslator -h`

RSIDBuildTranslator can be run using 3 different modes; **rsid**, **chrpos37**, and **chrpos38**, dependent on what you have available in your dataframe. For mode specific options you can use the following commands:

```bash
RSIDBuildTranslator rsid -h

RSIDBuildTranslator chrpos37 -h

RSIDBuildTranslator chrpos38 -h
```

### General options:

| Flag | Description |
|-|-|
| -h, --help | Use this flag to retrieve all options and help |
| -i, --input | The name of the input file, with the path to the file (if required). The program can read most types of *delimited* files.
| -o, --output | A name for the output file, with the path where you want to place it (if required). Allowed file extentions are ".txt", ".tsv", and ".csv".
| --exclude-ref-alt (optional) | Include this flag in the command if you would like to exclude printing the "ref" and "alt" alleles from the databse to your output file. The "ref" and "alt" alleles are printed by default.

### Mode specific options:

**`rsid`**

| Flag | Description |
|-|-|
| -rs, --rsid_col | Name of the column with rsIDs in your dataframe.

**`chrpos37`**

| Flag | Description |
|-|-|
| -chr37 | Name of the column with chromosome number in build GRCh37 (hg19) in your dataframe.
| -pos37 | Name of the column with position in build GRCh37 (hg19) in your dataframe.

**`chrpos38`**

| Flag | Description |
|-|-|
| -chr38 | Name of the column with chromosome number in build GRCh38 (hg38) in your dataframe.
| -pos38 | Name of the column with position in build GRCh38 (hg38) in your dataframe.

## Examples

Example for running RSIDBuildTranslator in mode **`rsid`**.

```bash
>head test_data1.txt 
ID	REF	ALT	A1	A1_FREQ	TEST	OBS_CT	BETA	SE	T_STAT	P	ERRCODE
rs116944008	C	T	T	0.0260641	ADD	7213	-0.0243852	0.052663	-0.463043	0.643348	.
rs17151229	G	C	C	0.337446	ADD	7213	0.000517255	0.0174181	0.0296964	0.97631	.
rs75008380	A	G	G	0.0641897	ADD	7213	0.0197173	0.0337571	0.584095	0.559175	.
rs6467145	G	A	G	0.409053	ADD	7213	0.0343268	0.0168576	2.03628	0.0417584	.
rs17151241	A	G	G	0.407597	ADD	7213	0.0340739	0.0168882	2.01762	0.0436681	.

>RSIDBuildTranslator rsid -i test_data1.txt -o test_out1.txt -rs ID
2025-03-17 11:58:01,214 - INFO - Running tool in mode: 'rsid'
2025-03-17 11:58:01,218 - INFO - Input file 'test_data1.txt' read successfully.
2025-03-17 11:58:01,219 - INFO - rsID column 'ID' passed checks with 49 valid IDs ✨
2025-03-17 11:58:01,220 - INFO - GTEx database read successfully.
2025-03-17 11:58:01,231 - INFO - Processed entries 1 to 49...
2025-03-17 11:58:01,234 - INFO - Data cleaned and merged successfully.
Output file head:

    ID REF ALT A1   A1_FREQ TEST  OBS_CT      BETA        SE    T_STAT         P ERRCODE chr37      pos37 chr38      pos38 ref alt
0   rs116944008   C   T  T  0.026064  ADD    7213 -0.024385  0.052663 -0.463043  0.643348       .     7  127381902     7  127741848   C   T
1   rs17151229   G   C  C  0.337446  ADD    7213  0.000517  0.017418  0.029696  0.976310       .     7  127382155     7  127742101   G   C
2   rs75008380   A   G  G  0.064190  ADD    7213  0.019717  0.033757  0.584095  0.559175       .     7  127382169     7  127742115   A   G
3   rs6467145   G   A  G  0.409053  ADD    7213  0.034327  0.016858  2.036280  0.041758       .     7  127382265     7  127742211   G   A
4   rs17151241   A   G  G  0.407597  ADD    7213  0.034074  0.016888  2.017620  0.043668       .     7  127382743     7  127742689   A   G
2025-03-17 11:58:01,239 - INFO - Output file successfully written to 'test_out1.txt' with tab as delimiter.

```

Example for running RSIDBuildTranslator in mode **`chrpos37`**.

```bash
>head test_data2.tsv 
p_value	chromosome	base_pair_location	effect_allele	other_allele	effect_allele_frequency	beta	standard_error
0.400799342119828	1	845635	T	C	0.202	-0.0171282	0.0203843
0.404075947534627	1	845938	A	G	0.2036	-0.0169644	0.0203305
0.35851555231626	1	846078	T	C	0.1952	-0.0189615	0.020649
0.294246292876486	1	846398	A	G	0.203	-0.0213219	0.0203268
0.362153761210013	1	846808	T	C	0.1977	-0.0187402	0.0205631

>RSIDBuildTranslator chrpos37 -i test_data2.tsv -o test_out2.tsv -chr37 chromosome -pos37 base_pair_location
2025-03-17 14:14:19,213 - INFO - Running tool in mode: 'chrpos37'
2025-03-17 14:14:19,215 - INFO - Input file 'test_data2.tsv' read successfully.
2025-03-17 14:14:19,216 - INFO - Chromosome column 'chromosome' and position column 'base_pair_location' passed checks with 99 valid IDs ✨
2025-03-17 14:14:19,216 - INFO - GTEx database read successfully.
2025-03-17 14:14:19,224 - INFO - Processed entries 1 to 99...
2025-03-17 14:14:19,227 - INFO - Data cleaned and merged successfully.
Output file head:

    p_value  chromosome  base_pair_location effect_allele other_allele  ...  standard_error  rsid_dbSNP155  chr38   pos38 ref alt
0  0.400799           1              845635             T            C  ...        0.020384    rs117086422      1  910255   C   T
1   0.404076           1              845938             A            G  ...        0.020331     rs57760052      1  910558   G   A
2   0.358516           1              846078             T            C  ...        0.020649     rs28612348      1  910698   C   T
3   0.294246           1              846398             A            G  ...        0.020327     rs58781670      1  911018   G   A
4    0.362154           1              846808             T            C  ...        0.020563      rs4475691      1  911428   C   T

2025-03-17 14:14:19,232 - INFO - Output file successfully written to 'test_out2.tsv' with tab as delimiter.

```

Example for running RSIDBuildTranslator in mode **`chrpos38`**. Here the flag `--exclude-ref-alt` is used to demonstrate its purpose.

```bash
>head test_data1.txt 
#CHROM	POS	ID	REF	ALT	A1	A1_FREQ	TEST	OBS_CT	BETA	SE	T_STAT	P	ERRCODE
7	127741848	rs116944008	C	T	T	0.0260641	ADD	7213	-0.0243852	0.052663	-0.463043	0.643348	.
7	127742101	rs17151229	G	C	C	0.337446	ADD	7213	0.000517255	0.0174181	0.0296964	0.97631	.
7	127742115	rs75008380	A	G	G	0.0641897	ADD	7213	0.0197173	0.0337571	0.584095	0.559175	.
7	127742211	rs6467145	G	A	G	0.409053	ADD	7213	0.0343268	0.0168576	2.03628	0.0417584	.
7	127742689	rs17151241	A	G	G	0.407597	ADD	7213	0.0340739	0.0168882	2.01762	0.0436681	.

>RSIDBuildTranslator chrpos38 -i test_data1.txt -o test_out2.txt -chr38 CHROM -pos38 POS --exclude-ref-alt
2025-03-17 12:00:43,582 - INFO - Running tool in mode: 'chrpos38'
2025-03-17 12:00:43,584 - INFO - Input file 'test_data1.txt' read successfully.
2025-03-17 12:00:43,585 - INFO - Chromosome column 'CHROM' and position column 'POS' passed checks with 49 valid IDs ✨
2025-03-17 12:00:43,586 - INFO - GTEx database read successfully.
2025-03-17 12:00:43,587 - INFO - Processed entries 1 to 49...
2025-03-17 12:00:43,589 - INFO - Data cleaned and merged successfully.
Output file head:

   CHROM        POS           ID REF ALT A1   A1_FREQ TEST  OBS_CT      BETA        SE    T_STAT         P ERRCODE rsid_dbSNP155 chr37      pos37
0      7  127741848  rs116944008   C   T  T  0.026064  ADD    7213 -0.024385  0.052663 -0.463043  0.643348       .   rs116944008     7  127381902
1      7  127742101   rs17151229   G   C  C  0.337446  ADD    7213  0.000517  0.017418  0.029696  0.976310       .    rs17151229     7  127382155
2      7  127742115   rs75008380   A   G  G  0.064190  ADD    7213  0.019717  0.033757  0.584095  0.559175       .    rs75008380     7  127382169
3      7  127742211    rs6467145   G   A  G  0.409053  ADD    7213  0.034327  0.016858  2.036280  0.041758       .     rs6467145     7  127382265
4      7  127742689   rs17151241   A   G  G  0.407597  ADD    7213  0.034074  0.016888  2.017620  0.043668       .    rs17151241     7  127382743
2025-03-17 12:00:43,593 - INFO - Output file successfully written to 'test_out2.txt' with tab as delimiter.

```