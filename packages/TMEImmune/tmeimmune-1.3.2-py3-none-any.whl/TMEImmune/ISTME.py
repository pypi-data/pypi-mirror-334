
import pandas as pd
import numpy as np
import warnings
from TMEImmune import nb_utilities as nbu

class ISTME_signature:
    def __init__(self):
        self.immune = ['CD40LG','THEMIS','PYHIN1','TRAT1','FCRL1','SPIB','GPR174','SH2D1A','CCR4','ITK','FCRL3','C5orf20','FIGF','UBASH3A','MS4A1','CD300LG','SAMD3','ADH1B','GZMK','CHRDL1','ABI3BP','FCER2','TIFAB','P2RY12','CLEC10A','RSPO2','PCDH15','HLA-DOA','PLA2G2D','CLEC17A','CD3G','CCL19','PTPRC','C17orf87','GRIA1','CD8A','PRG4','P2RY13','SFTPC','HLA-DPB1','AADAC','EOMES','AOAH','CD1E','CCR2','CCL5','GFRA1','TFEC','CLDN18','FGL2','C4orf7','CD1B','GZMA','HLA-DPA1','SCARA5','PLEK','ZNF683','CD19','HLA-DRA','CD84','PIK3CG','NCKAP1L','CR1','WIF1','CLEC12A','KIAA0408','PIGR','CXCL13','CD74','TLR8','CHIT1','IL7R','HLA-DRB1','HLA-DQA1','COL6A6','LYZ','SFTPA2','CYBB','COL29A1','LCP1','IGJ','UBD','HLA-DQA2','CXCL9','PPYR1','IFNG','MRC1','FAM26F','B2M','CD1A','HLA-B','GBP5','ADAMDEC1','LAPTM5','C1QB','ITGB2','C1QA','SUCNR1','MARCO','HLA-C','VSIG4','F13A1','CXCL10','C1QC','HLA-A','CD163','FCGR3A','TMSL3']
        self.stromal = ['MDK','RPL8','S100P','FTH1','GPR87','UBC','CLDN3','FGL1','TMSB10','HSPB1','ACTB','ITPKA','KRT19','S100A2','EEF1A2','PABPC1','RPLP0','HSP90AB1','NMU','KRT8','KRT7','EPCAM','YWHAZ','MYH9','ACTG1','NPW','MMP13','TUBA1B','ERRFI1','DSP','KRT18','P4HB','ENO1','PKM2','RHOV','ALDOA','JUP','LDHA','HMGA1','HSPA1A','MIF','TUBB','HMGB3','CYP24A1','TPI1','FAM83A','RECQL4','FN1','VEGFA','GAPDH','TK1','TUBB3','UBE2C','MYBL2','COL3A1','COL1A1','COL1A2','COL11A1']
    def get_signature_data(self):
        geneset = {"IS_immune": self.immune, "IS_stromal": self.stromal}
        return geneset

def istmeScore(df):
    """
    Perform ssGSEA and compute the ISTME stromal and immune score
    df: normalized gene expression matrix, with gene symbol as the first column or index
    index: whether gene symbols are the row indices of df
    output: a pandas dataframe with two columns, 
        index: sample ID; 
        IS_immune: ISTME immune score; 
        IS_stromal: ISTME stromal score
    """
    signature = ISTME_signature()
    geneset = signature.get_signature_data()
    score = nbu.ssgsea(df, geneset = geneset, score = "ISTME")

    return score


def get_subtypes(score, immune_q = 0.5, stromal_q = 0.5):
    """
    Get four TME subtypes
    """
    warnings.filterwarnings('ignore')
    score["group"] = [0]*score.shape[0]
    immune_quantile = score['IS_immune'].quantile(q = immune_q)
    stromal_quantile = score['IS_stromal'].quantile(q = stromal_q)

    score.loc[(score['IS_immune'] <= immune_quantile) & (score['IS_stromal'] <= stromal_quantile).to_list(),'group'] = "immune_L, stromal_L"
    score.loc[(score['IS_immune'] > immune_quantile) & (score['IS_stromal'] <= stromal_quantile).to_list(),'group'] = "immune_H, stromal_L"
    score.loc[(score['IS_immune'] <= immune_quantile) & (score['IS_stromal'] > stromal_quantile).to_list(),'group'] = "immune_L, stromal_H"
    score.loc[(score['IS_immune'] > immune_quantile) & (score['IS_stromal'] > stromal_quantile).to_list(),'group'] = "immune_H, stromal_H"

    return(score)
