""""
code to get 15 conserved gene of bacteria then orthologous group
then orthologous gene in each orthologous group
then convert to ncbi then get sequence of each ncbi gene.
"""
import json
import requests

# subfunction to get 15 conserved gene of eco organism (bacteria)
def get_conseved_gene(org):
    p = requests.get('http://rest.kegg.jp/find/genes/'+org+'+conserved')  # conserved gene of organism using kegg api
    con_gene_id_list = []
    for line in p.text.rstrip().split('\n'): # remove space and split line and then seperate each element by tap to separate first element from second
        kg = line.split('\t')[0] # extract first item ( kegg gene id) from line and append it to list
        con_gene_id_list.append(kg)
    return con_gene_id_list
# subfunction to get orthologous group of each conserved gene above
def getOrthGene(gene_list):
    ko_genes=[]
    for gene in gene_list:
        try:          # avoid gene don't have orthologous one in kegg data base and make loop continue
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
# subfunction to get orthogous gene in each orthology group
def orthKoDict(list):
    o_dict={}
    for n in list:
        try: # avoid gene don't have orthology one in kegg data base and make loop continue
            g=requests.get('http://rest.kegg.jp//link/genes/'+n[3:]) # get orthologies gene for each ko from kegg database
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

# subfunction to convert from orthologies gene (output from above) to ncbi gene id to can get sequence of this genes from Entrez NCBI.
def ncbi_gene_id_conv(gene_list):
    j=[]
    for i in gene_list:
        try:  # avoid that orthologygene don't have ncbi id in kegg data base and make loop continue
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
con_gene_id_list=get_conseved_gene(org) # see subfunction detail above
# print(con_gene_id_list)
ko_genes_list = getOrthGene(con_gene_id_list[1:15]) # see subfunction detail above
#print(ko_genes_list)
o_dict=orthKoDict(ko_genes_list) # see subfunction detail above
#print(type(o_dict))
ncbi_dict=o_dict.copy()
for m,v in o_dict.items(): # extract orthogous gene list from dictionary to can convert it to ncbi gene ids
    u= ncbi_gene_id_conv(v)
    ncbi_dict[m]=u
print(json.dumps(ncbi_dict,indent=4)) # easy to show

