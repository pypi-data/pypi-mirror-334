import numpy as np 
import pandas as pd
import warnings
from collections import defaultdict
import scipy.stats as stat
from sklearn.model_selection import GridSearchCV, StratifiedKFold
#import networkx as nx
from statsmodels.stats.multitest import multipletests
from sklearn.metrics import roc_curve, auc, accuracy_score, f1_score, precision_score, recall_score, precision_recall_curve
from sklearn.linear_model import LogisticRegression
from scipy.special import logit
from TMEImmune import data_processing
from TMEImmune import nb_utilities as nbu

warnings.filterwarnings('ignore')
warnings.filterwarnings(action='ignore', category=DeprecationWarning)
warnings.filterwarnings(action='ignore', category=FutureWarning)


def get_netbio(test_gene, test_clin, test_clinid, test_ssgsea = None, 
			   cohort_targets = {'PD1':['Gide']}, train_gene = None, 
			   train_geneid = "gene_id", train_clin = None, train_clinid = None, train_ssgsea = None, 
			   nGene = 200, qval = 0.01, penalty = "l2"):

	""" 
	train NetBio model and get NetBio score
	test_gene: gene expression dataset, gene symbol must be the first column of the dataset
	test_clin: clinical dataset having treatment response
	test_clinid: column name of treatment response column
	test_ssgsea: whether to perform ssgsea on the gene expression dataset
	cohort_targets: {treatment: training dataset}, by default use Gide et al.'s data to train model
	train_geneid: column of gene symbol in training dataset
	"""
	if train_gene is None:
		train_dataset = "Gide"
		train_geneid = 'genes'
		target = "PD1"
		train_samples, train_edf, train_epdf, train_responses = nbu.parse_reactomeExpression_and_immunotherapyResponse(train_dataset)

	else:
		target, train_dataset = cohort_targets.items
		train_data = nbu.netbio_data(train_gene, train_clin, train_clinid, train_ssgsea)
		train_edf, train_epdf, train_responses = train_data.get_gene(train_geneid), train_data.get_ssgsea(), train_data.get_clin()

	reactome = data_processing.load_data("c2.all.v7.2.symbols.gmt")

	test_data = nbu.netbio_data(test_gene, test_clin, test_clinid, test_ssgsea)
	test_geneid = test_gene.columns[0]
	test_edf, test_epdf, test_responses = test_data.get_gene(test_geneid), test_data.get_ssgsea(), test_data.get_clin()

	### data cleanup: match genes and pathways between cohorts
	#common_genes, common_pathways = list(set(train_edf[train_geneid].tolist()) & set(test_edf[test_geneid].tolist())), list(set(train_epdf['pathway'].tolist()) & set(test_epdf['pathway'].tolist()))
	common_genes, common_pathways = list(set(train_edf[train_geneid]) & set(test_edf[test_geneid])), list(set(train_epdf['pathway']) & set(test_epdf['pathway']))
	train_edf = train_edf.loc[train_edf[train_geneid].isin(common_genes),:].sort_values(by=train_geneid)
	train_epdf = train_epdf.loc[train_epdf['pathway'].isin(common_pathways),:].sort_values(by='pathway')
	test_edf = test_edf.loc[test_edf[test_geneid].isin(common_genes),:].sort_values(by=test_geneid)
	test_epdf = test_epdf.loc[test_epdf['pathway'].isin(common_pathways),:].sort_values(by = 'pathway')


	### data cleanup: expression standardization
	train_edf = nbu.expression_StandardScaler(train_edf)
	train_epdf = nbu.expression_StandardScaler(train_epdf)
	test_edf = nbu.expression_StandardScaler(test_edf)
	test_epdf = nbu.expression_StandardScaler(test_epdf)

	biomarker_dir = 'nb_biomarker'
	bdf = data_processing.load_data('%s/%s.txt'%(biomarker_dir, target))
	bdf = bdf.dropna(subset=['gene_id'])
	b_genes = []
	for idx, gene in enumerate(bdf.sort_values(by=['propagate_score'], ascending=False)['gene_id'].tolist()):
		if gene in train_edf[train_geneid].tolist():
			if not gene in b_genes:
				b_genes.append(gene)
			if len(set(b_genes)) >= nGene:
				break

	tmp_hypergeom = defaultdict(list)
	pvalues, qvalues = [], []
	for pw in list(reactome.keys()):
		pw_genes = list(set(reactome[pw]) & set(train_edf[train_geneid].tolist()))
		M = len(train_edf[train_geneid].tolist())
		n = len(pw_genes)
		N = len(set(b_genes))
		k = len(set(pw_genes) & set(b_genes))
		p = stat.hypergeom.sf(k-1, M, n, N)
		tmp_hypergeom['pw'].append(pw)
		tmp_hypergeom['p'].append(p)
		pvalues.append(p)
	_, qvalues, _, _ = multipletests(pvalues)
	tmp_hypergeom['q'] = qvalues
	tmp_hypergeom = pd.DataFrame(tmp_hypergeom).sort_values(by=['q'])
	proximal_pathways = tmp_hypergeom.loc[tmp_hypergeom['q']<=qval,:]['pw'].tolist() ## proximal_pathways

	train_dic = {}
	test_dic = {}

	train_dic['NetBio'] = train_epdf.loc[train_epdf['pathway'].isin(proximal_pathways),:]
	test_dic['NetBio'] = test_epdf.loc[test_epdf['pathway'].isin(proximal_pathways),:]

	X_train, X_test = train_dic['NetBio'].T.values[1:], test_dic['NetBio'].T.values[1:]
	y_train, y_test = train_responses, test_responses

	# make predictions
	model = LogisticRegression()
	if penalty == 'l2':
		param_grid = {'penalty':['l2'], 'max_iter':[1000], 'solver':['lbfgs'], 'C':np.arange(0.1, 1, 0.1), 'class_weight':['balanced'] }
	if penalty == 'none':
		param_grid = {'penalty':['none'], 'max_iter':[1000], 'class_weight':['balanced'] }
	cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
	gcv = GridSearchCV(model, param_grid=param_grid, cv=cv, scoring='roc_auc', 
			n_jobs=5).fit(X_train, y_train) #cv=5

	pred_proba = gcv.best_estimator_.predict_proba(X_test)[:,1]
	logit_pred = logit(np.clip(pred_proba, 1e-6, 1 - 1e-6))

	return logit_pred
