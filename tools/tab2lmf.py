#!/usr/bin/env python3

################################################################################
# Luis Morgado da Costa (lmorgado.dacosta@gmail.com)
# Last Modified: August 2019
# License: MIT License (below)
# Files: tab2lmf.py, meta.py (optional)
################################################################################
# Copyright 2019, Luis Morgado da Costa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
################################################################################


################################################################################
# USAGE & NOTES
################################################################################
# 
# Assuming one is using PWN3.0 synset ids, download: ili-map-pwn30.tab
# (https://github.com/globalwordnet/ili/blob/master/ili-map-pwn30.tab)
#
# python3 tab2lmf.py [wnid code] [wn.tab] > wnlmf.xml
# 
# Example:
# python3 tab2lmf.py okwn wn.tab > wnlmf.xml
# 
# The please validate (e.g.):
# xmlstarlet val -e wnlmf.xml
# 
# TODO:
# - turn this into a script that can be used in the command-line (functions) 
# - make ASCII romanization optional 
# - add synset-synset relations... maybe something like:
#   01646866-v  	ssrel:hypo 	01646866-v
# 
################################################################################

import sys, os
from collections import defaultdict as dd
from unidecode import unidecode

################################################################################
# Making sure the number of arguments is either
################################################################################
if (len(sys.argv) <= 2) or (len(sys.argv) > 4):
    sys.stderr.write("\nThis script expects 2 argument:\n")
    sys.stderr.write("[1] the wordnet id code (e.g. pwn, okwn)\n")
    sys.stderr.write("[2] a tsv to produce the LMF from\n\n")
    sys.exit()

elif len(sys.argv) == 3:
    sys.stderr.write("\nThis script was able to find 2 arguments.\n")
    sys.stderr.write("It will assume they are:\n")
    sys.stderr.write("[1] the wordnet id code (e.g. pwn, okwn)\n")
    sys.stderr.write("[2] a tsv to produce the LMF from\n\n")
    wnid = sys.argv[1]
    wnfile_path = sys.argv[2]
################################################################################


ilimapfile ='ili-map-pwn30.tab'


################################################################################
# See if meta.py exists, else create the dictionary here
################################################################################
if os.path.exists('meta.py'):
    from meta import meta
else:
    meta = dd(lambda: dd(str))


meta['okwn'] = {'id':'okwn', 
                'label':'Open Kristang Wordnet',
                'lang':'mcm',
                'email':'lmorgado.dacosta@gmail.com',
                'license':'https://creativecommons.org/licenses/by/4.0/',
                'version':'0.1',
                'citation':"...",
                'url':'http://compling.hss.ntu.edu.sg/kristang/',
                'dc:publisher':"Global Wordnet Association", 
                'dc:format':"OMW-LMF",
                'description':"...",
                'conf':"1.0"}

meta['okwnx'] = {'id':'okwnx', 
                 'label':'Open Kristang Wordnet Extended',
                 'lang':'mcm',
                 'email':'lmorgado.dacosta@gmail.com',
                 'license':'https://creativecommons.org/licenses/by/4.0/',
                 'version':'0.1',
                 'citation':"...",
                 'url':'http://compling.hss.ntu.edu.sg/kristang/',
                 'dc:publisher':"Global Wordnet Association", 
                 'dc:format':"OMW-LMF",
                 'description':"...",
                 'conf':"1.0"}

meta['cantown'] = {'id':'cantown', 
                   'label':'Cantonese Wordnet',
                   'lang':'yue',
                   'email':'neosome@gmail.com, lmorgado.dacosta@gmail.com',
                   'license':'https://creativecommons.org/licenses/by/4.0/',
                   'version':'1.0',
                   'citation':"...",
                   'url':'...',
                   'dc:format':"OMW-LMF",
                   'description':"...",
                   'conf':"1.0"}


meta['copwn'] = {'id':'copwn', 
                 'label':'Coptic Wordnet',
                 'lang':'cop',
                 'email':'laurasla@ifi.uio.no',
                 'license':'https://creativecommons.org/licenses/by/4.0/',
                 'version':'1.0',
                 'citation':"Laura Slaughter, Luis Morgado Da Costa, So Miyagawa, Marco Büchler, Amir Zeldes, Hugo Lundhaug and Heike Behlmer. 2019. The Making of Coptic Wordnet. In Global WordNet Conference 2019 Proceedings, Poland.",
                 'url':'...',
                 'dc:format':"OMW-LMF",
                 'description':"...",
                 'conf':"1.0"}