# get sequence fron Entrez ncbi database of each orthologies gene
from Bio import Entrez
Entrez.email = 'hendgooonet@hotmail.com'
import time
from Bio import Entrez, SeqIO
#ncbi_dict={'ko:K10875': ['7247141', '4816519', '6497163', '6613185', '6739181', '6526655', '6562163', '6576868', '6634100', '6038603', '8233115', '8035003', '172728', '25341357', '6098805', '9940284', '20197664', '20246929', '8342795', '24596435', '36342459', '5507503', '5499561', '9321366', '9316713', '9319586', '9328354', '9320236', '9316447', '9311653', '18013778', '18021272', '18021868', '18017069', '18025833', '18029436', '18043520', '18035021', '18034979', '18048134', '18044758', '18616881', '18642454', '18637031', '18623665', '25498158', '25499905', '25499907', '25499908', '25497866', '25494466', '25493137', '11435042', '11408204', '11441869', '11440844', '25484660', '9663405', '9653729', '9632200', '9640489', '5728084', '9620759', '9617314', '25739034', '5003492', '9831530', '9684693', '9684071', '17044002', '17353537', '23612590', '4620739', '2896840', '34715884', '5546039', '11497887', '11531043', '14494790', '13885235', '8200197', '5124184', '18871523', '5232801', '3636192', '8297764', '14540697', '18245914', '8497388', '28877131', '30033453', '10808816', '11516202', '11511264', '18258936', '2676424', '19323250', '27662682', '23555004', '9679172', '18483175', '19244448', '19258749', '18163232', '28884449', '9537223', '20703773', '19270862', '5482850', '5431537', '18762750', '28825610', '19461923', '3508475', '4983370', '7917093', '4700353', '26232850', '4566920', '9691008', '9096151', '22583920', '8438085', '9521556', '9578794', '9583595', '5970732', '19146591', '19136124', '19120010', '29111614', '13401574', '19331808', '19114953', '9186360', '10191339', '18498240', '19413978', '18844199', '18909628', '18797971', '18882747', '18680385', '19305678', '6071074', '6009842', '9594665', '19211194', '18816991', '18472014', '23562915', '19314721', '5855522', '13540555', '18932810', '5893238', '16079097', '8623874', '10503243', '14875452', '3407677', '5879648', '14891969', '14921180', '2655325', '34860036', '3498264', '3426642', '7318503', '5471511', '14691092', '3503495', '15803261', '5479120', '24425419', '3371603', '7898412', '7198237', '7202815', '7447887', '7443308', '20228280', '20220987', '20223759', '20228492', '17362113', '9476897', '20656159', '20663504', '24127699', '17262933', '17257800', '19046390', '17305696', '17305189'], 'ko:K02607': ['7215281', '7214569', '34794', '4816621', '6497089', '6732262', '6527556', '6561703', '6576488', '6634341', '1270475', '6053092', '8237347', '177964', '25345752', '6101451', '9938414', '10903008', '20215350', '20246170', '8346198', '24597195', '20317347', '36338945', '5503225', '6753626', '9305477', '18019908', '18046004', '18622011', '11426931', '9656781', '9636996', '9622723', '25737015', '5001023', '9832968', '8240646', '9680390', '17044735', '17358320', '23613422', '16994614', '17087269', '17318117', '4622493', '11469570', '2892429', '34713800', '5547414', '11528854', '11534793', '14493110', '11501914', '13884410', '8197394', '18870788', '5232473', '3645737', '8296240', '14540318', '8049355', '8499666', '30036044', '10804122', '11522143', '11509359', '18254664', '2676557', '19321808', '27663829', '23559090', '20369268', '30068866', '28955146', '18487554', '19252359', '19259606', '28887045', '9533347', '20711474', '19274344', '5487485', '5430008', '18761423', '28820914', '4978345', '7912082', '4590750', '26234653', '24164666', '9695117', '9093232', '22586677', '8444804', '9520555', '9584004', '5445514', '5972832', '19152613', '19123163', '29121518', '13398483', '19334857', '9186909', '10187229', '18497930', '19408400', '18844454', '18908001', '18799821', '20673862', '18878122', '18672937', '19304641', '6075111', '6075110', '6075040', '9378889', '9594339', '19204450', '18821684', '18475013', '20374234', '23562287', '19318218', '5853815', '10539290', '18935308', '5889796', '16071152', '8629126', '14922483', '15807103', '7837001', '9465938', '24126115', '17255498', '17290345', '4769882', '4755543'], 'ko:K13431': ['7218360', '4815407', '6503103', '6617628', '27208499', '6525070', '6566057', '6585109', '6634546', '1271053', '6036876', '8229879', '8032534', '8043889', '185438', '6098685', '10908575', '20215710', '20233457', '29830071', '24597586', '20318948', '36336071', '5518191', '6759120', '9305441', '18031013', '18053820', '18620675', '18635025', '11442690', '9632024', '9635365', '5717607', '9618714', '25733343', '5000172', '9832715', '8246371', '9685309', '17041430', '17356238', '16992811', '17085311', '4618637', '11468759', '2892040', '34715693', '5547201', '11527361', '11496496', '11531532', '14493556', '11503970', '13882874', '8199067', '4836684', '18872089', '5231984', '3636513', '8298720', '8048381', '18249644', '8498417', '28878396', '10810106', '11505671', '2682794', '19326278', '27665270', '23555772', '20368644', '30060153', '28945190', '9671100', '18489146', '19252677', '18165360', '28882365', '28882366', '9533828', '20703325', '19274936', '5489674', '5432207', '18763237', '28821192', '19461656', '3505082', '4987768', '7920705', '4702236', '4584106', '26230036', '4558197', '9697586', '9096762', '22583789', '8437464', '9521725', '9582125', '5446055', '29115120', '13399292', '19341236', '19116840', '19021696', '10187455', '18493531', '19410745', '18842137', '18907900', '20671032', '18886325', '18679873', '19303645', '6073983', '9378899', '9595524', '19211872', '18820428', '18471944', '20375328', '23562332', '19318363', '5854135', '10542214', '18927495', '859779', '9699410', '13468305', '20564433', '5889384', '16077449', '8620992', '10505363', '14866311', '3406986', '5878999', '14883291', '14913278', '814309', '3790627', '3497956', '3426542', '7321728', '5475747', '14693483', '20714563', '15805919', '5479908', '24424462', '3374225', '7899766', '7827326', '7202662', '7447888', '20221754', '17360229', '9467566', '20662794', '17281584', '17277700', '17277701', '17296153', '5655648', '5073763', '13388373', '13448477', '5419975', '8857270', '5702158'], 'ko:K10878': ['6494579', '6609948', '6621169', '6735265', '6530937', '6559584', '6580030', '1271049', '6034453', '8230584', '8038444', '191771', '25343664', '6101218', '9948118', '20216172', '20245356', '8350757', '24595786', '9321015', '9309136', '9323991', '18009701', '18025174', '18019114', '18046432', '18038910', '18055129', '18624255', '18638119', '18626079', '11437108', '11434102', '11438542', '11442500', '9634215', '9653055', '9662731', '9648722', '9640370', '9639741', '9639665', '9640793', '9620336', '25739059', '25727863', '5002077', '9834438', '9836295', '8243283', '9681987', '9682507', '17040446', '17043914', '17353645', '17353974', '23614157', '23616048', '16996586', '17089603', '17317929', '17323980', '4620270', '11470096', '2893143', '34717019', '5542429', '11527389', '11496111', '11533888', '14492699', '11501444', '13886626', '8197162', '4838374', '5127923', '18871897', '3643873', '14539346', '8046312', '8500041', '10807101', '11521363', '2682279', '27668144', '23553100', '20361649', '30062629', '28949324', '9665698', '18171529', '20710822', '19272715', '5493992', '18758630', '28820457', '19465583', '3505526', '7920448', '4708588', '4593138', '26233669', '4562007', '9695406', '9097091', '22585938', '8444168', '5449912', '5982585', '19131003', '19128756', '29115245', '13394831', '19331100', '19116887', '10185532', '19413866', '18837134', '18920947', '18806363', '20670629', '18884626', '18680179', '19305835', '6073174', '6007228', '9588330', '19207578', '18473985', '20376628', '19320101', '10547315', '10532110', '18922298', '858943', '9698999', '13468021', '20521173', '5892801', '16077872', '3409001', '14887284', '8444997', '3791756', '3801893', '3497657', '3497971', '3428092', '7319604', '7323265', '5471283', '5476576', '14691725', '14695388', '15806736', '24423672', '24423908', '3374512', '7844539', '7196214', '7444204', '7443515', '20222203', '20223435', '9476767', '20658629', '24140738', '19046578', '17260581', '17292968', '8860845', '4747758', '5699481'], 'ko:K10877': ['7214233', '8234806', '8031331', '190999', '25355084', '6097544', '9946787', '10897228', '20230587', '20323340', '5510937', '6755697', '9635971', '9652322', '5717493', '5718907', '9627870', '25738841', '9831910', '8240718', '17043867', '17356432', '17356695', '17326779', '4622748', '11470773', '2895105', '34714659', '5543153', '11525388', '11494386', '11531903', '14497388', '11502352', '13884954', '8196516', '4839521', '5128306', '18875344', '5232932', '8296376', '14539595', '8046455', '18250057', '8495408', '28880182', '5482580', '5438090', '18757150', '28820248', '19464519', '3509904', '4977926', '7913140', '4701220', '4592157', '26228876', '4564293', '9694399', '9099386', '22587045', '8443229', '9523645', '9578115', '5445382', '19151832', '19128548', '29118221', '19337967', '19023671', '9186234', '18492823', '19417826', '18833644', '18919589', '18798313', '20666812', '18880794', '18671254', '19301619', '6073544', '9379224', '9594239', '19198289', '18475308', '20377175', '23564071', '19315378', '5853432', '10528920', '18928837', '18934650', '5890361', '8624946', '14871530', '14915527', '7829178', '20226499', '5069332', '13390853', '8851119'], 'ko:K02604': ['7215869', '4801647', '6499026', '6606455', '6728155', '6537371', '6575418', '6635186', '1271764', '6038195', '8231519', '8051441', '25342164', '6098231', '9938807', '20217854', '20238729', '8353308', '24589606', '20314339', '36341257', '5514310', '9317582', '18026969', '18038414', '18640123', '11409205', '9644057', '9637439', '5718955', '9626601', '5005251', '34946453', '8244190', '9686454', '17038118', '17351865', '23611971', '16997443', '17085376', '17318533', '4622992', '11468419', '2895581', '34716106', '5542472', '11525564', '11494540', '11531861', '14496389', '11502369', '13884959', '4839598', '5128310', '18873207', '5230675', '3641238', '8301632', '14539618', '8046462', '8495670', '28880171', '30036331', '10805659', '11521143', '18260546', '2680558', '19327650', '27667010', '23553264', '20359500', '30062797', '28949496', '9665549', '18484381', '19253248', '19262689', '18169717', '28890230', '9534611', '20702773', '19274650', '5494419', '5435545', '28820790', '19464601', '3511117', '4980421', '7912546', '4706494', '4586431', '26233537', '4561797', '9695041', '9094047', '8437206', '9520709', '9581109', '5448572', '5982404', '19142928', '19137602', '19122346', '29119026', '13402691', '19337721', '19107615', '19026337', '9185758', '10185413', '18498679', '19420831', '18913522', '18803576', '18886868', '18669748', '6082899', '6016995', '9591055', '19202201', '18473065', '20374812', '23563264', '5853889', '10546487', '18926001', '859878', '9699499', '13466644', '20564532', '5892549', '16072271', '8617339', '10506859', '14875989', '14914153', '2655193', '3830452', '3498589', '3421671', '7318538', '5472686', '14691149', '3502800', '20713000', '15807048', '5476866', '24425549', '3372894', '7893966', '7830688', '7196189', '9471778', '20642384', '24128277', '17255726', '8850387', '5468834'], 'ko:K03108': ['7243375', '4800530', '6499476', '6619246', '6727321', '6535817', '6568591', '6575054', '6629992', '6052041', '6051112', '8025822', '173625', '25356821', '6104278', '9937892', '20216322', '20231094', '29830878', '29831036', '24594299', '20327212', '36338764', '5519783', '9323204', '9323201', '18009233', '18043762', '18043763', '18638293', '25501703', '9654233', '5728458', '9617924', '25729520', '8246413', '9685554', '17043349', '23612234', '16996462', '17085086', '17319151', '4621674', '11471813', '34716531', '5545224', '11526721', '11499217', '11531505', '14493318', '11500976', '8196886', '4838571', '5124052', '18874678', '5231017', '3639169', '8298365', '14541636', '8048568', '18250446', '30038074', '10807181', '11523974', '11510414', '18256919', '2685077', '27667053', '23549311', '20367734', '30065164', '28946292', '9671682', '18483574', '19250746', '19257955', '18165987', '28882723', '9528966', '20706030', '19273367', '5486332', '5431231', '18765056', '19466897', '3508938', '4991093', '7919307', '4703921', '4593975', '26230813', '4565752', '9696413', '9093087', '22587250', '8442783', '9524556', '9578216', '5449537', '5980143', '19146812', '19134123', '19121780', '29119348', '13404194', '19331604', '19108638', '9186207', '10187661', '18498058', '19412203', '18843835', '18908745', '18806394', '20671700', '18886404', '6077201', '9378833', '9593113', '18818423', '18472019', '20376391', '10529567', '5887760', '16078976', '8628138', '10501540', '14873597', '14919046', '3503227', '20713126', '15803755', '5477309', '24423873', '3372067', '7844935', '7194697', '7451889', '17362922', '17361126', '9471978', '20644213', '24141563', '17284324', '17289514', '5068451', '13386069', '13447762', '5414747', '8859581', '4770015'], 'ko:K02606': ['7241013', '37970', '6494402', '6618885', '6736136', '6532121', '6560425', '6578713', '6626785', '1270041', '8231932', '8024770', '6099296', '9944692', '10911457', '20216951', '20241863', '24590522', '20322398', '5514776', '6757750', '18016077', '18053470', '18624755', '25485446', '9636011', '9631619', '5722793', '9617436', '25736500', '9833621', '8248166', '9686920', '17044133', '17353391', '23616663', '16998025', '17086390', '4619236', '11472490', '2892583', '34718019', '5543771', '11529205', '11494034', '11535773', '14498237', '11500920', '13882472', '8198008', '4839075', '5124179', '18871479', '5231834', '3637753', '8299827', '14538131', '18248798', '8495692', '28873897', '30036208', '10807524', '11517950', '11508353', '18257359', '5051166', '19325487', '27665108', '23553368', '20359563', '30064113', '28950118', '9668832', '18485743', '19245599', '19260596', '18169217', '9530974', '20702149', '19269271', '5485116', '28819650', '19471666', '3513038', '4978800', '7911025', '4707688', '4587146', '26229388', '4559489', '9690605', '9094847', '22581008', '8441540', '9520181', '9576942', '5443786', '5980785', '19152446', '19132702', '19117918', '29118211', '13396848', '19330133', '19113211', '9182188', '10186169', '19413897', '18920606', '20678072', '18875543', '19308100', '6072019', '6007686', '9585828', '19209512', '18472923', '20375836', '23561946', '19317613', '5856387', '10533861', '18934200', '858780', '9698855', '13467702', '20521008', '5888476', '16067847', '8618071', '10502080', '14876045', '14916504', '3502153', '20714546', '15807064', '5479924', '7823391', '9474739', '20656700', '24140854', '17285470', '17269442', '8863840', '5465622', '5702189']}
for k,g in ncbi_dict.items():
     # print(k)
     # print(type(k))
     # print(g)
     # print(type(g))
     handle = Entrez.efetch(db="nucleotide", id=g, rettype="fasta", retmode="text")
     record = handle.read()
     out_handle = open('%s.fasta' % str(k[3:]), 'w+')
     out_handle.write(record.rstrip('\n'))