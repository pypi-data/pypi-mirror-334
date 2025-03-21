import numpy as np 
import pandas as pd
#import gseapy as gp
from collections import defaultdict
from sklearn.preprocessing import StandardScaler
from TMEImmune import data_processing
from joblib import Parallel, delayed


class nb_pathway():
	def __init__(self):
		self.gene_set = data_processing.load_data("gene_sets_full.json")
    
	def reactome_geneset(self):
		return self.gene_set
	

class netbio_data:
	def __init__(self, gene, clin, response, ssgsea = None):
		self.gene = gene
		self.clin = clin[~clin[response].isna()]
		self._ssgsea = ssgsea
		self.response = response
		self.common_id = list(set(gene.columns) & set(clin.index))

	def get_gene(self, gene_id):
		gene_columns = [gene_id] + self.common_id
		return self.gene[gene_columns]
	
	def get_clin(self):
		clin = self.clin.loc[self.common_id,:]
		if clin[self.response].isin(["R", "NR"]).all():
			clin_resp = clin[self.response].apply(lambda x: 1 if x == "R" else 0)
		elif clin[self.response].isin([0,1]).all():
			clin_resp = clin[self.response]
		else:
			raise ValueError("Unsupported response type")
		return clin_resp
	
	def get_ssgsea(self):
		ssgsea_result = self._ssgsea
		ssgsea_gene = self.gene.iloc[:,1:]
		ssgsea_gene.index = self.gene.iloc[:,0]
		if self._ssgsea is None:
			ssgsea_result = ssgsea(ssgsea_gene)

		ssgsea_col = ['pathway'] + self.common_id
		ssgsea_result = ssgsea_result[ssgsea_col]

		return ssgsea_result


## pathway expression and immunotherapy response
def parse_reactomeExpression_and_immunotherapyResponse(dataset, Prat_cancer_type='MELANOMA'):

	edf = data_processing.load_data('Gide/expression_mRNA.norm3.txt')
	epdf = data_processing.load_data('Gide/pathway_expression_ssgsea.txt')
	pdf = data_processing.load_data('Gide/patient_df.txt')
	
	# features, labels
	exp_dic, responses = defaultdict(list), []
	e_samples = []
	for sample, response in zip(pdf['Patient'].tolist(), pdf['Response'].tolist()):
		# labels
		binary_response = response
		if response == 'NR':
			binary_response = 0
		if response == 'R':
			binary_response = 1
		# features
		for e_sample in epdf.columns:
			tmp = []

			if (sample in e_sample) or (e_sample in sample):
				e_samples.append(e_sample)
				responses.append(binary_response)	

	edf = pd.DataFrame(data=edf, columns=np.append(['gene_id'], e_samples))
	edf = edf.rename(columns = {"gene_id": "genes"})
	epdf = pd.DataFrame(data=epdf, columns=np.append(['pathway'], e_samples))
	responses = np.array(responses)
	return e_samples, edf, epdf, responses


def expression_StandardScaler(exp_df):
	'''
	Input : expression dataframe
	'''
	col1 = exp_df.columns[0]
	tmp = StandardScaler().fit_transform(exp_df.T.values[1:])
	new_tmp = defaultdict(list)
	new_tmp[col1] = exp_df[col1].tolist()
	for s_idx, sample in enumerate(exp_df.columns[1:]):
		new_tmp[sample] = tmp[s_idx]
	output = pd.DataFrame(data=new_tmp, columns=exp_df.columns)
	return output


def ssgsea(df, geneset = None, score = "NetBio"):

	if geneset is None:
		# get netbio reactome pathways and corresponding genesets
		gene_set_dict = nb_pathway().reactome_geneset()
		# Remove pathways where the gene list is empty
		gene_set_dict = {pathway: genes for pathway, genes in gene_set_dict.items() if genes}
	else:
		gene_set_dict = geneset

	gene_set_dict = {sig: set(genes) & set(df.index) for sig, genes in gene_set_dict.items()}

	df1 = df.apply(pd.to_numeric)
	df_ranked = df1.rank(axis = 0, method = "average")
	df_ranked = df_ranked.apply(abs)
	num_signatures = len(gene_set_dict)
	num_samples = df_ranked.shape[1]

	sigs = list(gene_set_dict.keys())

    #for sample in range(num_samples):  # Loop through samples
	def compute_sample_es(sample):
		ordered_genes = df_ranked.iloc[:, sample].sort_values(ascending=False)
		ordered_genes1 = ordered_genes.pow(1. / 4)

		gene_lookup = {gene: idx for idx, gene in enumerate(ordered_genes.index)}
		sample_ES = np.zeros(num_signatures)

		for j, sig in enumerate(sigs):  # Iterate over signatures
			hit_genes = gene_set_dict[sig] & set(gene_lookup.keys())  # Find intersection of genes

			if not hit_genes:
				sample_ES[j] = 0
				continue 

			hit_indices = np.array([gene_lookup[gene] for gene in hit_genes], dtype = int)  # Get indices for these genes
			hit_ind = np.zeros(len(ordered_genes), dtype=bool)
			hit_ind[hit_indices] = True
			no_hit_ind = ~hit_ind
			hit_exp = ordered_genes1[hit_ind]

			if np.sum(hit_exp) > 0:
				no_hit_penalty = np.cumsum(no_hit_ind / np.sum(no_hit_ind))
				hit_reward = np.cumsum((hit_ind * ordered_genes1) / np.sum(hit_exp))
				sample_ES[j] = np.sum(hit_reward - no_hit_penalty)

		return sample_ES
	print("-------- Begin ssgsea, might take some time --------")
	results = Parallel(n_jobs=-1)(delayed(compute_sample_es)(sample) for sample in range(num_samples))
	print("-------- Complete computing enrichment score --------")
    # Convert results to a NumPy array
	ES_vector = np.array(results).T  # Transpose to match (pathways x samples) shape
        # Convert back to DataFrame
	ES_df = pd.DataFrame(ES_vector, index=sigs, columns=df.columns)
	ES_df = ES_df.replace(r'^\s*$', np.nan, regex=True)
	ES_df = ES_df.replace("nan", np.nan)
	ES_df = ES_df.dropna(how='all')

	if score == "ESTIMATE":
		return ES_df.T
	elif score == "ISTME":
		# Normalize ES_vector for each row
		nes_df = ES_df.apply(lambda row: row / (row.max() - row.min()) if row.max() - row.min() != 0 else row, axis = 1)
		return nes_df.T
		
	print("-------- Normalizing enrichment score --------")

	any_na = ES_df.isna().any().any()
	if any_na:
		es_range = (ES_df.min().min(skipna=True), ES_df.max().max(skipna=True))
	else:
		es_range = (ES_df.min().min(), ES_df.max().max())

	# check if the range is valid
	if pd.isna(es_range[0]) or pd.isna(es_range[1]) or not np.isfinite(es_range[0]) or not np.isfinite(es_range[1]):
		raise ValueError("Normalizing factor contains NAs or infinite values")

	nes_df = ES_df / (es_range[1] - es_range[0])

	print("-------- ssgsea complete --------")

	NES_df = nes_df.reset_index().rename(columns = {"index": "pathway"})

	return NES_df