################################################################################
# Confirm the meta info before moving on
################################################################################
if wnid not in list(meta.keys()):
    sys.stderr.write("\nThere was no meta-info available for this wordnet.")
    sys.stderr.write("\nPlease edit the script and include it.""")
    sys.stderr.write("\nQuitting...\n\n")
    sys.exit()

sys.stderr.write("\nThis is the meta info found for this wnid.\n\n")
for value in meta[wnid]:
    sys.stderr.write("{}:{}\n".format(value, meta[wnid][value]))

sys.stderr.write("\nDo you want to proceed? [yes|no]\n\n")
confirmation = input()
if confirmation.strip() not in  ["yes", "y", "Y", "Yes"]:
    sys.stderr.write("Quitting...\n")
    sys.exit()
################################################################################



def vary(lemma):
    """returns a list of variants and their tag data
       this version gives basic transliteration with unidecode"""    
    vars = []  # [(var, cat, tag), ]  e.g. ('colour', 'dialect', 'GB')
    var = unidecode(lemma)
    var = var.strip()
    if var and var != lemma:
        vars.append((var.lower(), 'transliteration', 'ascii'))
    return vars
    
def print_header(meta, lang, comment):
    """print the header of the lexicon, filled in with WN-LMF meta data"""

    header = str()

    if comment:
        header += ("""<!-- {}  -->\n""".format(comment))

    header += ("""  <Lexicon id="{}" \n""".format(meta['id']+'-'+lang))
    header += ("""           label="{}" \n""".format(meta['label']))
    header += ("""           language="{}" \n""".format(lang))
    header += ("""           email="{}" \n""".format(meta['email']))
    header += ("""           license="{}" \n""".format(meta['license']))
    header += ("""           version="{}" \n""".format(meta['version']))
    header += ("""           citation="{}" \n""".format(meta['citation']))
    header += ("""           url="{}" \n""".format(meta['url']))
    header += ("""           dc:publisher="Global Wordnet Association" \n""")
    header += ("""           dc:format="OMW-LMF" \n""")
    header += ("""           dc:description="{}" \n""".format(meta['description']))
    header += ("""           confidenceScore="{}">""".format(meta['conf']))

    return header


def print_footer():

    footer = str()
    footer += ("  </Lexicon>")
    return footer


