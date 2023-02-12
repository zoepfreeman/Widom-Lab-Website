from pubmed_lookup import PubMedLookup, Publication
import requests
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# def create_dic(keyword): 
#     ids=requests.get(f'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={keyword}&retmode=json&sort=pub_date&retmax=5').json()
#     id_list=ids['esearchresult']['idlist']
#     email='junkmail1898@gmail.com'
#     pub_dic={}
#     for i in range(len(id_list)):
#         url='http://www.ncbi.nlm.nih.gov/pubmed/'+id_list[i]
#         lookup = PubMedLookup(url, email)
#         publication = Publication(lookup)
#         pub_dic[i]={'title':publication.title,'authors':publication.authors,'journal':publication.journal,'year':publication.year,'month':publication.month,'url':publication.url,'pubmed':publication.pubmed_url,'abstract':repr(publication.abstract)}
#     return pub_dic

# RNA_dict=create_dic('RNA')
# FRET_dict=create_dic('FRET')
