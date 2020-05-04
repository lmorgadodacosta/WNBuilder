#!/usr/bin/env python3

################################################################################
# Luis Morgado da Costa (lmorgado.dacosta@gmail.com)
# Last Modified: August 2019
# License: MIT License (below)
# Files: tab2lmf.py, meta.py
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
# This file is a companion to tab2lmf.py and it contains meta information for 
# any number of wordnets.
################################################################################

from collections import defaultdict as dd
meta = dd(lambda: dd(str))


meta['albanet'] = {'id':'albanet', 
                   'label':'Albanet (Albanian Wordnet)',
                   'lang':'als', # als = Tosk Albanian; sq = Albanian (Macrolanguage)
                   'email':'',
                   'license':'https://creativecommons.org/licenses/by/3.0/',
                   'version':'1.0',
                   'citation':"Ervin Ruci. 2008. On the current state of Albanet and related applications. Technical report, University of Vlora. (http://fjalnet.com/technicalreportalbanet.pdf)",
                   'url':'http://fjalnet.com',
                   # 'dc:publisher':"Global Wordnet Association", 
                   'dc:format':"OMW-LMF",
                   'description':"This is the original URL, but it seems to be down.",
                   'conf':"1.0"}

meta['awn'] = {'id':'awn',
               'label':'Arabic Wordnet',
               'lang':'ar', # the paper mentions Standard Arabic (the code could be "ar" or "arb"?)
               'email':'',
               'license':'https://creativecommons.org/licenses/by/3.0/',
               'version':'2.0',
               'citation':"Black W., Elkateb S., Rodriguez H., Alkhalifa M., Vossen P., Pease A., Bertran M., Fellbaum C., (2006) The Arabic WordNet Project, Proceedings of LREC 2006; Lahsen Abouenour, Karim Bouzoubaa, Paolo Rosso (2013) On the evaluation and improvement of Arabic WordNet coverage and usability, Language Resources and Evaluation 47(3) pp 891–917",
               'url':'http://www.globalwordnet.org/AWN/',
               # 'dc:publisher':"Global Wordnet Association",
               'dc:format':"OMW-LMF",
               'description':'',
               'conf':"1.0"}

meta['dannet'] = {'id':'dannet',
                  'label':'DanNet',
                  'lang':'da', # Danish, 3 letter code = dan 
                  'email':'bspedersen@hum.ku.dk',
                  'license':'wordnet',
                  'version':'1.0',
                  'citation':"Bolette S. Pedersen, Sanni Nimb, Jørg Asmussen, Nicolai H. Sørensen, Lars Trap-Jensen og Henrik Lorentzen. DanNet – the challenge of compiling a WordNet for Danish by reusing a monolingual dictionary. Lang Resources & Evaluation (2009) 43:269–299.",
                  'url':'https://cst.ku.dk/english/projekter/dannet/',
                  # 'dc:publisher':"Global Wordnet Association",
                  'dc:format':"OMW-LMF",
                  'description':'',
                  'conf':"1.0"}
