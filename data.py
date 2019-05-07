import requests
import json
# from get_conserved_gene import get_conseved_gene
# from getOrthGene import getOrthGene

import requests
def get_conseved_gene(org):
    p = requests.get('http://rest.kegg.jp/find/genes/'+org+'+conserved')  # conserved gene of organism using kegg api
    con_gene_id_list = []
    for line in p.text.rstrip().split('\n'): # remove space and split line and then seperate each element by tap to separate first element from second
        kg = line.split('\t')[0] # extract second item ( kegg gene id) from line and append it to list
        con_gene_id_list.append(kg)
    return con_gene_id_list

# import requests
# import re
# #gene_list=['dosa:Os03t0165266-00', 'dosa:Os07t0692500-01', 'ctp:CTRG_00701', 'ctp:CTRG_06071']
def getOrthGene(gene_list):
    ko_genes=[]
    for gene in gene_list:
        try:
            orth = requests.get('http://rest.kegg.jp/link/ko/'+gene) # get orthology of gene from kegg data base
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
        if (orth.text and not orth.text.isspace()):
            line= orth.text.rstrip()
            kg = line.split('\t')[1]  # extract second item ( kegg gene id) from line and append it to list
            ko_genes.append(kg)
    return ko_genes



def orthKoDict(list):
    o_dict={}
    for n in list:
        try:
            g=requests.get('http://rest.kegg.jp//link/genes/'+n[3:])
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
        if (g.text and not g.text.isspace()):
            d= []
            for line in g.text.rstrip().split("\n"):
                if "_" in line:
                    k=line.split()[1]
                    d.append(k)
            o_dict[n]=d
    return o_dict


def ncbi_gene_id_conv(gene_list):
    j=[]
    for i in gene_list:
        try:
            ncbi_g = requests.get('http://rest.kegg.jp/conv/ncbi-geneid/'+i) # from keggapi to get ncbi gene id for each kegg gene id
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error. Make sure you are connected to Internet. Technical Details given below.\n")
            print(str(e))
            continue
        except requests.Timeout as e:
            print("OOPS!! Timeout Error")
            print(str(e))
            continue
        except requests.RequestException as e:
            print("OOPS!! General Error")
            print(str(e))
            continue
        except KeyboardInterrupt:
            print("Someone closed the program")
        if (ncbi_g.text and not ncbi_g.text.isspace()):
            j.append(ncbi_g.text.rstrip("\n").split(':')[2]) # extract second item ( ncbi gene id) from line and append it to list
    return j
org="eco"
o_dict={}
con_gene_id_list=get_conseved_gene(org)
print(con_gene_id_list)
ko_genes_list = getOrthGene(con_gene_id_list[1:10])
print(ko_genes_list)
o_dict=orthKoDict(ko_genes_list)
print(type(o_dict))
# gene_list=['dosa:Os03t0165266-00', 'dosa:Os07t0692500-01', 'ctp:CTRG_00701']
# print(ncbi_gene_id_conv(gene_list))
ncbi_dict=o_dict.copy()
for m,v in o_dict.items():
    u= ncbi_gene_id_conv(v)
    ncbi_dict[m]=u
print(json.dumps(ncbi_dict,indent=4))