def read_wn(fn):
    """Given a .tab+ file (also ready for forms), it prepares lexical 
       entries and senses"""

    lexicon = dd(lambda: dd(lambda: dd(lambda: dd(lambda:set()))))
    ss_defs = dd(lambda: dd(lambda: dd())) # ssdefs['synsetID']['eng'][0] = "first English def" 
    ss_exes = dd(lambda: dd(lambda: dd())) # ssexes['synsetID']['eng'][0] = "first English example" 

    defined_synsets = dd() # this is a set to store all seen synsets as they should only be defined once
    
    map_file = open(ilimapfile,'r')
    ilimap = dd(str)
    for l in map_file:
        row = l.strip().split()
        ilimap[row[1].replace('-s','-a')] = row[0]


    tab_file = open(fn, 'r')
    lex_c = 0
    for line in tab_file:

        tab = line.split('\t')

        if tab[1].endswith(':lemma'):
            lex_c += 1

            lang = tab[1].split(':')[0]
            
            ss = tab[0].strip()
            lemma = tab[2].strip()
            pos = ss[-1].replace('s', 'a')

            var_end = len(tab) - 1
            variants = set()
            if var_end > 2:
                for i in range(3, var_end+1):
                    variants.add(tab[i].strip())

            ####################################################################
            # TRYING TO FIX:                                                   #
            # Synset should only be defined once (in a single lexicon)         #
            # and senses for other languages should link to the same synset    #
            # The best decision is to take the first time it is defined and    #
            # store a list to check whether it has been defined in other       #
            # language.                                                        #
            # the "Synset id naming convention" makes it that it must be       #
            # defined  with the ID starting as the wnid. In a file with        #
            # multiple languages this will also include the language           #
            # (e.g. "ntumc-cmn" or "ntumc-in")                                 #
            ####################################################################
                                                                               #
            if ss in defined_synsets.keys():                                   #
                ssID = wnid + '-' + defined_synsets[ss] + '-' + ss             #
                new_ss = False                                                 #
            else:                                                              #
                defined_synsets[ss] = lang                                     #
                ssID = wnid + '-' + lang + '-' + ss                            #
                new_ss = True                                                  #
                                                                               #
            ####################################################################

            
            if lexicon[lang]['Lex'][(lemma,tuple(variants),pos)]['lexID']:
                lexID = list(lexicon[lang]['Lex'][(lemma,tuple(variants),pos)]['lexID'])[0]
            
            else:
                lexID = wnid+'-'+lang+'-'+'lex'+str(lex_c)


            senseID = ss+'-'+lexID


            if new_ss:
                lexicon[lang]['Synset'][ssID]['pos'].add(pos)
                lexicon[lang]['Synset'][ssID]['ili'].add(ilimap[ss])

            
            lexicon[lang]['Lex'][(lemma,tuple(variants),pos)]['lexID'].add(lexID)
            lexicon[lang]['LexEntry'][lexID]['lemma'].add(lemma)
            lexicon[lang]['LexEntry'][lexID]['pos'].add(pos)
            for var in variants:
                lexicon[lang]['LexEntry'][lexID]['variants'].add(var)
            lexicon[lang]['LexEntry'][lexID]['sense'].add(ssID)




            
        ########################################################################
        # DEFINITIONS                                                          #
        ########################################################################
        # Definitions in this TSV file are synset objects. There is no plan to #
        # support sense definitions in this TSV format.                        #
        #                                                                      #
        # But multiple definitions can still exist for multiple languages.     #
        # Synsets in the XML format are only instanciated once even if there   #
        # are multiple lexicons in the same WN-LMF.                            #
        #                                                                      #
        # Because it doesn't really matter in which lexicon they are first     #
        # instanciated, they are being instanciated in the first language they #
        # are seen. This matters for the definitions, since they should be     #
        # grouped by synset first, and then language. All synset definitions   #
        # need to be dumped when the synset is defined. And each langauge      #
        # should be individually added to that definition. (when language is   #
        # no added, the WN-LMF assumes the definition is given in the same     #
        # language as the lexicon object.                                      #
        #                                                                      #
        # In the original tsv file, a definition is defined by 4 TSV values:   #
        #                                                                      #
        # synsetID  \t  lang:def  \t  OrderInteger  \t definition              #
        #                                                                      #
        # We will store the definitions like so:                               #
        # ssdefs['synsetID']['eng'][0] = "first eng def"                       #
        # ssdefs['synsetID']['eng'][1] = "second eng def"                      #
        # ssdefs['synsetID']['cmn'][0] = "first cmn def"                       #
        ########################################################################
        elif (tab[1].endswith(':def')) and (len(tab) == 4) :
            ss = tab[0].strip()
            lang = tab[1].split(':')[0].strip()
            order_int = int(tab[2].strip())
            definition = tab[3].strip()
            
            ss_defs[ss][lang][order_int] = definition


        ########################################################################
        # EXAMPLES                                                             #
        ########################################################################
        # Examples are essentially the same as definitions.                    #
        # We do not currently support sense examples in this TSV format.       # 
        ########################################################################
        elif (tab[1].endswith(':exe')) and (len(tab) == 4) :
            ss = tab[0].strip()
            lang = tab[1].split(':')[0].strip()
            order_int = int(tab[2].strip())
            example = tab[3].strip()
            
            ss_exes[ss][lang][order_int] = example
            
    return lexicon, ss_defs, ss_exes


################################################################################
# PRINT OUT XML
################################################################################

wn, ss_defs, ss_exes = read_wn(wnfile_path)

