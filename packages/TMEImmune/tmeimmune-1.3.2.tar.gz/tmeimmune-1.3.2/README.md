# TMEImmune

`TMEImmune` is a Python package that implements the ESTIMATE algorithm, ISTMEscore method, NetBio method, and SIA method. The ESTIMATE and ISTMEscore methods were originally available only in R, and we've ported them to Python for broader accessibility. Additionally, the NetBio and SIA methods, which did not have existing packages, has been manually implemented in Python following the original publications and codes.

## Features

- Implementation of the ESTIMATE algorithm for estimating stromal, immune and estimate scores in tumor samples. Estimate tumor purity for Affymetrix platform data. 
- Implementation of the ISTMEscore method for improved tumor microenvironment (TME) immune and stromal scoring. The ISTME TME subtypes are also provided.
- Novel implementation of the NetBio and SIA method for comprehensive TME analysis.
- Data pre-processing including normalization and batch correction for both unnormalized read counts and normalized data.
- Performance evaluation for immune checkpoint inhibitor response prediction and survival prognosis.

## Requirement

The installation of `TMEImmune` requires python version 3.10 and above.


## Installation

You can install the package via the following two commands:

```bash
pip install TMEImmune
pip install git+https://github.com/ShahriyariLab/TMEImmune
```


## Usage

Here are some basic usage examples:

Example 1:
```
import pandas as pd
from TMEImmune import data_processing, TME_score, optimal

# Step 1: Data Normalization
clin = pd.read_csv("example_clin.csv", index_col = 0)
df = data_processing.normalization(path = "example_gene.csv", method = 'TMM', batch = clin, batch_col = "CANCER")

# Step 2: Compute TME score
score = TME_score.get_score(df, method = ['ESTIMATE','ISTME', 'NetBio', 'SIA'], clin = clin, test_clinid = "response")

# Step 3: Performance comparison
outcome = optimal.get_performance(score, metric = ['ICI', 'survival'], 
                                  score_name = ['EST_stromal','EST_immune','IS_immune', 'IS_stromal','NetBio','SIA'], 
                                  ICI_col = 'response', surv_col = ['time', 'delta'], df_clin = clin)
```

Example 2:
```
gene = pd.read_excel("riaz.xlsx", sheet_name=0, index_col=0)
clin = pd.read_excel("riaz.xlsx", sheet_name=1, index_col = 1)
clin = clin.loc[clin.index.str.contains("Pre", na=False)]
clin['delta'] = clin['Dead/Alive\n(Dead = True)'].apply(lambda x: 1 if x == True else 0)
clin['OS'] = clin['Time to Death\n(weeks)']
df_norm = data_processing.normalization(gene, batch = clin, batch_col = "Cohort")

score = TME_score.get_score(df_norm, method = ['ESTIMATE','ISTME', 'NetBio', 'SIA'], clin = clin, test_clinid = "response")

outcome = optimal.get_performance(score, metric = ['ICI', 'survival'], 
                                  score_name = ['EST_stromal','EST_immune','IS_immune', 'IS_stromal','NetBio','SIA'], 
                                  ICI_col = 'response', surv_col = ['delta', 'OS'], df_clin = clin, name = "Riaz et al.")
```

## Docker Container
For users who prefer a ready-to-use, stable runtime environment, we provide a pre-built Docker container `tmeimmune` that includes all necessary dependencies and configurations for running our package. Below shows an example to pull the image from docker and run it, which returns the same output as Example 1 in previous section.

Pull the docker image:
```
docker pull qiluzhou/tmeimmune:v1.0
```

Run the container using Example 1:
```
docker run --rm -v $(pwd):/app tmeimmune python /app/docker_test.py
```


## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact and contribution
If you have any questions or feedback, feel free to open an issue on GitHub Issues. We also welcome contributions for integrating new TME scores into our package. If you'd like to propose a method, please attach a link to its introduction in the Github issue using the `feature_request` template, and we will evaluate it accordingly. If you encounter any bugs, open an issue on `bug_report`. All the changes we've made can be tracked through the GitHub project `TMEImmune_project`.

## Acknowledgements
The ESTIMATE algorithm from Yoshihara et al.
The ISTMEscore method from Zeng et al.
The NetBio method from Kong et al.
The SIA method from Mezheyeuski et al.

## Citations

If you use `TMEImmune` in your research, please cite the following papers:

Yoshihara, K., Shahmoradgoli, M., Martínez, E. et al. Inferring tumour purity and stromal and immune cell admixture from expression data. Nat Commun 4, 2612 (2013). https://doi.org/10.1038/ncomms3612

Zeng, Z., Li, J., Zhang, J. et al. Immune and stromal scoring system associated with tumor microenvironment and prognosis: a gene-based multi-cancer analysis. J Transl Med 19, 330 (2021). https://doi.org/10.1186/s12967-021-03002-1

Kong, J., Ha, D., Lee, J., Kim, I., Park, M., Im, S. H., ... & Kim, S. (2022). Network-based machine learning approach to predict immunotherapy response in cancer patients. Nature communications, 13(1), 3703. https://doi.org/10.1038/s41467-022-31535-6

Mezheyeuski, A., Backman, M., Mattsson, J., Martín-Bernabé, A., Larsson, C., Hrynchyk, I., Hammarström, K., Ström, S., Ekström, J., Mauchanski, S., Khelashvili, S., Lindberg, A., Agnarsdóttir, M., Edqvist, P. H., Huvila, J., Segersten, U., Malmström, P. U., Botling, J., Nodin, B., Hedner, C., … Sjöblom, T. (2023). An immune score reflecting pro- and anti-tumoural balance of tumour microenvironment has major prognostic impact and predicts immunotherapy response in solid cancers. EBioMedicine, 88, 104452. https://doi.org/10.1016/j.ebiom.2023.104452