print("""<?xml version="1.0" encoding="UTF-8"?>""")
print("""<!DOCTYPE LexicalResource SYSTEM "http://globalwordnet.github.io/schemas/WN-LMF-1.0.dtd">""")
print("""<LexicalResource xmlns:dc="http://purl.org/dc/elements/1.1/">""")
for lang in wn:

    # header = print_header(meta[wnid+'-'+lang], None)
    header = print_header(meta[wnid], lang, None)
    print(header)

    for lexID in wn[lang]['LexEntry']:

        lexEntry = str()
        lexEntry += """    <LexicalEntry id="{}">\n""".format(lexID)

        lemma = list(wn[lang]['LexEntry'][lexID]['lemma'])[0]
        pos = list(wn[lang]['LexEntry'][lexID]['pos'])[0]
        lexEntry += """      <Lemma writtenForm="{}" partOfSpeech="{}"/>\n""".format(lemma,pos)
        variants = wn[lang]['LexEntry'][lexID]['variants']

        


        ########################################################################
        # FORMS AND VARIANTS                                                   #
        ########################################################################
        newvariants = set(variants)

        ########################################################################
        # This generates autmatic ASCII forms based on the unicode databse.    #
        # ASCII forms generated here are based on the cannonical lemma.        #     
        ########################################################################
        # for (var,cat,tag) in vary(lemma):
        #     if var not in newvariants:
        #         newvariants.add(var)
        #         lexEntry += """      <Form  writtenForm="{}">\n""".format(var)
        #         lexEntry += """          <Tag category="{}">{}</Tag>\n""".format(cat, tag)
        #         lexEntry += """      </Form>\n"""           

        ########################################################################
        # Here we include the forms provided on the TSV file.                  #
        # Currently there is no way of providing a tag for these forms.        #
        # These forms might also be non-ascii and, as such, these might add    #
        # further forms to the WN-LMF to aid in the search functions           #
        ########################################################################
        for v in variants:
            lexEntry += """      <Form  writtenForm="{}"></Form>\n""".format(v)
            for (var,cat,tag) in vary(v):
                if var not in newvariants:
                    newvariants.add(var)
                    lexEntry += """      <Form  writtenForm="{}">\n""".format(var)
                    lexEntry += """          <Tag category="{}">{}</Tag>\n""".format(cat, tag)
                    lexEntry += """      </Form>\n"""


                

        senses = wn[lang]['LexEntry'][lexID]['sense']

        for ssID in senses:
            senseID = ssID+'-'+lexID
            lexEntry += """      <Sense id="{}" synset="{}"></Sense>\n""".format(senseID, ssID)

        lexEntry += """    </LexicalEntry>"""

        print(lexEntry)


    for ssID in wn[lang]['Synset']:
        
        original_ss = ssID[len(wnid)+len(lang)+2:]
        pos = list(wn[lang]['Synset'][ssID]['pos'])[0]
        ili = list(wn[lang]['Synset'][ssID]['ili'])[0]
        synEntry = """    <Synset id="{}" ili="{}" partOfSpeech="{}">""".format(ssID, ili, pos)

        if (original_ss in ss_defs.keys()) or (original_ss in ss_exes.keys()):
            synEntry += "\n"


            if original_ss in ss_defs.keys():
                for def_lang in ss_defs[original_ss]:
                    # There is one definition per language;
                    # Multiple definitions are separated by ';'

                    definition = ""
                    for i in sorted(list(ss_defs[original_ss][def_lang].keys())):
                        definition += ss_defs[original_ss][def_lang][i]
                        definition += '; '

                    synEntry += """        <Definition language="{}">{}</Definition>\n""".format(def_lang,
                                                                                                 definition.strip('; '))



            if original_ss in ss_exes.keys():
                for exe_lang in ss_exes[original_ss]:
                    # There can be multiple examples per language;

                    for i in sorted(list(ss_exes[original_ss][exe_lang].keys())):
                        example = ss_exes[original_ss][exe_lang][i]
                        synEntry += """        <Example language="{}">{}</Example>\n""".format(exe_lang,
                                                                                           example.strip())
                    
            synEntry += """    </Synset>""".format(ssID, ili, pos) # well aligned
            
        else:
            synEntry += """</Synset>""".format(ssID, ili, pos)  # well aligned
        
        print(synEntry)

    footer = print_footer()
    print(footer)
print("""</LexicalResource>""")
