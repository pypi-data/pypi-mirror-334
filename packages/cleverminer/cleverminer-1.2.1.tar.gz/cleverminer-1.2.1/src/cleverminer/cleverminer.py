import sys #line:1
import time #line:2
import copy #line:3
from time import strftime #line:5
from time import gmtime #line:6
import pandas as pd #line:8
import numpy as np #line:9
from pandas .api .types import CategoricalDtype #line:10
import progressbar #line:11
import re #line:12
from textwrap import wrap #line:13
import seaborn as sns #line:14
import matplotlib .pyplot as plt #line:15
import re #line:16
import pickle #line:17
import json #line:18
import hashlib #line:19
from datetime import datetime #line:20
import tempfile #line:21
import os #line:22
import urllib #line:23
class cleverminer :#line:25
    version_string ="1.2.1"#line:27
    temppath =tempfile .gettempdir ()#line:29
    cache_dir =os .path .join (temppath ,'clm_cache')#line:30
    def __init__ (O00O00OO0O00O00O0 ,**O000OO0000O00OOOO ):#line:32
        ""#line:61
        O00O00OO0O00O00O0 ._print_disclaimer ()#line:62
        O00O00OO0O00O00O0 .use_cache =False #line:63
        O00O00OO0O00O00O0 .cache_also_data =True #line:64
        O00O00OO0O00O00O0 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:73
        O00O00OO0O00O00O0 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:81
        O00O00OO0O00O00O0 .df =None #line:82
        O00O00OO0O00O00O0 .kwargs =None #line:83
        if len (O000OO0000O00OOOO )>0 :#line:84
            O00O00OO0O00O00O0 .kwargs =O000OO0000O00OOOO #line:85
        O00O00OO0O00O00O0 .profiles ={}#line:86
        O00O00OO0O00O00O0 .verbosity ={}#line:87
        O00O00OO0O00O00O0 .verbosity ['debug']=False #line:88
        O00O00OO0O00O00O0 .verbosity ['print_rules']=False #line:89
        O00O00OO0O00O00O0 .verbosity ['print_hashes']=True #line:90
        O00O00OO0O00O00O0 .verbosity ['last_hash_time']=0 #line:91
        O00O00OO0O00O00O0 .verbosity ['hint']=False #line:92
        if "opts"in O000OO0000O00OOOO :#line:93
            O00O00OO0O00O00O0 ._set_opts (O000OO0000O00OOOO .get ("opts"))#line:94
        if "opts"in O000OO0000O00OOOO :#line:95
            OO0OO0O00OOO00O0O =O000OO0000O00OOOO ['opts']#line:96
            if 'use_cache'in OO0OO0O00OOO00O0O :#line:97
                O00O00OO0O00O00O0 .use_cache =OO0OO0O00OOO00O0O ['use_cache']#line:98
            if 'cache_also_data'in OO0OO0O00OOO00O0O :#line:99
                O00O00OO0O00O00O0 .cache_also_data =OO0OO0O00OOO00O0O ['cache_also_data']#line:100
            if "verbose"in O000OO0000O00OOOO .get ('opts'):#line:101
                OOO0O0O0O000OOOO0 =O000OO0000O00OOOO .get ('opts').get ('verbose')#line:102
                if OOO0O0O0O000OOOO0 .upper ()=='FULL':#line:103
                    O00O00OO0O00O00O0 .verbosity ['debug']=True #line:104
                    O00O00OO0O00O00O0 .verbosity ['print_rules']=True #line:105
                    O00O00OO0O00O00O0 .verbosity ['print_hashes']=False #line:106
                    O00O00OO0O00O00O0 .verbosity ['hint']=True #line:107
                    O00O00OO0O00O00O0 .options ['progressbar']=False #line:108
                elif OOO0O0O0O000OOOO0 .upper ()=='RULES':#line:109
                    O00O00OO0O00O00O0 .verbosity ['debug']=False #line:110
                    O00O00OO0O00O00O0 .verbosity ['print_rules']=True #line:111
                    O00O00OO0O00O00O0 .verbosity ['print_hashes']=True #line:112
                    O00O00OO0O00O00O0 .verbosity ['hint']=True #line:113
                    O00O00OO0O00O00O0 .options ['progressbar']=False #line:114
                elif OOO0O0O0O000OOOO0 .upper ()=='HINT':#line:115
                    O00O00OO0O00O00O0 .verbosity ['debug']=False #line:116
                    O00O00OO0O00O00O0 .verbosity ['print_rules']=False #line:117
                    O00O00OO0O00O00O0 .verbosity ['print_hashes']=True #line:118
                    O00O00OO0O00O00O0 .verbosity ['last_hash_time']=0 #line:119
                    O00O00OO0O00O00O0 .verbosity ['hint']=True #line:120
                    O00O00OO0O00O00O0 .options ['progressbar']=False #line:121
                elif OOO0O0O0O000OOOO0 .upper ()=='DEBUG':#line:122
                    O00O00OO0O00O00O0 .verbosity ['debug']=True #line:123
                    O00O00OO0O00O00O0 .verbosity ['print_rules']=True #line:124
                    O00O00OO0O00O00O0 .verbosity ['print_hashes']=True #line:125
                    O00O00OO0O00O00O0 .verbosity ['last_hash_time']=0 #line:126
                    O00O00OO0O00O00O0 .verbosity ['hint']=True #line:127
                    O00O00OO0O00O00O0 .options ['progressbar']=False #line:128
        if "load"in O000OO0000O00OOOO :#line:131
            if O00O00OO0O00O00O0 .use_cache :#line:133
                O00O00OO0O00O00O0 .use_cache =False #line:134
        O0OOO00O000O00O0O =copy .deepcopy (O000OO0000O00OOOO )#line:135
        if 'df'in O0OOO00O000O00O0O :#line:136
            O0OOO00O000O00O0O ['df']=O0OOO00O000O00O0O ['df'].to_json ()#line:137
        O0O0OOO000OO0O00O =O00O00OO0O00O00O0 ._get_hash (O0OOO00O000O00O0O )#line:138
        O00O00OO0O00O00O0 .guid =O0O0OOO000OO0O00O #line:139
        if O00O00OO0O00O00O0 .use_cache :#line:140
            if not (os .path .isdir (O00O00OO0O00O00O0 .cache_dir )):#line:141
                os .mkdir (O00O00OO0O00O00O0 .cache_dir )#line:142
            O00O00OO0O00O00O0 .cache_fname =os .path .join (O00O00OO0O00O00O0 .cache_dir ,O0O0OOO000OO0O00O +'.clm')#line:143
            if os .path .isfile (O00O00OO0O00O00O0 .cache_fname ):#line:144
                print (f"Will use cached file {O00O00OO0O00O00O0.cache_fname}")#line:145
                OOOO000OO00O0O0O0 ='pickle'#line:146
                if "fmt"in O000OO0000O00OOOO :#line:147
                    OOOO000OO00O0O0O0 =O000OO0000O00OOOO .get ('fmt')#line:148
                O00O00OO0O00O00O0 .load (O00O00OO0O00O00O0 .cache_fname ,fmt =OOOO000OO00O0O0O0 )#line:149
                return #line:150
            print (f"Task {O0O0OOO000OO0O00O} not in cache, will calculate it.")#line:151
        O00O00OO0O00O00O0 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:153
        if not (O00O00OO0O00O00O0 ._is_py310 ):#line:154
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:155
        else :#line:156
            if (O00O00OO0O00O00O0 .verbosity ['debug']):#line:157
                print ("Python 3.10+ detected.")#line:158
        O00O00OO0O00O00O0 ._initialized =False #line:159
        if "load"in O000OO0000O00OOOO :#line:160
            OOOO000OO00O0O0O0 ='pickle'#line:161
            if "fmt"in O000OO0000O00OOOO :#line:162
                OOOO000OO00O0O0O0 =O000OO0000O00OOOO .get ('fmt')#line:163
            O00O00OO0O00O00O0 .load (filename =O000OO0000O00OOOO .get ('load'),fmt =OOOO000OO00O0O0O0 )#line:164
            return #line:165
        O00O00OO0O00O00O0 ._init_data ()#line:166
        O00O00OO0O00O00O0 ._init_task ()#line:167
        if len (O000OO0000O00OOOO )>0 :#line:168
            if "df"in O000OO0000O00OOOO :#line:169
                O00O00OO0O00O00O0 ._prep_data (O000OO0000O00OOOO .get ("df"))#line:170
            else :#line:171
                print ("Missing dataframe. Cannot initialize.")#line:172
                O00O00OO0O00O00O0 ._initialized =False #line:173
                return #line:174
            OO0OO0OOOO0OOO0OO =O000OO0000O00OOOO .get ("proc",None )#line:175
            if not (OO0OO0OOOO0OOO0OO ==None ):#line:176
                O00O00OO0O00O00O0 ._calculate (**O000OO0000O00OOOO )#line:177
            else :#line:178
                if O00O00OO0O00O00O0 .verbosity ['debug']:#line:179
                    print ("INFO: just initialized")#line:180
                O0O000O0OOO00OO00 ={}#line:181
                O0O00OOOO00O00OOO ={}#line:182
                O0O00OOOO00O00OOO ["varname"]=O00O00OO0O00O00O0 .data ["varname"]#line:183
                O0O00OOOO00O00OOO ["catnames"]=O00O00OO0O00O00O0 .data ["catnames"]#line:184
                O0O000O0OOO00OO00 ["datalabels"]=O0O00OOOO00O00OOO #line:185
                O00O00OO0O00O00O0 .result =O0O000O0OOO00OO00 #line:186
        O00O00OO0O00O00O0 ._initialized =True #line:188
        if O00O00OO0O00O00O0 .use_cache :#line:189
            O00O00OO0O00O00O0 .save (O00O00OO0O00O00O0 .cache_fname ,savedata =O00O00OO0O00O00O0 .cache_also_data ,embeddata =False )#line:190
            print (f"CACHE: results cache saved into {O00O00OO0O00O00O0.cache_fname}")#line:191
    def _get_hash (OO000OOO0000OOOOO ,OO0O00000OO000O0O ):#line:194
        class O0OO0OOO00OO0OO00 (json .JSONEncoder ):#line:196
            def default (OO00O0000000O0OOO ,O00O0OOOO0O0O0O00 ):#line:197
                if isinstance (O00O0OOOO0O0O0O00 ,np .integer ):#line:198
                    return int (O00O0OOOO0O0O0O00 )#line:199
                if isinstance (O00O0OOOO0O0O0O00 ,np .floating ):#line:200
                    return float (O00O0OOOO0O0O0O00 )#line:201
                if isinstance (O00O0OOOO0O0O0O00 ,np .ndarray ):#line:202
                    return O00O0OOOO0O0O0O00 .tolist ()#line:203
                return super (O0OO0OOO00OO0OO00 ,OO00O0000000O0OOO ).default (O00O0OOOO0O0O0O00 )#line:204
        OOO0OOOO0O0OO0O00 =hashlib .sha256 (json .dumps (OO0O00000OO000O0O ,sort_keys =True ,cls =O0OO0OOO00OO0OO00 ).encode ('utf-8')).hexdigest ()#line:206
        return OOO0OOOO0O0OO0O00 #line:208
    def _get_fast_hash (O0O0OO0000O0OOOOO ,OO000O0O0O0O0O0OO ):#line:211
        OOO000O0000OOO0OO =pickle .dumps (OO000O0O0O0O0O0OO )#line:216
        print (f"...CALC THE HASH {datetime.now()}")#line:217
        OO0O0OOOOOO0O00O0 =hashlib .md5 (OOO000O0000OOO0OO ).hexdigest ()#line:218
        return OO0O0OOOOOO0O00O0 #line:223
    def _set_opts (O00OOO00OO00O00OO ,O00OOOOOOO00O0OOO ):#line:225
        if "no_optimizations"in O00OOOOOOO00O0OOO :#line:226
            O00OOO00OO00O00OO .options ['optimizations']=not (O00OOOOOOO00O0OOO ['no_optimizations'])#line:227
            print ("No optimization will be made.")#line:228
        if "disable_progressbar"in O00OOOOOOO00O0OOO :#line:229
            O00OOO00OO00O00OO .options ['progressbar']=False #line:230
            print ("Progressbar will not be shown.")#line:231
        if "max_rules"in O00OOOOOOO00O0OOO :#line:232
            O00OOO00OO00O00OO .options ['max_rules']=O00OOOOOOO00O0OOO ['max_rules']#line:233
        if "max_categories"in O00OOOOOOO00O0OOO :#line:234
            O00OOO00OO00O00OO .options ['max_categories']=O00OOOOOOO00O0OOO ['max_categories']#line:235
            if O00OOO00OO00O00OO .verbosity ['debug']==True :#line:236
                print (f"Maximum number of categories set to {O00OOO00OO00O00OO.options['max_categories']}")#line:237
        if "no_automatic_data_conversions"in O00OOOOOOO00O0OOO :#line:238
            O00OOO00OO00O00OO .options ['automatic_data_conversions']=not (O00OOOOOOO00O0OOO ['no_automatic_data_conversions'])#line:239
            print ("No automatic data conversions will be made.")#line:240
        if "keep_df"in O00OOOOOOO00O0OOO :#line:241
            O00OOO00OO00O00OO .options ['keep_df']=O00OOOOOOO00O0OOO ['keep_df']#line:242
    def _init_data (O00O0O00OO0OOOO0O ):#line:245
        O00O0O00OO0OOOO0O .data ={}#line:247
        O00O0O00OO0OOOO0O .data ["varname"]=[]#line:248
        O00O0O00OO0OOOO0O .data ["catnames"]=[]#line:249
        O00O0O00OO0OOOO0O .data ["vtypes"]=[]#line:250
        O00O0O00OO0OOOO0O .data ["dm"]=[]#line:251
        O00O0O00OO0OOOO0O .data ["rows_count"]=int (0 )#line:252
        O00O0O00OO0OOOO0O .data ["data_prepared"]=0 #line:253
    def _init_task (O0O0O0OOO00OO00OO ):#line:255
        if "opts"in O0O0O0OOO00OO00OO .kwargs :#line:257
            O0O0O0OOO00OO00OO ._set_opts (O0O0O0OOO00OO00OO .kwargs .get ("opts"))#line:258
        O0O0O0OOO00OO00OO .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:268
        O0O0O0OOO00OO00OO .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:272
        O0O0O0OOO00OO00OO .rulelist =[]#line:273
        O0O0O0OOO00OO00OO .stats ['total_cnt']=0 #line:274
        O0O0O0OOO00OO00OO .stats ['total_valid']=0 #line:275
        O0O0O0OOO00OO00OO .stats ['control_number']=0 #line:276
        O0O0O0OOO00OO00OO .result ={}#line:277
        O0O0O0OOO00OO00OO ._opt_base =None #line:278
        O0O0O0OOO00OO00OO ._opt_relbase =None #line:279
        O0O0O0OOO00OO00OO ._opt_base1 =None #line:280
        O0O0O0OOO00OO00OO ._opt_relbase1 =None #line:281
        O0O0O0OOO00OO00OO ._opt_base2 =None #line:282
        O0O0O0OOO00OO00OO ._opt_relbase2 =None #line:283
        OOOO000OOO00OOOO0 =None #line:284
        if not (O0O0O0OOO00OO00OO .kwargs ==None ):#line:285
            OOOO000OOO00OOOO0 =O0O0O0OOO00OO00OO .kwargs .get ("quantifiers",None )#line:286
            if not (OOOO000OOO00OOOO0 ==None ):#line:287
                for OO00O00O00OO000OO in OOOO000OOO00OOOO0 .keys ():#line:288
                    if OO00O00O00OO000OO .upper ()=='BASE':#line:289
                        O0O0O0OOO00OO00OO ._opt_base =OOOO000OOO00OOOO0 .get (OO00O00O00OO000OO )#line:290
                    if OO00O00O00OO000OO .upper ()=='RELBASE':#line:291
                        O0O0O0OOO00OO00OO ._opt_relbase =OOOO000OOO00OOOO0 .get (OO00O00O00OO000OO )#line:292
                    if (OO00O00O00OO000OO .upper ()=='FRSTBASE')|(OO00O00O00OO000OO .upper ()=='BASE1'):#line:293
                        O0O0O0OOO00OO00OO ._opt_base1 =OOOO000OOO00OOOO0 .get (OO00O00O00OO000OO )#line:294
                    if (OO00O00O00OO000OO .upper ()=='SCNDBASE')|(OO00O00O00OO000OO .upper ()=='BASE2'):#line:295
                        O0O0O0OOO00OO00OO ._opt_base2 =OOOO000OOO00OOOO0 .get (OO00O00O00OO000OO )#line:296
                    if (OO00O00O00OO000OO .upper ()=='FRSTRELBASE')|(OO00O00O00OO000OO .upper ()=='RELBASE1'):#line:297
                        O0O0O0OOO00OO00OO ._opt_relbase1 =OOOO000OOO00OOOO0 .get (OO00O00O00OO000OO )#line:298
                    if (OO00O00O00OO000OO .upper ()=='SCNDRELBASE')|(OO00O00O00OO000OO .upper ()=='RELBASE2'):#line:299
                        O0O0O0OOO00OO00OO ._opt_relbase2 =OOOO000OOO00OOOO0 .get (OO00O00O00OO000OO )#line:300
            else :#line:301
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:302
        else :#line:303
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:304
    def mine (OO0O0OOO0000O0OO0 ,**OO0O0OOO0OO0O0OO0 ):#line:307
        ""#line:312
        if not (OO0O0OOO0000O0OO0 ._initialized ):#line:313
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:314
            return #line:315
        OO0O0OOO0000O0OO0 .kwargs =None #line:316
        if len (OO0O0OOO0OO0O0OO0 )>0 :#line:317
            OO0O0OOO0000O0OO0 .kwargs =OO0O0OOO0OO0O0OO0 #line:318
        OO0O0OOO0000O0OO0 ._init_task ()#line:319
        if len (OO0O0OOO0OO0O0OO0 )>0 :#line:320
            O0000OOOO0OO00O0O =OO0O0OOO0OO0O0OO0 .get ("proc",None )#line:321
            if not (O0000OOOO0OO00O0O ==None ):#line:322
                OO0O0OOO0000O0OO0 ._calc_all (**OO0O0OOO0OO0O0OO0 )#line:323
            else :#line:324
                print ("Rule mining procedure missing")#line:325
    def _get_ver (OOO00O00O0O0OO0O0 ):#line:328
        return OOO00O00O0O0OO0O0 .version_string #line:329
    def _print_disclaimer (O000OO0000OOOO00O ):#line:331
        print (f"Cleverminer version {O000OO0000OOOO00O._get_ver()}.")#line:332
    def _automatic_data_conversions (OO0OO00OOO0O0O0O0 ,O00O00O0O00O00OO0 ):#line:333
        print ("Automatically reordering numeric categories ...")#line:334
        for O0O0O00O00O00O000 in range (len (O00O00O0O00O00OO0 .columns )):#line:335
            if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:336
                print (f"#{O0O0O00O00O00O000}: {O00O00O0O00O00OO0.columns[O0O0O00O00O00O000]} : {O00O00O0O00O00OO0.dtypes[O0O0O00O00O00O000]}.")#line:337
            try :#line:338
                O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]]=O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]].astype (str ).astype (float )#line:339
                if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:340
                    print (f"CONVERTED TO FLOATS #{O0O0O00O00O00O000}: {O00O00O0O00O00OO0.columns[O0O0O00O00O00O000]} : {O00O00O0O00O00OO0.dtypes[O0O0O00O00O00O000]}.")#line:341
                O0O0OOO00000OOO0O =pd .unique (O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]])#line:342
                O000OO0OO00OOO000 =True #line:343
                for OO000O00OOOOOO000 in O0O0OOO00000OOO0O :#line:344
                    if OO000O00OOOOOO000 %1 !=0 :#line:345
                        O000OO0OO00OOO000 =False #line:346
                if O000OO0OO00OOO000 :#line:347
                    O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]]=O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]].astype (int )#line:348
                    if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:349
                        print (f"CONVERTED TO INT #{O0O0O00O00O00O000}: {O00O00O0O00O00OO0.columns[O0O0O00O00O00O000]} : {O00O00O0O00O00OO0.dtypes[O0O0O00O00O00O000]}.")#line:350
                OO0OO000OOO00O0O0 =pd .unique (O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]])#line:351
                OO0OO0OO0O0000O0O =CategoricalDtype (categories =OO0OO000OOO00O0O0 .sort (),ordered =True )#line:352
                O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]]=O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]].astype (OO0OO0OO0O0000O0O )#line:353
                if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:354
                    print (f"CONVERTED TO CATEGORY #{O0O0O00O00O00O000}: {O00O00O0O00O00OO0.columns[O0O0O00O00O00O000]} : {O00O00O0O00O00OO0.dtypes[O0O0O00O00O00O000]}.")#line:355
            except :#line:357
                if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:358
                    print ("...cannot be converted to int")#line:359
                try :#line:360
                    OOOO00OOO000000OO =O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]].unique ()#line:361
                    if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:362
                        print (f"Values: {OOOO00OOO000000OO}")#line:363
                    OO0O0O00OO0O00O00 =True #line:364
                    O0O0O0OO000000000 =[]#line:365
                    for OO000O00OOOOOO000 in OOOO00OOO000000OO :#line:366
                        O0O0O0OO0O0O0OOOO =re .findall (r"-?\d+",OO000O00OOOOOO000 )#line:369
                        if len (O0O0O0OO0O0O0OOOO )>0 :#line:371
                            O0O0O0OO000000000 .append (int (O0O0O0OO0O0O0OOOO [0 ]))#line:372
                        else :#line:373
                            OO0O0O00OO0O00O00 =False #line:374
                    if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:375
                        print (f"Is ok: {OO0O0O00OO0O00O00}, extracted {O0O0O0OO000000000}")#line:376
                    if OO0O0O00OO0O00O00 :#line:377
                        OOO000O0OOOO0OOOO =copy .deepcopy (O0O0O0OO000000000 )#line:378
                        OOO000O0OOOO0OOOO .sort ()#line:379
                        OO00OOO0OO00OOO00 =[]#line:381
                        for OO0OO00O00O0O000O in OOO000O0OOOO0OOOO :#line:382
                            OOO00O0OO0O000OO0 =O0O0O0OO000000000 .index (OO0OO00O00O0O000O )#line:383
                            OO00OOO0OO00OOO00 .append (OOOO00OOO000000OO [OOO00O0OO0O000OO0 ])#line:385
                        if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:386
                            print (f"Sorted list: {OO00OOO0OO00OOO00}")#line:387
                        OO0OO0OO0O0000O0O =CategoricalDtype (categories =OO00OOO0OO00OOO00 ,ordered =True )#line:388
                        O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]]=O00O00O0O00O00OO0 [O00O00O0O00O00OO0 .columns [O0O0O00O00O00O000 ]].astype (OO0OO0OO0O0000O0O )#line:389
                except :#line:390
                    if OO0OO00OOO0O0O0O0 .verbosity ['debug']:#line:391
                        print ("...cannot extract numbers from all categories")#line:392
        print ("Automatically reordering numeric categories ...done")#line:394
    def _prep_data (O00O0000000OOO000 ,O0O0OOO0OOO00O000 ):#line:396
        print ("Starting data preparation ...")#line:397
        O00O0000000OOO000 ._init_data ()#line:398
        O00O0000000OOO000 .stats ['start_prep_time']=time .time ()#line:399
        if O00O0000000OOO000 .options ['automatic_data_conversions']:#line:400
            O00O0000000OOO000 ._automatic_data_conversions (O0O0OOO0OOO00O000 )#line:401
        O00O0000000OOO000 .data ["rows_count"]=O0O0OOO0OOO00O000 .shape [0 ]#line:402
        for OOO00O000OO0OOOO0 in O0O0OOO0OOO00O000 .select_dtypes (exclude =['category']).columns :#line:403
            O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ]=O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ].apply (str )#line:404
        try :#line:405
            OOO0O0O0OO00OO00O =pd .DataFrame .from_records ([(OOOO00O00OO00OO00 ,O0O0OOO0OOO00O000 [OOOO00O00OO00OO00 ].nunique ())for OOOO00O00OO00OO00 in O0O0OOO0OOO00O000 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:407
        except :#line:408
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:409
            O0O0O000OOOOOOO00 =""#line:410
            try :#line:411
                for OOO00O000OO0OOOO0 in O0O0OOO0OOO00O000 .columns :#line:412
                    O0O0O000OOOOOOO00 =OOO00O000OO0OOOO0 #line:413
                    print (f"...column {OOO00O000OO0OOOO0} has {int(O0O0OOO0OOO00O000[OOO00O000OO0OOOO0].nunique())} values")#line:414
            except :#line:415
                print (f"... detected : column {O0O0O000OOOOOOO00} has unsupported type: {type(O0O0OOO0OOO00O000[OOO00O000OO0OOOO0])}.")#line:416
                exit (1 )#line:417
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:418
            exit (1 )#line:419
        if O00O0000000OOO000 .verbosity ['hint']:#line:422
            print ("Quick profile of input data: unique value counts are:")#line:423
            print (OOO0O0O0OO00OO00O )#line:424
            for OOO00O000OO0OOOO0 in O0O0OOO0OOO00O000 .columns :#line:425
                if O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ].nunique ()<O00O0000000OOO000 .options ['max_categories']:#line:426
                    O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ]=O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ].astype ('category')#line:427
                else :#line:428
                    print (f"WARNING: attribute {OOO00O000OO0OOOO0} has more than {O00O0000000OOO000.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:429
                    del O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ]#line:430
        for OOO00O000OO0OOOO0 in O0O0OOO0OOO00O000 .columns :#line:432
            if O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ].nunique ()>O00O0000000OOO000 .options ['max_categories']:#line:433
                print (f"WARNING: attribute {OOO00O000OO0OOOO0} has more than {O00O0000000OOO000.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:434
                del O0O0OOO0OOO00O000 [OOO00O000OO0OOOO0 ]#line:435
        if O00O0000000OOO000 .options ['keep_df']:#line:436
            if O00O0000000OOO000 .verbosity ['debug']:#line:437
                print ("Keeping df.")#line:438
            O00O0000000OOO000 .df =O0O0OOO0OOO00O000 #line:439
        print ("Encoding columns into bit-form...")#line:440
        OO00O0OOOOO00OOOO =0 #line:441
        OOOOOO000O0O00O0O =0 #line:442
        for OO0000OOOO00OOO00 in O0O0OOO0OOO00O000 :#line:443
            if O00O0000000OOO000 .verbosity ['debug']:#line:444
                print ('Column: '+OO0000OOOO00OOO00 +' @ '+str (time .time ()))#line:445
            if O00O0000000OOO000 .verbosity ['debug']:#line:446
                print ('Column: '+OO0000OOOO00OOO00 )#line:447
            O00O0000000OOO000 .data ["varname"].append (OO0000OOOO00OOO00 )#line:448
            O0OO00000OOO0O0OO =pd .get_dummies (O0O0OOO0OOO00O000 [OO0000OOOO00OOO00 ])#line:449
            OOOO0OO00O0OOO0O0 =0 #line:450
            if (O0O0OOO0OOO00O000 .dtypes [OO0000OOOO00OOO00 ].name =='category'):#line:451
                OOOO0OO00O0OOO0O0 =1 #line:452
            O00O0000000OOO000 .data ["vtypes"].append (OOOO0OO00O0OOO0O0 )#line:453
            if O00O0000000OOO000 .verbosity ['debug']:#line:454
                print (O0OO00000OOO0O0OO )#line:455
                print (O0O0OOO0OOO00O000 [OO0000OOOO00OOO00 ])#line:456
            O00O0O0O000O00O0O =0 #line:457
            OOOOO0O0O000O00O0 =[]#line:458
            OO000O0000OO0OO0O =[]#line:459
            if O00O0000000OOO000 .verbosity ['debug']:#line:460
                print ('...starting categories '+str (time .time ()))#line:461
            for O00OO000000O0OOO0 in O0OO00000OOO0O0OO :#line:462
                if O00O0000000OOO000 .verbosity ['debug']:#line:463
                    print ('....category : '+str (O00OO000000O0OOO0 )+' @ '+str (time .time ()))#line:464
                OOOOO0O0O000O00O0 .append (O00OO000000O0OOO0 )#line:465
                OOOO0OO00OO000OOO =int (0 )#line:466
                O00OO0000O000OOOO =O0OO00000OOO0O0OO [O00OO000000O0OOO0 ].values #line:467
                if O00O0000000OOO000 .verbosity ['debug']:#line:468
                    print (O00OO0000O000OOOO .ndim )#line:469
                OO00OOO000OOO0OOO =np .packbits (O00OO0000O000OOOO ,bitorder ='little')#line:470
                OOOO0OO00OO000OOO =int .from_bytes (OO00OOO000OOO0OOO ,byteorder ='little')#line:471
                OO000O0000OO0OO0O .append (OOOO0OO00OO000OOO )#line:472
                if O00O0000000OOO000 .verbosity ['debug']:#line:474
                    for OO0O0000000O0O0O0 in range (O00O0000000OOO000 .data ["rows_count"]):#line:476
                        if O00OO0000O000OOOO [OO0O0000000O0O0O0 ]>0 :#line:477
                            OOOO0OO00OO000OOO +=1 <<OO0O0000000O0O0O0 #line:478
                            OO000O0000OO0OO0O .append (OOOO0OO00OO000OOO )#line:479
                    print ('....category ATTEMPT 2: '+str (O00OO000000O0OOO0 )+" @ "+str (time .time ()))#line:482
                    OOO0OOOO0OOOOO000 =int (0 )#line:483
                    O0OOO0OO0OO0000OO =int (1 )#line:484
                    for OO0O0000000O0O0O0 in range (O00O0000000OOO000 .data ["rows_count"]):#line:485
                        if O00OO0000O000OOOO [OO0O0000000O0O0O0 ]>0 :#line:486
                            OOO0OOOO0OOOOO000 +=O0OOO0OO0OO0000OO #line:487
                            O0OOO0OO0OO0000OO *=2 #line:488
                            O0OOO0OO0OO0000OO =O0OOO0OO0OO0000OO <<1 #line:489
                            print (str (OOOO0OO00OO000OOO ==OOO0OOOO0OOOOO000 )+" @ "+str (time .time ()))#line:490
                O00O0O0O000O00O0O +=1 #line:491
                OOOOOO000O0O00O0O +=1 #line:492
                if O00O0000000OOO000 .verbosity ['debug']:#line:493
                    print (OOOOO0O0O000O00O0 )#line:494
            O00O0000000OOO000 .data ["catnames"].append (OOOOO0O0O000O00O0 )#line:495
            O00O0000000OOO000 .data ["dm"].append (OO000O0000OO0OO0O )#line:496
        print ("Encoding columns into bit-form...done")#line:498
        if O00O0000000OOO000 .verbosity ['hint']:#line:499
            print (f"List of attributes for analysis is: {O00O0000000OOO000.data['varname']}")#line:500
            print (f"List of category names for individual attributes is : {O00O0000000OOO000.data['catnames']}")#line:501
        if O00O0000000OOO000 .verbosity ['debug']:#line:502
            print (f"List of vtypes is (all should be 1) : {O00O0000000OOO000.data['vtypes']}")#line:503
        O00O0000000OOO000 .data ["data_prepared"]=1 #line:504
        print ("Data preparation finished.")#line:505
        if O00O0000000OOO000 .verbosity ['debug']:#line:506
            print ('Number of variables : '+str (len (O00O0000000OOO000 .data ["dm"])))#line:507
            print ('Total number of categories in all variables : '+str (OOOOOO000O0O00O0O ))#line:508
        O00O0000000OOO000 .stats ['end_prep_time']=time .time ()#line:509
        if O00O0000000OOO000 .verbosity ['debug']:#line:510
            print ('Time needed for data preparation : ',str (O00O0000000OOO000 .stats ['end_prep_time']-O00O0000000OOO000 .stats ['start_prep_time']))#line:511
    def _bitcount (OOOO000O0O00000O0 ,O00OOO0OO00O000OO ):#line:513
        OOOOO000OOOOO000O =None #line:514
        if (OOOO000O0O00000O0 ._is_py310 ):#line:515
            OOOOO000OOOOO000O =O00OOO0OO00O000OO .bit_count ()#line:516
        else :#line:517
            OOOOO000OOOOO000O =bin (O00OOO0OO00O000OO ).count ("1")#line:518
        return OOOOO000OOOOO000O #line:519
    def _verifyCF (OO0000O0O00OOO0OO ,_O0OOO0OO00000O0O0 ):#line:522
        OO0O0OO0OO00OOO0O =OO0000O0O00OOO0OO ._bitcount (_O0OOO0OO00000O0O0 )#line:523
        O0OOOO0OOOO0O0OO0 =[]#line:524
        OO0O0OO0O00O000O0 =[]#line:525
        OO0O00OO0O00000O0 =0 #line:526
        O00O0O0O0OOO000O0 =0 #line:527
        OOO000OO00O00OOO0 =0 #line:528
        OO0O0O00O0O0OOO0O =0 #line:529
        O00O000O000OOO000 =0 #line:530
        O00000O0OO000O0OO =0 #line:531
        O0O0000O00OOO0OOO =0 #line:532
        OO0O0000O00000O00 =0 #line:533
        OOOO0O00O00OO0000 =0 #line:534
        O00O000000OO0O00O =None #line:535
        OO0OOOOOO00000OOO =None #line:536
        O000O00O00OO0O0OO =None #line:537
        if ('min_step_size'in OO0000O0O00OOO0OO .quantifiers ):#line:538
            O00O000000OO0O00O =OO0000O0O00OOO0OO .quantifiers .get ('min_step_size')#line:539
        if ('min_rel_step_size'in OO0000O0O00OOO0OO .quantifiers ):#line:540
            OO0OOOOOO00000OOO =OO0000O0O00OOO0OO .quantifiers .get ('min_rel_step_size')#line:541
            if OO0OOOOOO00000OOO >=1 and OO0OOOOOO00000OOO <100 :#line:542
                OO0OOOOOO00000OOO =OO0OOOOOO00000OOO /100 #line:543
        O0O0O00O0O0000O00 =0 #line:544
        OOO00000O00O000O0 =0 #line:545
        O00OO0O000000O000 =[]#line:546
        if ('aad_weights'in OO0000O0O00OOO0OO .quantifiers ):#line:547
            O0O0O00O0O0000O00 =1 #line:548
            O0OOOO0O0OOOO0O0O =[]#line:549
            O00OO0O000000O000 =OO0000O0O00OOO0OO .quantifiers .get ('aad_weights')#line:550
        OO00O0OO0O000O00O =OO0000O0O00OOO0OO .data ["dm"][OO0000O0O00OOO0OO .data ["varname"].index (OO0000O0O00OOO0OO .kwargs .get ('target'))]#line:551
        def O0O00OO00O0OO000O (O00OOO0O00000O0O0 ,O000O00O00O0O0O00 ):#line:552
            OO0O00OO0OO00OOOO =True #line:553
            if (O00OOO0O00000O0O0 >O000O00O00O0O0O00 ):#line:554
                if not (O00O000000OO0O00O is None or O00OOO0O00000O0O0 >=O000O00O00O0O0O00 +O00O000000OO0O00O ):#line:555
                    OO0O00OO0OO00OOOO =False #line:556
                if not (OO0OOOOOO00000OOO is None or O00OOO0O00000O0O0 >=O000O00O00O0O0O00 *(1 +OO0OOOOOO00000OOO )):#line:557
                    OO0O00OO0OO00OOOO =False #line:558
            if (O00OOO0O00000O0O0 <O000O00O00O0O0O00 ):#line:559
                if not (O00O000000OO0O00O is None or O00OOO0O00000O0O0 <=O000O00O00O0O0O00 -O00O000000OO0O00O ):#line:560
                    OO0O00OO0OO00OOOO =False #line:561
                if not (OO0OOOOOO00000OOO is None or O00OOO0O00000O0O0 <=O000O00O00O0O0O00 *(1 -OO0OOOOOO00000OOO )):#line:562
                    OO0O00OO0OO00OOOO =False #line:563
            return OO0O00OO0OO00OOOO #line:564
        for O000OO0000O00OO0O in range (len (OO00O0OO0O000O00O )):#line:565
            O00O0O0O0OOO000O0 =OO0O00OO0O00000O0 #line:567
            OO0O00OO0O00000O0 =OO0000O0O00OOO0OO ._bitcount (_O0OOO0OO00000O0O0 &OO00O0OO0O000O00O [O000OO0000O00OO0O ])#line:568
            O0OOOO0OOOO0O0OO0 .append (OO0O00OO0O00000O0 )#line:569
            if O000OO0000O00OO0O >0 :#line:570
                if (OO0O00OO0O00000O0 >O00O0O0O0OOO000O0 ):#line:571
                    if (OOO000OO00O00OOO0 ==1 )and (O0O00OO00O0OO000O (OO0O00OO0O00000O0 ,O00O0O0O0OOO000O0 )):#line:572
                        OO0O0000O00000O00 +=1 #line:573
                    else :#line:574
                        if O0O00OO00O0OO000O (OO0O00OO0O00000O0 ,O00O0O0O0OOO000O0 ):#line:575
                            OO0O0000O00000O00 =1 #line:576
                        else :#line:577
                            OO0O0000O00000O00 =0 #line:578
                    if OO0O0000O00000O00 >OO0O0O00O0O0OOO0O :#line:579
                        OO0O0O00O0O0OOO0O =OO0O0000O00000O00 #line:580
                    OOO000OO00O00OOO0 =1 #line:581
                    if O0O00OO00O0OO000O (OO0O00OO0O00000O0 ,O00O0O0O0OOO000O0 ):#line:582
                        O00000O0OO000O0OO +=1 #line:583
                if (OO0O00OO0O00000O0 <O00O0O0O0OOO000O0 ):#line:584
                    if (OOO000OO00O00OOO0 ==-1 )and (O0O00OO00O0OO000O (OO0O00OO0O00000O0 ,O00O0O0O0OOO000O0 )):#line:585
                        OOOO0O00O00OO0000 +=1 #line:586
                    else :#line:587
                        if O0O00OO00O0OO000O (OO0O00OO0O00000O0 ,O00O0O0O0OOO000O0 ):#line:588
                            OOOO0O00O00OO0000 =1 #line:589
                        else :#line:590
                            OOOO0O00O00OO0000 =0 #line:591
                    if OOOO0O00O00OO0000 >O00O000O000OOO000 :#line:592
                        O00O000O000OOO000 =OOOO0O00O00OO0000 #line:593
                    OOO000OO00O00OOO0 =-1 #line:594
                    if O0O00OO00O0OO000O (OO0O00OO0O00000O0 ,O00O0O0O0OOO000O0 ):#line:595
                        O0O0000O00OOO0OOO +=1 #line:596
                if (OO0O00OO0O00000O0 ==O00O0O0O0OOO000O0 ):#line:597
                    OOO000OO00O00OOO0 =0 #line:598
                    OOOO0O00O00OO0000 =0 #line:599
                    OO0O0000O00000O00 =0 #line:600
            if (O0O0O00O0O0000O00 ):#line:602
                OOOO0O0OOOO000O00 =OO0000O0O00OOO0OO ._bitcount (OO00O0OO0O000O00O [O000OO0000O00OO0O ])#line:603
                O0OOOO0O0OOOO0O0O .append (OOOO0O0OOOO000O00 )#line:604
        if (O0O0O00O0O0000O00 &sum (O0OOOO0OOOO0O0OO0 )>0 ):#line:606
            for O000OO0000O00OO0O in range (len (OO00O0OO0O000O00O )):#line:607
                if O0OOOO0O0OOOO0O0O [O000OO0000O00OO0O ]>0 :#line:608
                    if O0OOOO0OOOO0O0OO0 [O000OO0000O00OO0O ]/sum (O0OOOO0OOOO0O0OO0 )>O0OOOO0O0OOOO0O0O [O000OO0000O00OO0O ]/sum (O0OOOO0O0OOOO0O0O ):#line:609
                        OOO00000O00O000O0 +=O00OO0O000000O000 [O000OO0000O00OO0O ]*((O0OOOO0OOOO0O0OO0 [O000OO0000O00OO0O ]/sum (O0OOOO0OOOO0O0OO0 ))/(O0OOOO0O0OOOO0O0O [O000OO0000O00OO0O ]/sum (O0OOOO0O0OOOO0O0O ))-1 )#line:610
        OOO0OOOOO0O000000 =True #line:613
        for O0O00OOOOO0O0O00O in OO0000O0O00OOO0OO .quantifiers .keys ():#line:614
            if O0O00OOOOO0O0O00O .upper ()=='BASE':#line:615
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=OO0O0OO0OO00OOO0O )#line:616
            if O0O00OOOOO0O0O00O .upper ()=='RELBASE':#line:617
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=OO0O0OO0OO00OOO0O *1.0 /OO0000O0O00OOO0OO .data ["rows_count"])#line:618
            if O0O00OOOOO0O0O00O .upper ()=='S_UP':#line:619
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=OO0O0O00O0O0OOO0O )#line:620
            if O0O00OOOOO0O0O00O .upper ()=='S_DOWN':#line:621
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=O00O000O000OOO000 )#line:622
            if O0O00OOOOO0O0O00O .upper ()=='S_ANY_UP':#line:623
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=OO0O0O00O0O0OOO0O )#line:624
            if O0O00OOOOO0O0O00O .upper ()=='S_ANY_DOWN':#line:625
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=O00O000O000OOO000 )#line:626
            if O0O00OOOOO0O0O00O .upper ()=='MAX':#line:627
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=max (O0OOOO0OOOO0O0OO0 ))#line:628
            if O0O00OOOOO0O0O00O .upper ()=='MIN':#line:629
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=min (O0OOOO0OOOO0O0OO0 ))#line:630
            if O0O00OOOOO0O0O00O .upper ()=='RELMAX':#line:631
                if sum (O0OOOO0OOOO0O0OO0 )>0 :#line:632
                    OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=max (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 ))#line:633
                else :#line:634
                    OOO0OOOOO0O000000 =False #line:635
            if O0O00OOOOO0O0O00O .upper ()=='RELMAX_LEQ':#line:636
                if sum (O0OOOO0OOOO0O0OO0 )>0 :#line:637
                    OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )>=max (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 ))#line:638
                else :#line:639
                    OOO0OOOOO0O000000 =False #line:640
            if O0O00OOOOO0O0O00O .upper ()=='RELMIN':#line:641
                if sum (O0OOOO0OOOO0O0OO0 )>0 :#line:642
                    OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=min (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 ))#line:643
                else :#line:644
                    OOO0OOOOO0O000000 =False #line:645
            if O0O00OOOOO0O0O00O .upper ()=='RELMIN_LEQ':#line:646
                if sum (O0OOOO0OOOO0O0OO0 )>0 :#line:647
                    OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )>=min (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 ))#line:648
                else :#line:649
                    OOO0OOOOO0O000000 =False #line:650
            if O0O00OOOOO0O0O00O .upper ()=='AAD':#line:651
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )<=OOO00000O00O000O0 )#line:652
            if O0O00OOOOO0O0O00O .upper ()=='RELRANGE_LEQ':#line:653
                OOO0O00OOOO000OOO =OO0000O0O00OOO0OO .quantifiers .get (O0O00OOOOO0O0O00O )#line:654
                if OOO0O00OOOO000OOO >=1 and OOO0O00OOOO000OOO <100 :#line:655
                    OOO0O00OOOO000OOO =OOO0O00OOOO000OOO *1.0 /100 #line:656
                O000OO00OO0000OOO =min (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 )#line:657
                OO0OO000OO0O0O0OO =max (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 )#line:658
                OOO0OOOOO0O000000 =OOO0OOOOO0O000000 and (OOO0O00OOOO000OOO >=OO0OO000OO0O0O0OO -O000OO00OO0000OOO )#line:659
        O0O00O000O00O00O0 ={}#line:660
        if OOO0OOOOO0O000000 ==True :#line:661
            if OO0000O0O00OOO0OO .verbosity ['debug']:#line:662
                print ("Rule found: base: "+str (OO0O0OO0OO00OOO0O )+", hist: "+str (O0OOOO0OOOO0O0OO0 )+", max: "+str (max (O0OOOO0OOOO0O0OO0 ))+", min: "+str (min (O0OOOO0OOOO0O0OO0 ))+", s_up: "+str (OO0O0O00O0O0OOO0O )+", s_down: "+str (O00O000O000OOO000 ))#line:663
            OO0000O0O00OOO0OO .stats ['total_valid']+=1 #line:664
            O0O00O000O00O00O0 ["base"]=OO0O0OO0OO00OOO0O #line:665
            O0O00O000O00O00O0 ["rel_base"]=OO0O0OO0OO00OOO0O *1.0 /OO0000O0O00OOO0OO .data ["rows_count"]#line:666
            O0O00O000O00O00O0 ["s_up"]=OO0O0O00O0O0OOO0O #line:667
            O0O00O000O00O00O0 ["s_down"]=O00O000O000OOO000 #line:668
            O0O00O000O00O00O0 ["s_any_up"]=O00000O0OO000O0OO #line:669
            O0O00O000O00O00O0 ["s_any_down"]=O0O0000O00OOO0OOO #line:670
            O0O00O000O00O00O0 ["max"]=max (O0OOOO0OOOO0O0OO0 )#line:671
            O0O00O000O00O00O0 ["min"]=min (O0OOOO0OOOO0O0OO0 )#line:672
            if OO0000O0O00OOO0OO .verbosity ['debug']:#line:673
                O0O00O000O00O00O0 ["rel_max"]=max (O0OOOO0OOOO0O0OO0 )*1.0 /OO0000O0O00OOO0OO .data ["rows_count"]#line:674
                O0O00O000O00O00O0 ["rel_min"]=min (O0OOOO0OOOO0O0OO0 )*1.0 /OO0000O0O00OOO0OO .data ["rows_count"]#line:675
            if sum (O0OOOO0OOOO0O0OO0 )>0 :#line:676
                O0O00O000O00O00O0 ["rel_max"]=max (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 )#line:677
                O0O00O000O00O00O0 ["rel_min"]=min (O0OOOO0OOOO0O0OO0 )*1.0 /sum (O0OOOO0OOOO0O0OO0 )#line:678
            else :#line:679
                O0O00O000O00O00O0 ["rel_max"]=0 #line:680
                O0O00O000O00O00O0 ["rel_min"]=0 #line:681
            O0O00O000O00O00O0 ["hist"]=O0OOOO0OOOO0O0OO0 #line:682
            if O0O0O00O0O0000O00 :#line:683
                O0O00O000O00O00O0 ["aad"]=OOO00000O00O000O0 #line:684
                O0O00O000O00O00O0 ["hist_full"]=O0OOOO0O0OOOO0O0O #line:685
                O0O00O000O00O00O0 ["rel_hist"]=[OOOOO000O00O00OO0 /sum (O0OOOO0OOOO0O0OO0 )for OOOOO000O00O00OO0 in O0OOOO0OOOO0O0OO0 ]#line:686
                O0O00O000O00O00O0 ["rel_hist_full"]=[O0O0OOOO00O00000O /sum (O0OOOO0O0OOOO0O0O )for O0O0OOOO00O00000O in O0OOOO0O0OOOO0O0O ]#line:687
        if OO0000O0O00OOO0OO .verbosity ['debug']:#line:688
            print ("Info: base: "+str (OO0O0OO0OO00OOO0O )+", hist: "+str (O0OOOO0OOOO0O0OO0 )+", max: "+str (max (O0OOOO0OOOO0O0OO0 ))+", min: "+str (min (O0OOOO0OOOO0O0OO0 ))+", s_up: "+str (OO0O0O00O0O0OOO0O )+", s_down: "+str (O00O000O000OOO000 ))#line:689
        return OOO0OOOOO0O000000 ,O0O00O000O00O00O0 #line:690
    def _verifyUIC (O00OOOO0O000O000O ,_O00O00O0000O00OO0 ):#line:692
        O0OOOO0O00O0OOO00 ={}#line:693
        OO0OO00O0O0OOO0O0 =0 #line:694
        for OO0000O0OOOOOOOOO in O00OOOO0O000O000O .task_actinfo ['cedents']:#line:695
            O0OOOO0O00O0OOO00 [OO0000O0OOOOOOOOO ['cedent_type']]=OO0000O0OOOOOOOOO ['filter_value']#line:696
            OO0OO00O0O0OOO0O0 =OO0OO00O0O0OOO0O0 +1 #line:697
        if O00OOOO0O000O000O .verbosity ['debug']:#line:698
            print (OO0000O0OOOOOOOOO ['cedent_type']+" : "+str (OO0000O0OOOOOOOOO ['filter_value']))#line:699
        O0000OO00OO000OOO =O00OOOO0O000O000O ._bitcount (_O00O00O0000O00OO0 )#line:700
        OO0000OOOOO000000 =[]#line:701
        OOO00OOOO0O0OOOOO =0 #line:702
        O0O0O00000OO000O0 =0 #line:703
        O00OO00O00OOOO0OO =0 #line:704
        OO000OOOOO0OOO0OO =[]#line:705
        OO000OOO0O00O0OO0 =[]#line:706
        if ('aad_weights'in O00OOOO0O000O000O .quantifiers ):#line:707
            OO000OOOOO0OOO0OO =O00OOOO0O000O000O .quantifiers .get ('aad_weights')#line:708
            O0O0O00000OO000O0 =1 #line:709
        O0O0OOO00O00O0OO0 =O00OOOO0O000O000O .data ["dm"][O00OOOO0O000O000O .data ["varname"].index (O00OOOO0O000O000O .kwargs .get ('target'))]#line:710
        for OOO0000O0O00OOOO0 in range (len (O0O0OOO00O00O0OO0 )):#line:711
            O0OOOO000O00000OO =OOO00OOOO0O0OOOOO #line:713
            OOO00OOOO0O0OOOOO =O00OOOO0O000O000O ._bitcount (_O00O00O0000O00OO0 &O0O0OOO00O00O0OO0 [OOO0000O0O00OOOO0 ])#line:714
            OO0000OOOOO000000 .append (OOO00OOOO0O0OOOOO )#line:715
            OOOO0O0OO000OO00O =O00OOOO0O000O000O ._bitcount (O0OOOO0O00O0OOO00 ['cond']&O0O0OOO00O00O0OO0 [OOO0000O0O00OOOO0 ])#line:717
            OO000OOO0O00O0OO0 .append (OOOO0O0OO000OO00O )#line:718
        OO00OOO0OO00OO00O =0 #line:720
        O000OOOO000000OO0 =0 #line:721
        if (O0O0O00000OO000O0 &sum (OO0000OOOOO000000 )>0 ):#line:722
            for OOO0000O0O00OOOO0 in range (len (O0O0OOO00O00O0OO0 )):#line:723
                if OO000OOO0O00O0OO0 [OOO0000O0O00OOOO0 ]>0 :#line:724
                    if OO0000OOOOO000000 [OOO0000O0O00OOOO0 ]/sum (OO0000OOOOO000000 )>OO000OOO0O00O0OO0 [OOO0000O0O00OOOO0 ]/sum (OO000OOO0O00O0OO0 ):#line:725
                        O00OO00O00OOOO0OO +=OO000OOOOO0OOO0OO [OOO0000O0O00OOOO0 ]*((OO0000OOOOO000000 [OOO0000O0O00OOOO0 ]/sum (OO0000OOOOO000000 ))/(OO000OOO0O00O0OO0 [OOO0000O0O00OOOO0 ]/sum (OO000OOO0O00O0OO0 ))-1 )#line:726
                if OO000OOOOO0OOO0OO [OOO0000O0O00OOOO0 ]>0 :#line:727
                    OO00OOO0OO00OO00O +=OO0000OOOOO000000 [OOO0000O0O00OOOO0 ]#line:728
                    O000OOOO000000OO0 +=OO000OOO0O00O0OO0 [OOO0000O0O00OOOO0 ]#line:729
        OO00O00OO0O0000OO =0 #line:730
        if sum (OO0000OOOOO000000 )>0 and O000OOOO000000OO0 >0 :#line:731
            OO00O00OO0O0000OO =(OO00OOO0OO00OO00O /sum (OO0000OOOOO000000 ))/(O000OOOO000000OO0 /sum (OO000OOO0O00O0OO0 ))#line:732
        OO0000OOO0OO0OO0O =True #line:736
        for OOO000000OO00OOOO in O00OOOO0O000O000O .quantifiers .keys ():#line:737
            if OOO000000OO00OOOO .upper ()=='BASE':#line:738
                OO0000OOO0OO0OO0O =OO0000OOO0OO0OO0O and (O00OOOO0O000O000O .quantifiers .get (OOO000000OO00OOOO )<=O0000OO00OO000OOO )#line:739
            if OOO000000OO00OOOO .upper ()=='RELBASE':#line:740
                OO0000OOO0OO0OO0O =OO0000OOO0OO0OO0O and (O00OOOO0O000O000O .quantifiers .get (OOO000000OO00OOOO )<=O0000OO00OO000OOO *1.0 /O00OOOO0O000O000O .data ["rows_count"])#line:741
            if OOO000000OO00OOOO .upper ()=='AAD_SCORE':#line:742
                OO0000OOO0OO0OO0O =OO0000OOO0OO0OO0O and (O00OOOO0O000O000O .quantifiers .get (OOO000000OO00OOOO )<=O00OO00O00OOOO0OO )#line:743
            if OOO000000OO00OOOO .upper ()=='RELEVANT_CAT_BASE':#line:744
                OO0000OOO0OO0OO0O =OO0000OOO0OO0OO0O and (O00OOOO0O000O000O .quantifiers .get (OOO000000OO00OOOO )<=OO00OOO0OO00OO00O )#line:745
            if OOO000000OO00OOOO .upper ()=='RELEVANT_BASE_LIFT':#line:746
                OO0000OOO0OO0OO0O =OO0000OOO0OO0OO0O and (O00OOOO0O000O000O .quantifiers .get (OOO000000OO00OOOO )<=OO00O00OO0O0000OO )#line:747
        OO000O00O00OOOO00 ={}#line:748
        if OO0000OOO0OO0OO0O ==True :#line:749
            O00OOOO0O000O000O .stats ['total_valid']+=1 #line:750
            OO000O00O00OOOO00 ["base"]=O0000OO00OO000OOO #line:751
            OO000O00O00OOOO00 ["rel_base"]=O0000OO00OO000OOO *1.0 /O00OOOO0O000O000O .data ["rows_count"]#line:752
            OO000O00O00OOOO00 ["hist"]=OO0000OOOOO000000 #line:753
            OO000O00O00OOOO00 ["aad_score"]=O00OO00O00OOOO0OO #line:754
            OO000O00O00OOOO00 ["hist_cond"]=OO000OOO0O00O0OO0 #line:755
            OO000O00O00OOOO00 ["rel_hist"]=[O000OO0O0O000O000 /sum (OO0000OOOOO000000 )for O000OO0O0O000O000 in OO0000OOOOO000000 ]#line:756
            OO000O00O00OOOO00 ["rel_hist_cond"]=[OO0OO0O00OOO00000 /sum (OO000OOO0O00O0OO0 )for OO0OO0O00OOO00000 in OO000OOO0O00O0OO0 ]#line:757
            OO000O00O00OOOO00 ["relevant_base_lift"]=OO00O00OO0O0000OO #line:758
            OO000O00O00OOOO00 ["relevant_cat_base"]=OO00OOO0OO00OO00O #line:759
            OO000O00O00OOOO00 ["relevant_cat_base_full"]=O000OOOO000000OO0 #line:760
        return OO0000OOO0OO0OO0O ,OO000O00O00OOOO00 #line:761
    def _verify4ft (OO00O00OOO00000OO ,_O00O0OO000O0O000O ,_trace_cedent =None ,_traces =None ):#line:763
        O0O00O0O0OOO0OOO0 ={}#line:764
        O0000OOOO0OOO0O0O =0 #line:765
        for O0OOO0O0000OOO0O0 in OO00O00OOO00000OO .task_actinfo ['cedents']:#line:766
            O0O00O0O0OOO0OOO0 [O0OOO0O0000OOO0O0 ['cedent_type']]=O0OOO0O0000OOO0O0 ['filter_value']#line:767
            O0000OOOO0OOO0O0O =O0000OOOO0OOO0O0O +1 #line:768
        O00O00OO00OO00O0O =OO00O00OOO00000OO ._bitcount (O0O00O0O0OOO0OOO0 ['ante']&O0O00O0O0OOO0OOO0 ['succ']&O0O00O0O0OOO0OOO0 ['cond'])#line:769
        O00O0000O00O000OO =None #line:770
        O00O0000O00O000OO =0 #line:771
        if O00O00OO00OO00O0O >0 :#line:772
            O00O0000O00O000OO =OO00O00OOO00000OO ._bitcount (O0O00O0O0OOO0OOO0 ['ante']&O0O00O0O0OOO0OOO0 ['succ']&O0O00O0O0OOO0OOO0 ['cond'])*1.0 /OO00O00OOO00000OO ._bitcount (O0O00O0O0OOO0OOO0 ['ante']&O0O00O0O0OOO0OOO0 ['cond'])#line:773
        OOO0O0O00O00000OO =1 <<OO00O00OOO00000OO .data ["rows_count"]#line:775
        O0O00000000OOO000 =OO00O00OOO00000OO ._bitcount (O0O00O0O0OOO0OOO0 ['ante']&O0O00O0O0OOO0OOO0 ['succ']&O0O00O0O0OOO0OOO0 ['cond'])#line:776
        O0OO0000OOOOO0O0O =OO00O00OOO00000OO ._bitcount (O0O00O0O0OOO0OOO0 ['ante']&~(OOO0O0O00O00000OO |O0O00O0O0OOO0OOO0 ['succ'])&O0O00O0O0OOO0OOO0 ['cond'])#line:777
        O0OOO0O0000OOO0O0 =OO00O00OOO00000OO ._bitcount (~(OOO0O0O00O00000OO |O0O00O0O0OOO0OOO0 ['ante'])&O0O00O0O0OOO0OOO0 ['succ']&O0O00O0O0OOO0OOO0 ['cond'])#line:778
        O000O000OOO0OO0OO =OO00O00OOO00000OO ._bitcount (~(OOO0O0O00O00000OO |O0O00O0O0OOO0OOO0 ['ante'])&~(OOO0O0O00O00000OO |O0O00O0O0OOO0OOO0 ['succ'])&O0O00O0O0OOO0OOO0 ['cond'])#line:779
        OO00000OOOO00O0OO =0 #line:780
        OO00O0O0O0OOO00OO =0 #line:781
        if (O0O00000000OOO000 +O0OO0000OOOOO0O0O )*(O0O00000000OOO000 +O0OOO0O0000OOO0O0 )>0 :#line:782
            OO00000OOOO00O0OO =O0O00000000OOO000 *(O0O00000000OOO000 +O0OO0000OOOOO0O0O +O0OOO0O0000OOO0O0 +O000O000OOO0OO0OO )/(O0O00000000OOO000 +O0OO0000OOOOO0O0O )/(O0O00000000OOO000 +O0OOO0O0000OOO0O0 )-1 #line:783
            OO00O0O0O0OOO00OO =OO00000OOOO00O0OO +1 #line:784
        else :#line:785
            OO00000OOOO00O0OO =None #line:786
            OO00O0O0O0OOO00OO =None #line:787
        O0O00OO000000O00O =0 #line:788
        if (O0O00000000OOO000 +O0OO0000OOOOO0O0O )*(O0O00000000OOO000 +O0OOO0O0000OOO0O0 )>0 :#line:789
            O0O00OO000000O00O =1 -O0O00000000OOO000 *(O0O00000000OOO000 +O0OO0000OOOOO0O0O +O0OOO0O0000OOO0O0 +O000O000OOO0OO0OO )/(O0O00000000OOO000 +O0OO0000OOOOO0O0O )/(O0O00000000OOO000 +O0OOO0O0000OOO0O0 )#line:790
        else :#line:791
            O0O00OO000000O00O =None #line:792
        O000OO0O0OOOO00OO =True #line:793
        for O00O0OO00OO000OO0 in OO00O00OOO00000OO .quantifiers .keys ():#line:794
            if O00O0OO00OO000OO0 .upper ()=='BASE':#line:795
                O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and (OO00O00OOO00000OO .quantifiers .get (O00O0OO00OO000OO0 )<=O00O00OO00OO00O0O )#line:796
            if O00O0OO00OO000OO0 .upper ()=='RELBASE':#line:797
                O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and (OO00O00OOO00000OO .quantifiers .get (O00O0OO00OO000OO0 )<=O00O00OO00OO00O0O *1.0 /OO00O00OOO00000OO .data ["rows_count"])#line:798
            if (O00O0OO00OO000OO0 .upper ()=='PIM')or (O00O0OO00OO000OO0 .upper ()=='CONF'):#line:799
                O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and (OO00O00OOO00000OO .quantifiers .get (O00O0OO00OO000OO0 )<=O00O0000O00O000OO )#line:800
            if O00O0OO00OO000OO0 .upper ()=='AAD':#line:801
                if OO00000OOOO00O0OO !=None :#line:802
                    O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and (OO00O00OOO00000OO .quantifiers .get (O00O0OO00OO000OO0 )<=OO00000OOOO00O0OO )#line:803
                else :#line:804
                    O000OO0O0OOOO00OO =False #line:805
            if O00O0OO00OO000OO0 .upper ()=='BAD':#line:806
                if O0O00OO000000O00O !=None :#line:807
                    O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and (OO00O00OOO00000OO .quantifiers .get (O00O0OO00OO000OO0 )<=O0O00OO000000O00O )#line:808
                else :#line:809
                    O000OO0O0OOOO00OO =False #line:810
            if O00O0OO00OO000OO0 .upper ()=='LAMBDA'or O00O0OO00OO000OO0 .upper ()=='FN':#line:811
                OOO0O00O00O0O00OO =OO00O00OOO00000OO .quantifiers .get (O00O0OO00OO000OO0 )#line:812
                O000OO0O0O000OO00 =[O0O00000000OOO000 ,O0OO0000OOOOO0O0O ,O0OOO0O0000OOO0O0 ,O000O000OOO0OO0OO ]#line:813
                O0000O0OO00O00OOO =OOO0O00O00O0O00OO .__code__ .co_argcount #line:814
                if O0000O0OO00O00OOO ==1 :#line:816
                    O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and OOO0O00O00O0O00OO (O000OO0O0O000OO00 )#line:817
                elif O0000O0OO00O00OOO ==2 :#line:818
                    OOOO0000O0OO000OO ={}#line:819
                    O0000OO0OO00OOOOO ={}#line:820
                    O0000OO0OO00OOOOO ["varname"]=OO00O00OOO00000OO .data ["varname"]#line:821
                    O0000OO0OO00OOOOO ["catnames"]=OO00O00OOO00000OO .data ["catnames"]#line:822
                    OOOO0000O0OO000OO ['datalabels']=O0000OO0OO00OOOOO #line:823
                    OOOO0000O0OO000OO ['trace_cedent']=_trace_cedent #line:824
                    OOOO0000O0OO000OO ['traces']=_traces #line:825
                    O000OO0O0OOOO00OO =O000OO0O0OOOO00OO and OOO0O00O00O0O00OO (O000OO0O0O000OO00 ,OOOO0000O0OO000OO )#line:828
                else :#line:829
                    print (f"Unsupported number of arguments for lambda function ({O0000O0OO00O00OOO} for procedure SD4ft-Miner")#line:830
            O00OO0O000OO000OO ={}#line:831
        if O000OO0O0OOOO00OO ==True :#line:832
            OO00O00OOO00000OO .stats ['total_valid']+=1 #line:833
            O00OO0O000OO000OO ["base"]=O00O00OO00OO00O0O #line:834
            O00OO0O000OO000OO ["rel_base"]=O00O00OO00OO00O0O *1.0 /OO00O00OOO00000OO .data ["rows_count"]#line:835
            O00OO0O000OO000OO ["conf"]=O00O0000O00O000OO #line:836
            O00OO0O000OO000OO ["aad"]=OO00000OOOO00O0OO #line:837
            O00OO0O000OO000OO ["bad"]=O0O00OO000000O00O #line:838
            O00OO0O000OO000OO ["fourfold"]=[O0O00000000OOO000 ,O0OO0000OOOOO0O0O ,O0OOO0O0000OOO0O0 ,O000O000OOO0OO0OO ]#line:839
        return O000OO0O0OOOO00OO ,O00OO0O000OO000OO #line:840
    def _verifysd4ft (O0OO0OO000O00OO0O ,_OOOO0O0OO000O0OOO ):#line:842
        OOOOO00O0OOOO0O00 ={}#line:843
        O0OO00000OOOO0O00 =0 #line:844
        for O0000O0O0OOOO000O in O0OO0OO000O00OO0O .task_actinfo ['cedents']:#line:845
            OOOOO00O0OOOO0O00 [O0000O0O0OOOO000O ['cedent_type']]=O0000O0O0OOOO000O ['filter_value']#line:846
            O0OO00000OOOO0O00 =O0OO00000OOOO0O00 +1 #line:847
        OO00O0OOO0O000O0O =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])#line:848
        OO0O0OO0O000O000O =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])#line:849
        O0OOOOOO0O0OOO000 =None #line:850
        O000O00OOOO00000O =0 #line:851
        O00O000O00OO0O0OO =0 #line:852
        if OO00O0OOO0O000O0O >0 :#line:853
            O000O00OOOO00000O =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])*1.0 /O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])#line:854
        if OO0O0OO0O000O000O >0 :#line:855
            O00O000O00OO0O0OO =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])*1.0 /O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])#line:856
        OOOOO000O0OOO0000 =1 <<O0OO0OO000O00OO0O .data ["rows_count"]#line:858
        OOO0OO00OOO000OOO =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])#line:859
        O00OOO0O0OO0O0O0O =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['succ'])&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])#line:860
        OO00000O0O00OOOOO =O0OO0OO000O00OO0O ._bitcount (~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['ante'])&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])#line:861
        O0OO0OOO0OO00OOO0 =O0OO0OO000O00OO0O ._bitcount (~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['ante'])&~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['succ'])&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['frst'])#line:862
        OO00OO0O00000OOO0 =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])#line:863
        O000O0OO00OO000O0 =O0OO0OO000O00OO0O ._bitcount (OOOOO00O0OOOO0O00 ['ante']&~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['succ'])&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])#line:864
        O0O0OOOO0O00OO000 =O0OO0OO000O00OO0O ._bitcount (~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['ante'])&OOOOO00O0OOOO0O00 ['succ']&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])#line:865
        OO00000OOO00O00O0 =O0OO0OO000O00OO0O ._bitcount (~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['ante'])&~(OOOOO000O0OOO0000 |OOOOO00O0OOOO0O00 ['succ'])&OOOOO00O0OOOO0O00 ['cond']&OOOOO00O0OOOO0O00 ['scnd'])#line:866
        OO0OO0000000OOO00 =True #line:867
        for OOOOOO00O0O0O00OO in O0OO0OO000O00OO0O .quantifiers .keys ():#line:868
            if (OOOOOO00O0O0O00OO .upper ()=='FRSTBASE')|(OOOOOO00O0O0O00OO .upper ()=='BASE1'):#line:869
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=OO00O0OOO0O000O0O )#line:870
            if (OOOOOO00O0O0O00OO .upper ()=='SCNDBASE')|(OOOOOO00O0O0O00OO .upper ()=='BASE2'):#line:871
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=OO0O0OO0O000O000O )#line:872
            if (OOOOOO00O0O0O00OO .upper ()=='FRSTRELBASE')|(OOOOOO00O0O0O00OO .upper ()=='RELBASE1'):#line:873
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=OO00O0OOO0O000O0O *1.0 /O0OO0OO000O00OO0O .data ["rows_count"])#line:874
            if (OOOOOO00O0O0O00OO .upper ()=='SCNDRELBASE')|(OOOOOO00O0O0O00OO .upper ()=='RELBASE2'):#line:875
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=OO0O0OO0O000O000O *1.0 /O0OO0OO000O00OO0O .data ["rows_count"])#line:876
            if (OOOOOO00O0O0O00OO .upper ()=='FRSTPIM')|(OOOOOO00O0O0O00OO .upper ()=='PIM1')|(OOOOOO00O0O0O00OO .upper ()=='FRSTCONF')|(OOOOOO00O0O0O00OO .upper ()=='CONF1'):#line:877
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=O000O00OOOO00000O )#line:878
            if (OOOOOO00O0O0O00OO .upper ()=='SCNDPIM')|(OOOOOO00O0O0O00OO .upper ()=='PIM2')|(OOOOOO00O0O0O00OO .upper ()=='SCNDCONF')|(OOOOOO00O0O0O00OO .upper ()=='CONF2'):#line:879
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=O00O000O00OO0O0OO )#line:880
            if (OOOOOO00O0O0O00OO .upper ()=='DELTAPIM')|(OOOOOO00O0O0O00OO .upper ()=='DELTACONF'):#line:881
                OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=O000O00OOOO00000O -O00O000O00OO0O0OO )#line:882
            if (OOOOOO00O0O0O00OO .upper ()=='RATIOPIM')|(OOOOOO00O0O0O00OO .upper ()=='RATIOCONF'):#line:883
                if (O00O000O00OO0O0OO >0 ):#line:884
                    OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )<=O000O00OOOO00000O *1.0 /O00O000O00OO0O0OO )#line:885
                else :#line:886
                    OO0OO0000000OOO00 =False #line:887
            if (OOOOOO00O0O0O00OO .upper ()=='RATIOPIM_LEQ')|(OOOOOO00O0O0O00OO .upper ()=='RATIOCONF_LEQ'):#line:888
                if (O00O000O00OO0O0OO >0 ):#line:889
                    OO0OO0000000OOO00 =OO0OO0000000OOO00 and (O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )>=O000O00OOOO00000O *1.0 /O00O000O00OO0O0OO )#line:890
                else :#line:891
                    OO0OO0000000OOO00 =False #line:892
            if OOOOOO00O0O0O00OO .upper ()=='LAMBDA'or OOOOOO00O0O0O00OO .upper ()=='FN':#line:893
                OOOO0OO00OO00O0O0 =O0OO0OO000O00OO0O .quantifiers .get (OOOOOO00O0O0O00OO )#line:894
                O00O0000OO00000O0 =OOOO0OO00OO00O0O0 .func_code .co_argcount #line:895
                O00O00OOO0O0O0O0O =[OOO0OO00OOO000OOO ,O00OOO0O0OO0O0O0O ,OO00000O0O00OOOOO ,O0OO0OOO0OO00OOO0 ]#line:896
                O0O0O000OOO0O0O00 =[OO00OO0O00000OOO0 ,O000O0OO00OO000O0 ,O0O0OOOO0O00OO000 ,OO00000OOO00O00O0 ]#line:897
                if O00O0000OO00000O0 ==2 :#line:898
                    OO0OO0000000OOO00 =OO0OO0000000OOO00 and OOOO0OO00OO00O0O0 (O00O00OOO0O0O0O0O ,O0O0O000OOO0O0O00 )#line:899
                elif O00O0000OO00000O0 ==3 :#line:900
                    OO0OO0000000OOO00 =OO0OO0000000OOO00 and OOOO0OO00OO00O0O0 (O00O00OOO0O0O0O0O ,O0O0O000OOO0O0O00 ,None )#line:901
                else :#line:902
                    print (f"Unsupported number of arguments for lambda function ({O00O0000OO00000O0} for procedure SD4ft-Miner")#line:903
        OO00O00O0O0OO0OO0 ={}#line:904
        if OO0OO0000000OOO00 ==True :#line:905
            O0OO0OO000O00OO0O .stats ['total_valid']+=1 #line:906
            OO00O00O0O0OO0OO0 ["base1"]=OO00O0OOO0O000O0O #line:907
            OO00O00O0O0OO0OO0 ["base2"]=OO0O0OO0O000O000O #line:908
            OO00O00O0O0OO0OO0 ["rel_base1"]=OO00O0OOO0O000O0O *1.0 /O0OO0OO000O00OO0O .data ["rows_count"]#line:909
            OO00O00O0O0OO0OO0 ["rel_base2"]=OO0O0OO0O000O000O *1.0 /O0OO0OO000O00OO0O .data ["rows_count"]#line:910
            OO00O00O0O0OO0OO0 ["conf1"]=O000O00OOOO00000O #line:911
            OO00O00O0O0OO0OO0 ["conf2"]=O00O000O00OO0O0OO #line:912
            OO00O00O0O0OO0OO0 ["deltaconf"]=O000O00OOOO00000O -O00O000O00OO0O0OO #line:913
            if (O00O000O00OO0O0OO >0 ):#line:914
                OO00O00O0O0OO0OO0 ["ratioconf"]=O000O00OOOO00000O *1.0 /O00O000O00OO0O0OO #line:915
            else :#line:916
                OO00O00O0O0OO0OO0 ["ratioconf"]=None #line:917
            OO00O00O0O0OO0OO0 ["fourfold1"]=[OOO0OO00OOO000OOO ,O00OOO0O0OO0O0O0O ,OO00000O0O00OOOOO ,O0OO0OOO0OO00OOO0 ]#line:918
            OO00O00O0O0OO0OO0 ["fourfold2"]=[OO00OO0O00000OOO0 ,O000O0OO00OO000O0 ,O0O0OOOO0O00OO000 ,OO00000OOO00O00O0 ]#line:919
        return OO0OO0000000OOO00 ,OO00O00O0O0OO0OO0 #line:920
    def _verify_opt (OOOO000O0OOOOOOOO ,O0O0O0OO0OO00O0O0 ,O00O0OOO0OOO0OOO0 ):#line:923
        OOOO000O0OOOOOOOO .stats ['total_ver']+=1 #line:924
        OO0O0OO00OOOO00OO =False #line:925
        if not (O0O0O0OO0OO00O0O0 ['optim'].get ('only_con')):#line:926
            return False #line:927
        if OOOO000O0OOOOOOOO .verbosity ['debug']:#line:928
            print (OOOO000O0OOOOOOOO .options ['optimizations'])#line:929
        if not (OOOO000O0OOOOOOOO .options ['optimizations']):#line:930
            if OOOO000O0OOOOOOOO .verbosity ['debug']:#line:931
                print ("NO OPTS")#line:932
            return False #line:933
        if OOOO000O0OOOOOOOO .verbosity ['debug']:#line:934
            print ("OPTS")#line:935
        OOOOOOOO0O000OO00 ={}#line:936
        for O0000OO0OO0000O0O in OOOO000O0OOOOOOOO .task_actinfo ['cedents']:#line:937
            if OOOO000O0OOOOOOOO .verbosity ['debug']:#line:938
                print (O0000OO0OO0000O0O ['cedent_type'])#line:939
            OOOOOOOO0O000OO00 [O0000OO0OO0000O0O ['cedent_type']]=O0000OO0OO0000O0O ['filter_value']#line:940
            if OOOO000O0OOOOOOOO .verbosity ['debug']:#line:941
                print (O0000OO0OO0000O0O ['cedent_type']+" : "+str (O0000OO0OO0000O0O ['filter_value']))#line:942
        O000OOO0O0OOOO00O =1 <<OOOO000O0OOOOOOOO .data ["rows_count"]#line:943
        OO0O0O0O0OOO0O000 =O000OOO0O0OOOO00O -1 #line:944
        OOO0OOOO000O0O00O =""#line:945
        O0O0000O0000OO00O =0 #line:946
        if (OOOOOOOO0O000OO00 .get ('ante')!=None ):#line:947
            OO0O0O0O0OOO0O000 =OO0O0O0O0OOO0O000 &OOOOOOOO0O000OO00 ['ante']#line:948
        if (OOOOOOOO0O000OO00 .get ('succ')!=None ):#line:949
            OO0O0O0O0OOO0O000 =OO0O0O0O0OOO0O000 &OOOOOOOO0O000OO00 ['succ']#line:950
        if (OOOOOOOO0O000OO00 .get ('cond')!=None ):#line:951
            OO0O0O0O0OOO0O000 =OO0O0O0O0OOO0O000 &OOOOOOOO0O000OO00 ['cond']#line:952
        O0O0O0O00OO00000O =None #line:953
        if (OOOO000O0OOOOOOOO .proc =='CFMiner')|(OOOO000O0OOOOOOOO .proc =='4ftMiner')|(OOOO000O0OOOOOOOO .proc =='UICMiner'):#line:954
            O0OOOO0OO00000O0O =OOOO000O0OOOOOOOO ._bitcount (OO0O0O0O0OOO0O000 )#line:955
            if not (OOOO000O0OOOOOOOO ._opt_base ==None ):#line:956
                if not (OOOO000O0OOOOOOOO ._opt_base <=O0OOOO0OO00000O0O ):#line:957
                    OO0O0OO00OOOO00OO =True #line:958
            if not (OOOO000O0OOOOOOOO ._opt_relbase ==None ):#line:959
                if not (OOOO000O0OOOOOOOO ._opt_relbase <=O0OOOO0OO00000O0O *1.0 /OOOO000O0OOOOOOOO .data ["rows_count"]):#line:960
                    OO0O0OO00OOOO00OO =True #line:961
        if (OOOO000O0OOOOOOOO .proc =='SD4ftMiner'):#line:962
            O0OOOO0OO00000O0O =OOOO000O0OOOOOOOO ._bitcount (OO0O0O0O0OOO0O000 )#line:963
            if (not (OOOO000O0OOOOOOOO ._opt_base1 ==None ))&(not (OOOO000O0OOOOOOOO ._opt_base2 ==None )):#line:964
                if not (max (OOOO000O0OOOOOOOO ._opt_base1 ,OOOO000O0OOOOOOOO ._opt_base2 )<=O0OOOO0OO00000O0O ):#line:965
                    OO0O0OO00OOOO00OO =True #line:966
            if (not (OOOO000O0OOOOOOOO ._opt_relbase1 ==None ))&(not (OOOO000O0OOOOOOOO ._opt_relbase2 ==None )):#line:967
                if not (max (OOOO000O0OOOOOOOO ._opt_relbase1 ,OOOO000O0OOOOOOOO ._opt_relbase2 )<=O0OOOO0OO00000O0O *1.0 /OOOO000O0OOOOOOOO .data ["rows_count"]):#line:968
                    OO0O0OO00OOOO00OO =True #line:969
        return OO0O0OO00OOOO00OO #line:971
    def _print (OOO00O0O00000O0O0 ,OO0OO000OO000000O ,_OOO0O0OOO0OOOO0O0 ,_OOOO000OO0000000O ):#line:974
        if (len (_OOO0O0OOO0OOOO0O0 ))!=len (_OOOO000OO0000000O ):#line:975
            print ("DIFF IN LEN for following cedent : "+str (len (_OOO0O0OOO0OOOO0O0 ))+" vs "+str (len (_OOOO000OO0000000O )))#line:976
            print ("trace cedent : "+str (_OOO0O0OOO0OOOO0O0 )+", traces "+str (_OOOO000OO0000000O ))#line:977
        OO0OOOOOOOOOOOOO0 =''#line:978
        OOOO0O0O0OO00O000 ={}#line:979
        O0O0O0OOO0O00O000 =[]#line:980
        for OOOO000O0OO0OO0OO in range (len (_OOO0O0OOO0OOOO0O0 )):#line:981
            OO0O0O000O0O0OOOO =OOO00O0O00000O0O0 .data ["varname"].index (OO0OO000OO000000O ['defi'].get ('attributes')[_OOO0O0OOO0OOOO0O0 [OOOO000O0OO0OO0OO ]].get ('name'))#line:982
            OO0OOOOOOOOOOOOO0 =OO0OOOOOOOOOOOOO0 +OOO00O0O00000O0O0 .data ["varname"][OO0O0O000O0O0OOOO ]+'('#line:983
            O0O0O0OOO0O00O000 .append (OO0O0O000O0O0OOOO )#line:984
            OO00OOOO0O000OO00 =[]#line:985
            for OO0000O0OOOOOO00O in _OOOO000OO0000000O [OOOO000O0OO0OO0OO ]:#line:986
                OO0OOOOOOOOOOOOO0 =OO0OOOOOOOOOOOOO0 +str (OOO00O0O00000O0O0 .data ["catnames"][OO0O0O000O0O0OOOO ][OO0000O0OOOOOO00O ])+" "#line:987
                OO00OOOO0O000OO00 .append (str (OOO00O0O00000O0O0 .data ["catnames"][OO0O0O000O0O0OOOO ][OO0000O0OOOOOO00O ]))#line:988
            OO0OOOOOOOOOOOOO0 =OO0OOOOOOOOOOOOO0 [:-1 ]+')'#line:989
            OOOO0O0O0OO00O000 [OOO00O0O00000O0O0 .data ["varname"][OO0O0O000O0O0OOOO ]]=OO00OOOO0O000OO00 #line:990
            if OOOO000O0OO0OO0OO +1 <len (_OOO0O0OOO0OOOO0O0 ):#line:991
                OO0OOOOOOOOOOOOO0 =OO0OOOOOOOOOOOOO0 +' & '#line:992
        return OO0OOOOOOOOOOOOO0 ,OOOO0O0O0OO00O000 ,O0O0O0OOO0O00O000 #line:993
    def _print_hypo (O000OO0O00O0O0O0O ,O0OOO0OOO00OO0OOO ):#line:995
        O000OO0O00O0O0O0O .print_rule (O0OOO0OOO00OO0OOO )#line:996
    def _print_rule (O00OOO00O000000OO ,OOO0O0O0OO0O00OO0 ):#line:998
        if O00OOO00O000000OO .verbosity ['print_rules']:#line:999
            print ('Rules info : '+str (OOO0O0O0OO0O00OO0 ['params']))#line:1000
            for OO0OOOOOOO0O000O0 in O00OOO00O000000OO .task_actinfo ['cedents']:#line:1001
                print (OO0OOOOOOO0O000O0 ['cedent_type']+' = '+OO0OOOOOOO0O000O0 ['generated_string'])#line:1002
    def _genvar (OOOO0000O000OOO00 ,O00O0O00000OO0OO0 ,O00O00O0OO000O0OO ,_O0O0OO00000OO0000 ,_O0O000000O00O0O0O ,_O00000000OOOO00OO ,_OO0OOOO0000OO00O0 ,_OO000OO0OOOOO0OO0 ,_OO0000OOOOOOO00OO ,_OOO0000000O000OOO ):#line:1004
        _O000O0O0O00OOO0OO =0 #line:1005
        _O00O0OO00O0OOO0O0 =[]#line:1006
        for OO0OOO000O0OO0OO0 in range (O00O00O0OO000O0OO ['num_cedent']):#line:1007
            if ('force'in O00O00O0OO000O0OO ['defi'].get ('attributes')[OO0OOO000O0OO0OO0 ]and O00O00O0OO000O0OO ['defi'].get ('attributes')[OO0OOO000O0OO0OO0 ].get ('force')):#line:1009
                _O00O0OO00O0OOO0O0 .append (OO0OOO000O0OO0OO0 )#line:1010
        if O00O00O0OO000O0OO ['num_cedent']>0 :#line:1011
            _O000O0O0O00OOO0OO =(_OOO0000000O000OOO -_OO0000OOOOOOO00OO )/O00O00O0OO000O0OO ['num_cedent']#line:1012
        if O00O00O0OO000O0OO ['num_cedent']==0 :#line:1013
            if len (O00O0O00000OO0OO0 ['cedents_to_do'])>len (O00O0O00000OO0OO0 ['cedents']):#line:1014
                OO0000O00O0O0OOO0 ,OOOOOOOOOOOOO00O0 ,O0OO0OO0OOO000000 =OOOO0000O000OOO00 ._print (O00O00O0OO000O0OO ,_O0O0OO00000OO0000 ,_O0O000000O00O0O0O )#line:1015
                O00O00O0OO000O0OO ['generated_string']=OO0000O00O0O0OOO0 #line:1016
                O00O00O0OO000O0OO ['rule']=OOOOOOOOOOOOO00O0 #line:1017
                O00O00O0OO000O0OO ['filter_value']=(1 <<OOOO0000O000OOO00 .data ["rows_count"])-1 #line:1018
                O00O00O0OO000O0OO ['traces']=[]#line:1019
                O00O00O0OO000O0OO ['trace_cedent']=[]#line:1020
                O00O00O0OO000O0OO ['trace_cedent_asindata']=[]#line:1021
                O00O0O00000OO0OO0 ['cedents'].append (O00O00O0OO000O0OO )#line:1022
                _O0O0OO00000OO0000 .append (None )#line:1023
                OOOO0000O000OOO00 ._start_cedent (O00O0O00000OO0OO0 ,_OO0000OOOOOOO00OO ,_OOO0000000O000OOO )#line:1024
                O00O0O00000OO0OO0 ['cedents'].pop ()#line:1025
        for OO0OOO000O0OO0OO0 in range (O00O00O0OO000O0OO ['num_cedent']):#line:1028
            _O000OO00O0OOO0000 =True #line:1029
            for O00000O0O0O00O0O0 in range (len (_O00O0OO00O0OOO0O0 )):#line:1030
                if O00000O0O0O00O0O0 <OO0OOO000O0OO0OO0 and O00000O0O0O00O0O0 not in _O0O0OO00000OO0000 and O00000O0O0O00O0O0 in _O00O0OO00O0OOO0O0 :#line:1031
                    _O000OO00O0OOO0000 =False #line:1032
            if (len (_O0O0OO00000OO0000 )==0 or OO0OOO000O0OO0OO0 >_O0O0OO00000OO0000 [-1 ])and _O000OO00O0OOO0000 :#line:1034
                _O0O0OO00000OO0000 .append (OO0OOO000O0OO0OO0 )#line:1035
                O0O0OOOO0O0O00OOO =OOOO0000O000OOO00 .data ["varname"].index (O00O00O0OO000O0OO ['defi'].get ('attributes')[OO0OOO000O0OO0OO0 ].get ('name'))#line:1036
                _O0OO00OO00O0O00OO =O00O00O0OO000O0OO ['defi'].get ('attributes')[OO0OOO000O0OO0OO0 ].get ('minlen')#line:1037
                _O00OOO000O0OOOOOO =O00O00O0OO000O0OO ['defi'].get ('attributes')[OO0OOO000O0OO0OO0 ].get ('maxlen')#line:1038
                _OOOO00000O0OOOOO0 =O00O00O0OO000O0OO ['defi'].get ('attributes')[OO0OOO000O0OO0OO0 ].get ('type')#line:1039
                OOO0OOOO0O0OOO0OO =len (OOOO0000O000OOO00 .data ["dm"][O0O0OOOO0O0O00OOO ])#line:1040
                _OOO00O0OO0OO0O0O0 =[]#line:1041
                _O0O000000O00O0O0O .append (_OOO00O0OO0OO0O0O0 )#line:1042
                _OOO000O0O00OOOOOO =int (0 )#line:1043
                OOOO0000O000OOO00 ._gencomb (O00O0O00000OO0OO0 ,O00O00O0OO000O0OO ,_O0O0OO00000OO0000 ,_O0O000000O00O0O0O ,_OOO00O0OO0OO0O0O0 ,_O00000000OOOO00OO ,_OOO000O0O00OOOOOO ,OOO0OOOO0O0OOO0OO ,_OOOO00000O0OOOOO0 ,_OO0OOOO0000OO00O0 ,_OO000OO0OOOOO0OO0 ,_O0OO00OO00O0O00OO ,_O00OOO000O0OOOOOO ,_OO0000OOOOOOO00OO +OO0OOO000O0OO0OO0 *_O000O0O0O00OOO0OO ,_OO0000OOOOOOO00OO +(OO0OOO000O0OO0OO0 +1 )*_O000O0O0O00OOO0OO )#line:1044
                _O0O000000O00O0O0O .pop ()#line:1045
                _O0O0OO00000OO0000 .pop ()#line:1046
    def _gencomb (OO00O00O0O00OOO00 ,OOOO00OO00OO00OOO ,O0OO00OOO0OOO0OO0 ,_O000000O0O0O0OOOO ,_O000O00000O0O0O00 ,_O00O00O000OO000O0 ,_O00OOOO000O0OO00O ,_OO00OOO0OOO000O0O ,O0OO0O0OOOOOO0O00 ,_O00O0OOOOO000000O ,_OO0O0O00000O00000 ,_O0O0O00OOO000O0OO ,_O00O0O000OO00O00O ,_OO00O00OO0O00000O ,_O000O00O000O00O0O ,_O00O00OOO0O0OOO00 ,val_list =None ):#line:1048
        _OO0O0OO00OO0OO0O0 =[]#line:1049
        _O00O000OO0000O00O =val_list #line:1050
        if _O00O0OOOOO000000O =="subset":#line:1051
            if len (_O00O00O000OO000O0 )==0 :#line:1052
                _OO0O0OO00OO0OO0O0 =range (O0OO0O0OOOOOO0O00 )#line:1053
            else :#line:1054
                _OO0O0OO00OO0OO0O0 =range (_O00O00O000OO000O0 [-1 ]+1 ,O0OO0O0OOOOOO0O00 )#line:1055
        elif _O00O0OOOOO000000O =="seq":#line:1056
            if len (_O00O00O000OO000O0 )==0 :#line:1057
                _OO0O0OO00OO0OO0O0 =range (O0OO0O0OOOOOO0O00 -_O00O0O000OO00O00O +1 )#line:1058
            else :#line:1059
                if _O00O00O000OO000O0 [-1 ]+1 ==O0OO0O0OOOOOO0O00 :#line:1060
                    return #line:1061
                OOOO00OOO0O0OOO0O =_O00O00O000OO000O0 [-1 ]+1 #line:1062
                _OO0O0OO00OO0OO0O0 .append (OOOO00OOO0O0OOO0O )#line:1063
        elif _O00O0OOOOO000000O =="lcut":#line:1064
            if len (_O00O00O000OO000O0 )==0 :#line:1065
                OOOO00OOO0O0OOO0O =0 ;#line:1066
            else :#line:1067
                if _O00O00O000OO000O0 [-1 ]+1 ==O0OO0O0OOOOOO0O00 :#line:1068
                    return #line:1069
                OOOO00OOO0O0OOO0O =_O00O00O000OO000O0 [-1 ]+1 #line:1070
            _OO0O0OO00OO0OO0O0 .append (OOOO00OOO0O0OOO0O )#line:1071
        elif _O00O0OOOOO000000O =="rcut":#line:1072
            if len (_O00O00O000OO000O0 )==0 :#line:1073
                OOOO00OOO0O0OOO0O =O0OO0O0OOOOOO0O00 -1 ;#line:1074
            else :#line:1075
                if _O00O00O000OO000O0 [-1 ]==0 :#line:1076
                    return #line:1077
                OOOO00OOO0O0OOO0O =_O00O00O000OO000O0 [-1 ]-1 #line:1078
                if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1079
                    print ("Olditem: "+str (_O00O00O000OO000O0 [-1 ])+", Newitem : "+str (OOOO00OOO0O0OOO0O ))#line:1080
            _OO0O0OO00OO0OO0O0 .append (OOOO00OOO0O0OOO0O )#line:1081
        elif _O00O0OOOOO000000O =="one":#line:1082
            if len (_O00O00O000OO000O0 )==0 :#line:1083
                O000OOOO0OOO0O0OO =OO00O00O0O00OOO00 .data ["varname"].index (O0OO00OOO0OOO0OO0 ['defi'].get ('attributes')[_O000000O0O0O0OOOO [-1 ]].get ('name'))#line:1084
                try :#line:1085
                    OOOO00OOO0O0OOO0O =OO00O00O0O00OOO00 .data ["catnames"][O000OOOO0OOO0O0OO ].index (O0OO00OOO0OOO0OO0 ['defi'].get ('attributes')[_O000000O0O0O0OOOO [-1 ]].get ('value'))#line:1086
                except :#line:1087
                    print (f"ERROR: attribute '{O0OO00OOO0OOO0OO0['defi'].get('attributes')[_O000000O0O0O0OOOO[-1]].get('name')}' has not value '{O0OO00OOO0OOO0OO0['defi'].get('attributes')[_O000000O0O0O0OOOO[-1]].get('value')}'")#line:1088
                    exit (1 )#line:1089
                _OO0O0OO00OO0OO0O0 .append (OOOO00OOO0O0OOO0O )#line:1090
                _O00O0O000OO00O00O =1 #line:1091
                _OO00O00OO0O00000O =1 #line:1092
            else :#line:1093
                print ("DEBUG: one category should not have more categories")#line:1094
                return #line:1095
        elif _O00O0OOOOO000000O =="list":#line:1097
            if _O00O000OO0000O00O is None :#line:1098
                O000OOOO0OOO0O0OO =OO00O00O0O00OOO00 .data ["varname"].index (O0OO00OOO0OOO0OO0 ['defi'].get ('attributes')[_O000000O0O0O0OOOO [-1 ]].get ('name'))#line:1099
                O0O0O0OO00O0O0O00 =None #line:1100
                _OOOOO0OO0O0OOO000 =[]#line:1101
                try :#line:1102
                    O00O0O00O000O0O00 =O0OO00OOO0OOO0OO0 ['defi'].get ('attributes')[_O000000O0O0O0OOOO [-1 ]].get ('value')#line:1103
                    for OOO00O0O000OOO000 in O00O0O00O000O0O00 :#line:1104
                        O0O0O0OO00O0O0O00 =OOO00O0O000OOO000 #line:1105
                        OOOO00OOO0O0OOO0O =OO00O00O0O00OOO00 .data ["catnames"][O000OOOO0OOO0O0OO ].index (OOO00O0O000OOO000 )#line:1106
                        _OOOOO0OO0O0OOO000 .append (OOOO00OOO0O0OOO0O )#line:1107
                except :#line:1108
                    print (f"ERROR: attribute '{O0OO00OOO0OOO0OO0['defi'].get('attributes')[_O000000O0O0O0OOOO[-1]].get('name')}' has not value '{OOO00O0O000OOO000}'")#line:1110
                    exit (1 )#line:1111
                _O00O000OO0000O00O =_OOOOO0OO0O0OOO000 #line:1112
                _O00O0O000OO00O00O =len (_O00O000OO0000O00O )#line:1113
                _OO00O00OO0O00000O =len (_O00O000OO0000O00O )#line:1114
            _OO0O0OO00OO0OO0O0 .append (_O00O000OO0000O00O [len (_O00O00O000OO000O0 )])#line:1115
        else :#line:1117
            print ("Attribute type "+_O00O0OOOOO000000O +" not supported.")#line:1118
            return #line:1119
        if len (_OO0O0OO00OO0OO0O0 )>0 :#line:1121
            _OO000OOO0O0O00OOO =(_O00O00OOO0O0OOO00 -_O000O00O000O00O0O )/len (_OO0O0OO00OO0OO0O0 )#line:1122
        else :#line:1123
            _OO000OOO0O0O00OOO =0 #line:1124
        _O00O000O0000000OO =0 #line:1126
        for OO0OO0OOO00000OO0 in _OO0O0OO00OO0OO0O0 :#line:1128
                _O00O00O000OO000O0 .append (OO0OO0OOO00000OO0 )#line:1129
                _O000O00000O0O0O00 .pop ()#line:1130
                _O000O00000O0O0O00 .append (_O00O00O000OO000O0 )#line:1131
                _O00OO00OO0O00OOOO =_OO00OOO0OOO000O0O |OO00O00O0O00OOO00 .data ["dm"][OO00O00O0O00OOO00 .data ["varname"].index (O0OO00OOO0OOO0OO0 ['defi'].get ('attributes')[_O000000O0O0O0OOOO [-1 ]].get ('name'))][OO0OO0OOO00000OO0 ]#line:1132
                _OOOOOOOOOO00O00OO =1 #line:1133
                if (len (_O000000O0O0O0OOOO )<_OO0O0O00000O00000 ):#line:1134
                    _OOOOOOOOOO00O00OO =-1 #line:1135
                    if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1136
                        print ("DEBUG: will not verify, low cedent length")#line:1137
                if (len (_O000O00000O0O0O00 [-1 ])<_O00O0O000OO00O00O ):#line:1138
                    _OOOOOOOOOO00O00OO =0 #line:1139
                    if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1140
                        print ("DEBUG: will not verify, low attribute length")#line:1141
                _OOOOOOO00000OO0O0 =0 #line:1142
                if O0OO00OOO0OOO0OO0 ['defi'].get ('type')=='con':#line:1143
                    _OOOOOOO00000OO0O0 =_O00OOOO000O0OO00O &_O00OO00OO0O00OOOO #line:1144
                else :#line:1145
                    _OOOOOOO00000OO0O0 =_O00OOOO000O0OO00O |_O00OO00OO0O00OOOO #line:1146
                O0OO00OOO0OOO0OO0 ['trace_cedent']=_O000000O0O0O0OOOO #line:1147
                O0OO00OOO0OOO0OO0 ['traces']=_O000O00000O0O0O00 #line:1148
                OOO0O0O0O0OO000OO ,O0OO00O0O0OO0O00O ,OO0O00OOOO0OO0OOO =OO00O00O0O00OOO00 ._print (O0OO00OOO0OOO0OO0 ,_O000000O0O0O0OOOO ,_O000O00000O0O0O00 )#line:1149
                O0OO00OOO0OOO0OO0 ['generated_string']=OOO0O0O0O0OO000OO #line:1150
                O0OO00OOO0OOO0OO0 ['rule']=O0OO00O0O0OO0O00O #line:1151
                O0OO00OOO0OOO0OO0 ['filter_value']=_OOOOOOO00000OO0O0 #line:1152
                O0OO00OOO0OOO0OO0 ['traces']=copy .deepcopy (_O000O00000O0O0O00 )#line:1153
                O0OO00OOO0OOO0OO0 ['trace_cedent']=copy .deepcopy (_O000000O0O0O0OOOO )#line:1154
                O0OO00OOO0OOO0OO0 ['trace_cedent_asindata']=copy .deepcopy (OO0O00OOOO0OO0OOO )#line:1155
                if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1156
                    print (f"TC :{O0OO00OOO0OOO0OO0['trace_cedent_asindata']}")#line:1157
                OOOO00OO00OO00OOO ['cedents'].append (O0OO00OOO0OOO0OO0 )#line:1158
                OOO0OO000O0O0000O =OO00O00O0O00OOO00 ._verify_opt (OOOO00OO00OO00OOO ,O0OO00OOO0OOO0OO0 )#line:1159
                if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1160
                    print (f"DEBUG: {O0OO00OOO0OOO0OO0['generated_string']}.")#line:1161
                    print (f"DEBUG: {_O000000O0O0O0OOOO},{_OO0O0O00000O00000}.")#line:1162
                    if OOO0OO000O0O0000O :#line:1163
                        print ("DEBUG: Optimization: cutting")#line:1164
                if not (OOO0OO000O0O0000O ):#line:1165
                    if _OOOOOOOOOO00O00OO ==1 :#line:1166
                        if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1167
                            print ("DEBUG: verifying")#line:1168
                        if len (OOOO00OO00OO00OOO ['cedents_to_do'])==len (OOOO00OO00OO00OOO ['cedents']):#line:1169
                            if OO00O00O0O00OOO00 .proc =='CFMiner':#line:1170
                                O0O00OOOOOOOO0O00 ,OO00O0000O0OO00OO =OO00O00O0O00OOO00 ._verifyCF (_OOOOOOO00000OO0O0 )#line:1171
                            elif OO00O00O0O00OOO00 .proc =='UICMiner':#line:1172
                                O0O00OOOOOOOO0O00 ,OO00O0000O0OO00OO =OO00O00O0O00OOO00 ._verifyUIC (_OOOOOOO00000OO0O0 )#line:1173
                            elif OO00O00O0O00OOO00 .proc =='4ftMiner':#line:1174
                                O0O00OOOOOOOO0O00 ,OO00O0000O0OO00OO =OO00O00O0O00OOO00 ._verify4ft (_O00OO00OO0O00OOOO ,_O000000O0O0O0OOOO ,_O000O00000O0O0O00 )#line:1175
                            elif OO00O00O0O00OOO00 .proc =='SD4ftMiner':#line:1176
                                O0O00OOOOOOOO0O00 ,OO00O0000O0OO00OO =OO00O00O0O00OOO00 ._verifysd4ft (_O00OO00OO0O00OOOO )#line:1177
                            else :#line:1178
                                print ("Unsupported procedure : "+OO00O00O0O00OOO00 .proc )#line:1179
                                exit (0 )#line:1180
                            if O0O00OOOOOOOO0O00 ==True :#line:1181
                                OO00OOOO0OOO00O0O ={}#line:1182
                                OO00OOOO0OOO00O0O ["rule_id"]=OO00O00O0O00OOO00 .stats ['total_valid']#line:1183
                                OO00OOOO0OOO00O0O ["cedents_str"]={}#line:1184
                                OO00OOOO0OOO00O0O ["cedents_struct"]={}#line:1185
                                OO00OOOO0OOO00O0O ['traces']={}#line:1186
                                OO00OOOO0OOO00O0O ['trace_cedent_taskorder']={}#line:1187
                                OO00OOOO0OOO00O0O ['trace_cedent_dataorder']={}#line:1188
                                for O00O00O000OO00O0O in OOOO00OO00OO00OOO ['cedents']:#line:1189
                                    if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1190
                                        print (O00O00O000OO00O0O )#line:1191
                                    OO00OOOO0OOO00O0O ['cedents_str'][O00O00O000OO00O0O ['cedent_type']]=O00O00O000OO00O0O ['generated_string']#line:1192
                                    OO00OOOO0OOO00O0O ['cedents_struct'][O00O00O000OO00O0O ['cedent_type']]=O00O00O000OO00O0O ['rule']#line:1193
                                    OO00OOOO0OOO00O0O ['traces'][O00O00O000OO00O0O ['cedent_type']]=O00O00O000OO00O0O ['traces']#line:1194
                                    OO00OOOO0OOO00O0O ['trace_cedent_taskorder'][O00O00O000OO00O0O ['cedent_type']]=O00O00O000OO00O0O ['trace_cedent']#line:1195
                                    OO00OOOO0OOO00O0O ['trace_cedent_dataorder'][O00O00O000OO00O0O ['cedent_type']]=O00O00O000OO00O0O ['trace_cedent_asindata']#line:1196
                                OO00OOOO0OOO00O0O ["params"]=OO00O0000O0OO00OO #line:1197
                                if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1198
                                    OO00OOOO0OOO00O0O ["trace_cedent"]=copy .deepcopy (_O000000O0O0O0OOOO )#line:1199
                                OO00O00O0O00OOO00 ._print_rule (OO00OOOO0OOO00O0O )#line:1200
                                OO00O00O0O00OOO00 .rulelist .append (OO00OOOO0OOO00O0O )#line:1201
                            OO00O00O0O00OOO00 .stats ['total_cnt']+=1 #line:1202
                            OO00O00O0O00OOO00 .stats ['total_ver']+=1 #line:1203
                    if _OOOOOOOOOO00O00OO >=1 :#line:1204
                        if len (OOOO00OO00OO00OOO ['cedents_to_do'])>len (OOOO00OO00OO00OOO ['cedents']):#line:1205
                            OO00O00O0O00OOO00 ._start_cedent (OOOO00OO00OO00OOO ,_O000O00O000O00O0O +_O00O000O0000000OO *_OO000OOO0O0O00OOO ,_O000O00O000O00O0O +(_O00O000O0000000OO +0.33 )*_OO000OOO0O0O00OOO )#line:1206
                    OOOO00OO00OO00OOO ['cedents'].pop ()#line:1207
                    if (not (_OOOOOOOOOO00O00OO ==0 ))and (len (_O000000O0O0O0OOOO )<_O0O0O00OOO000O0OO ):#line:1208
                        OO00O00O0O00OOO00 ._genvar (OOOO00OO00OO00OOO ,O0OO00OOO0OOO0OO0 ,_O000000O0O0O0OOOO ,_O000O00000O0O0O00 ,_OOOOOOO00000OO0O0 ,_OO0O0O00000O00000 ,_O0O0O00OOO000O0OO ,_O000O00O000O00O0O +(_O00O000O0000000OO +0.33 )*_OO000OOO0O0O00OOO ,_O000O00O000O00O0O +(_O00O000O0000000OO +0.66 )*_OO000OOO0O0O00OOO )#line:1209
                else :#line:1210
                    OOOO00OO00OO00OOO ['cedents'].pop ()#line:1211
                if len (_O00O00O000OO000O0 )<_OO00O00OO0O00000O :#line:1212
                    OO00O00O0O00OOO00 ._gencomb (OOOO00OO00OO00OOO ,O0OO00OOO0OOO0OO0 ,_O000000O0O0O0OOOO ,_O000O00000O0O0O00 ,_O00O00O000OO000O0 ,_O00OOOO000O0OO00O ,_O00OO00OO0O00OOOO ,O0OO0O0OOOOOO0O00 ,_O00O0OOOOO000000O ,_OO0O0O00000O00000 ,_O0O0O00OOO000O0OO ,_O00O0O000OO00O00O ,_OO00O00OO0O00000O ,_O000O00O000O00O0O +_OO000OOO0O0O00OOO *(_O00O000O0000000OO +0.66 ),_O000O00O000O00O0O +_OO000OOO0O0O00OOO *(_O00O000O0000000OO +1 ),_O00O000OO0000O00O )#line:1213
                _O00O00O000OO000O0 .pop ()#line:1214
                _O00O000O0000000OO +=1 #line:1215
                if OO00O00O0O00OOO00 .options ['progressbar']:#line:1216
                    OO00O00O0O00OOO00 .bar .update (min (100 ,_O000O00O000O00O0O +_OO000OOO0O0O00OOO *_O00O000O0000000OO ))#line:1217
                if OO00O00O0O00OOO00 .verbosity ['debug']:#line:1218
                    print (f"Progress : lower: {_O000O00O000O00O0O}, step: {_OO000OOO0O0O00OOO}, step_no: {_O00O000O0000000OO} overall: {_O000O00O000O00O0O+_OO000OOO0O0O00OOO*_O00O000O0000000OO}")#line:1219
    def _start_cedent (OO0OO00OO0O000000 ,OOOO0O0O0OOO00O0O ,_OOOOOO00OO0OO0O00 ,_OOO00O000OO000OO0 ):#line:1221
        if len (OOOO0O0O0OOO00O0O ['cedents_to_do'])>len (OOOO0O0O0OOO00O0O ['cedents']):#line:1222
            _OOOOOO0O000O0O000 =[]#line:1223
            _O0O000O00O00OO0OO =[]#line:1224
            O00O0O0OOO0OO0O0O ={}#line:1225
            O00O0O0OOO0OO0O0O ['cedent_type']=OOOO0O0O0OOO00O0O ['cedents_to_do'][len (OOOO0O0O0OOO00O0O ['cedents'])]#line:1226
            O00OO000O0O0O0O0O =O00O0O0OOO0OO0O0O ['cedent_type']#line:1227
            if ((O00OO000O0O0O0O0O [-1 ]=='-')|(O00OO000O0O0O0O0O [-1 ]=='+')):#line:1228
                O00OO000O0O0O0O0O =O00OO000O0O0O0O0O [:-1 ]#line:1229
            O00O0O0OOO0OO0O0O ['defi']=OO0OO00OO0O000000 .kwargs .get (O00OO000O0O0O0O0O )#line:1231
            if (O00O0O0OOO0OO0O0O ['defi']==None ):#line:1232
                print ("Error getting cedent ",O00O0O0OOO0OO0O0O ['cedent_type'])#line:1233
            _OOOO0OO000000O00O =int (0 )#line:1234
            O00O0O0OOO0OO0O0O ['num_cedent']=len (O00O0O0OOO0OO0O0O ['defi'].get ('attributes'))#line:1235
            if (O00O0O0OOO0OO0O0O ['defi'].get ('type')=='con'):#line:1236
                _OOOO0OO000000O00O =(1 <<OO0OO00OO0O000000 .data ["rows_count"])-1 #line:1237
            OO0OO00OO0O000000 ._genvar (OOOO0O0O0OOO00O0O ,O00O0O0OOO0OO0O0O ,_OOOOOO0O000O0O000 ,_O0O000O00O00OO0OO ,_OOOO0OO000000O00O ,O00O0O0OOO0OO0O0O ['defi'].get ('minlen'),O00O0O0OOO0OO0O0O ['defi'].get ('maxlen'),_OOOOOO00OO0OO0O00 ,_OOO00O000OO000OO0 )#line:1238
    def _calc_all (O00O00O00OOOOOOO0 ,**OOOO0OOOOOOOO000O ):#line:1241
        if "df"in OOOO0OOOOOOOO000O :#line:1242
            O00O00O00OOOOOOO0 ._prep_data (O00O00O00OOOOOOO0 .kwargs .get ("df"))#line:1243
        if not (O00O00O00OOOOOOO0 ._initialized ):#line:1244
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1245
        else :#line:1246
            O00O00O00OOOOOOO0 ._calculate (**OOOO0OOOOOOOO000O )#line:1247
    def _check_cedents (O0O000O00OO00000O ,O0000OOOO000000O0 ,**OOOO0000O0OOO0000 ):#line:1249
        O0OOOO00O00O000O0 =True #line:1250
        if (OOOO0000O0OOO0000 .get ('quantifiers',None )==None ):#line:1251
            print (f"Error: missing quantifiers.")#line:1252
            O0OOOO00O00O000O0 =False #line:1253
            return O0OOOO00O00O000O0 #line:1254
        if (type (OOOO0000O0OOO0000 .get ('quantifiers'))!=dict ):#line:1255
            print (f"Error: quantifiers are not dictionary type.")#line:1256
            O0OOOO00O00O000O0 =False #line:1257
            return O0OOOO00O00O000O0 #line:1258
        for O000O0O0OO00OO0O0 in O0000OOOO000000O0 :#line:1260
            if (OOOO0000O0OOO0000 .get (O000O0O0OO00OO0O0 ,None )==None ):#line:1261
                print (f"Error: cedent {O000O0O0OO00OO0O0} is missing in parameters.")#line:1262
                O0OOOO00O00O000O0 =False #line:1263
                return O0OOOO00O00O000O0 #line:1264
            O000O0OOO00O0O00O =OOOO0000O0OOO0000 .get (O000O0O0OO00OO0O0 )#line:1265
            if (O000O0OOO00O0O00O .get ('minlen'),None )==None :#line:1266
                print (f"Error: cedent {O000O0O0OO00OO0O0} has no minimal length specified.")#line:1267
                O0OOOO00O00O000O0 =False #line:1268
                return O0OOOO00O00O000O0 #line:1269
            if not (type (O000O0OOO00O0O00O .get ('minlen'))is int ):#line:1270
                print (f"Error: cedent {O000O0O0OO00OO0O0} has invalid type of minimal length ({type(O000O0OOO00O0O00O.get('minlen'))}).")#line:1271
                O0OOOO00O00O000O0 =False #line:1272
                return O0OOOO00O00O000O0 #line:1273
            if (O000O0OOO00O0O00O .get ('maxlen'),None )==None :#line:1274
                print (f"Error: cedent {O000O0O0OO00OO0O0} has no maximal length specified.")#line:1275
                O0OOOO00O00O000O0 =False #line:1276
                return O0OOOO00O00O000O0 #line:1277
            if not (type (O000O0OOO00O0O00O .get ('maxlen'))is int ):#line:1278
                print (f"Error: cedent {O000O0O0OO00OO0O0} has invalid type of maximal length.")#line:1279
                O0OOOO00O00O000O0 =False #line:1280
                return O0OOOO00O00O000O0 #line:1281
            if (O000O0OOO00O0O00O .get ('type'),None )==None :#line:1282
                print (f"Error: cedent {O000O0O0OO00OO0O0} has no type specified.")#line:1283
                O0OOOO00O00O000O0 =False #line:1284
                return O0OOOO00O00O000O0 #line:1285
            if not ((O000O0OOO00O0O00O .get ('type'))in (['con','dis'])):#line:1286
                print (f"Error: cedent {O000O0O0OO00OO0O0} has invalid type. Allowed values are 'con' and 'dis'.")#line:1287
                O0OOOO00O00O000O0 =False #line:1288
                return O0OOOO00O00O000O0 #line:1289
            if (O000O0OOO00O0O00O .get ('attributes'),None )==None :#line:1290
                print (f"Error: cedent {O000O0O0OO00OO0O0} has no attributes specified.")#line:1291
                O0OOOO00O00O000O0 =False #line:1292
                return O0OOOO00O00O000O0 #line:1293
            for O0OOOOOO00OO0O0O0 in O000O0OOO00O0O00O .get ('attributes'):#line:1294
                if (O0OOOOOO00OO0O0O0 .get ('name'),None )==None :#line:1295
                    print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0} has no 'name' attribute specified.")#line:1296
                    O0OOOO00O00O000O0 =False #line:1297
                    return O0OOOO00O00O000O0 #line:1298
                if not ((O0OOOOOO00OO0O0O0 .get ('name'))in O0O000O00OO00000O .data ["varname"]):#line:1299
                    print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} not in variable list. Please check spelling.")#line:1300
                    O0OOOO00O00O000O0 =False #line:1301
                    return O0OOOO00O00O000O0 #line:1302
                if (O0OOOOOO00OO0O0O0 .get ('type'),None )==None :#line:1303
                    print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} has no 'type' attribute specified.")#line:1304
                    O0OOOO00O00O000O0 =False #line:1305
                    return O0OOOO00O00O000O0 #line:1306
                if not ((O0OOOOOO00OO0O0O0 .get ('type'))in (['rcut','lcut','seq','subset','one','list'])):#line:1307
                    print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} has unsupported type {O0OOOOOO00OO0O0O0.get('type')}. Supported types are 'subset','seq','lcut','rcut','one','list'.")#line:1308
                    O0OOOO00O00O000O0 =False #line:1309
                    return O0OOOO00O00O000O0 #line:1310
                if (O0OOOOOO00OO0O0O0 .get ('minlen'),None )==None :#line:1311
                    print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} has no minimal length specified.")#line:1312
                    O0OOOO00O00O000O0 =False #line:1313
                    return O0OOOO00O00O000O0 #line:1314
                if not (type (O0OOOOOO00OO0O0O0 .get ('minlen'))is int ):#line:1315
                    if not (O0OOOOOO00OO0O0O0 .get ('type')=='one'or O0OOOOOO00OO0O0O0 .get ('type')=='list'):#line:1316
                        print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} has invalid type of minimal length.")#line:1317
                        O0OOOO00O00O000O0 =False #line:1318
                        return O0OOOO00O00O000O0 #line:1319
                if (O0OOOOOO00OO0O0O0 .get ('maxlen'),None )==None :#line:1320
                    print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} has no maximal length specified.")#line:1321
                    O0OOOO00O00O000O0 =False #line:1322
                    return O0OOOO00O00O000O0 #line:1323
                if not (type (O0OOOOOO00OO0O0O0 .get ('maxlen'))is int ):#line:1324
                    if not (O0OOOOOO00OO0O0O0 .get ('type')=='one'or O0OOOOOO00OO0O0O0 .get ('type')=='list'):#line:1325
                        print (f"Error: cedent {O000O0O0OO00OO0O0} / attribute {O0OOOOOO00OO0O0O0.get('name')} has invalid type of maximal length.")#line:1326
                        O0OOOO00O00O000O0 =False #line:1327
                        return O0OOOO00O00O000O0 #line:1328
        return O0OOOO00O00O000O0 #line:1329

    def _calculate (OO000OOOOOOO00000 ,**O0O0OO000OOO0000O ):#line:3
        if OO000OOOOOOO00000 .data ["data_prepared"]==0 :#line:4
            print ("Error: data not prepared")#line:5
            return #line:6
        OO000OOOOOOO00000 .kwargs =O0O0OO000OOO0000O #line:7
        OO000OOOOOOO00000 .proc =O0O0OO000OOO0000O .get ('proc')#line:8
        OO000OOOOOOO00000 .quantifiers =O0O0OO000OOO0000O .get ('quantifiers')#line:9
        OO000OOOOOOO00000 ._init_task ()#line:11
        OO000OOOOOOO00000 .stats ['start_proc_time']=time .time ()#line:12
        OO000OOOOOOO00000 .task_actinfo ['cedents_to_do']=[]#line:13
        OO000OOOOOOO00000 .task_actinfo ['cedents']=[]#line:14
        if O0O0OO000OOO0000O .get ("proc")=='UICMiner':#line:17
            if not (OO000OOOOOOO00000 ._check_cedents (['ante'],**O0O0OO000OOO0000O )):#line:18
                return #line:19
            _OOO0O0000OOOO0OOO =O0O0OO000OOO0000O .get ("cond")#line:21
            if _OOO0O0000OOOO0OOO !=None :#line:22
                OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:23
            else :#line:24
                O00OO000O0000OOO0 =OO000OOOOOOO00000 .cedent #line:25
                O00OO000O0000OOO0 ['cedent_type']='cond'#line:26
                O00OO000O0000OOO0 ['filter_value']=(1 <<OO000OOOOOOO00000 .data ["rows_count"])-1 #line:27
                O00OO000O0000OOO0 ['generated_string']='---'#line:28
                if OO000OOOOOOO00000 .verbosity ['debug']:#line:29
                    print (O00OO000O0000OOO0 ['filter_value'])#line:30
                OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:31
                OO000OOOOOOO00000 .task_actinfo ['cedents'].append (O00OO000O0000OOO0 )#line:32
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:33
            if O0O0OO000OOO0000O .get ('target',None )==None :#line:34
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:35
                return #line:36
            if not (O0O0OO000OOO0000O .get ('target')in OO000OOOOOOO00000 .data ["varname"]):#line:37
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:38
                return #line:39
            if ("aad_score"in OO000OOOOOOO00000 .quantifiers ):#line:40
                if not ("aad_weights"in OO000OOOOOOO00000 .quantifiers ):#line:41
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:42
                    return #line:43
                if not (len (OO000OOOOOOO00000 .quantifiers .get ("aad_weights"))==len (OO000OOOOOOO00000 .data ["dm"][OO000OOOOOOO00000 .data ["varname"].index (OO000OOOOOOO00000 .kwargs .get ('target'))])):#line:44
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:45
                    return #line:46
        elif O0O0OO000OOO0000O .get ("proc")=='CFMiner':#line:47
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do']=['cond']#line:48
            if O0O0OO000OOO0000O .get ('target',None )==None :#line:49
                print ("ERROR: no target variable defined for CF Miner")#line:50
                return #line:51
            OO0000000O0O00000 =O0O0OO000OOO0000O .get ('target',None )#line:52
            OO000OOOOOOO00000 .profiles ['hist_target_entire_dataset_labels']=OO000OOOOOOO00000 .data ["catnames"][OO000OOOOOOO00000 .data ["varname"].index (OO000OOOOOOO00000 .kwargs .get ('target'))]#line:53
            OO0O0OO0O0O000OO0 =OO000OOOOOOO00000 .data ["dm"][OO000OOOOOOO00000 .data ["varname"].index (OO000OOOOOOO00000 .kwargs .get ('target'))]#line:54
            O0OOO0O0OOOO0O0O0 =[]#line:56
            for O00O0OO00OOO0O00O in range (len (OO0O0OO0O0O000OO0 )):#line:57
                O0O00OO00O00O0OO0 =OO000OOOOOOO00000 ._bitcount (OO0O0OO0O0O000OO0 [O00O0OO00OOO0O00O ])#line:58
                O0OOO0O0OOOO0O0O0 .append (O0O00OO00O00O0OO0 )#line:59
            OO000OOOOOOO00000 .profiles ['hist_target_entire_dataset_values']=O0OOO0O0OOOO0O0O0 #line:60
            if not (OO000OOOOOOO00000 ._check_cedents (['cond'],**O0O0OO000OOO0000O )):#line:61
                return #line:62
            if not (O0O0OO000OOO0000O .get ('target')in OO000OOOOOOO00000 .data ["varname"]):#line:63
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:64
                return #line:65
            if ("aad"in OO000OOOOOOO00000 .quantifiers ):#line:66
                if not ("aad_weights"in OO000OOOOOOO00000 .quantifiers ):#line:67
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:68
                    return #line:69
                if not (len (OO000OOOOOOO00000 .quantifiers .get ("aad_weights"))==len (OO000OOOOOOO00000 .data ["dm"][OO000OOOOOOO00000 .data ["varname"].index (OO000OOOOOOO00000 .kwargs .get ('target'))])):#line:70
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:71
                    return #line:72
        elif O0O0OO000OOO0000O .get ("proc")=='4ftMiner':#line:75
            if not (OO000OOOOOOO00000 ._check_cedents (['ante','succ'],**O0O0OO000OOO0000O )):#line:76
                return #line:77
            _OOO0O0000OOOO0OOO =O0O0OO000OOO0000O .get ("cond")#line:79
            if _OOO0O0000OOOO0OOO !=None :#line:80
                OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:81
            else :#line:82
                O00OO000O0000OOO0 =OO000OOOOOOO00000 .cedent #line:83
                O00OO000O0000OOO0 ['cedent_type']='cond'#line:84
                O00OO000O0000OOO0 ['filter_value']=(1 <<OO000OOOOOOO00000 .data ["rows_count"])-1 #line:85
                O00OO000O0000OOO0 ['generated_string']='---'#line:86
                OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:87
                OO000OOOOOOO00000 .task_actinfo ['cedents'].append (O00OO000O0000OOO0 )#line:88
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:89
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('succ')#line:90
        elif O0O0OO000OOO0000O .get ("proc")=='SD4ftMiner':#line:91
            if not (OO000OOOOOOO00000 ._check_cedents (['ante','succ','frst','scnd'],**O0O0OO000OOO0000O )):#line:94
                return #line:95
            _OOO0O0000OOOO0OOO =O0O0OO000OOO0000O .get ("cond")#line:96
            if _OOO0O0000OOOO0OOO !=None :#line:97
                OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:98
            else :#line:99
                O00OO000O0000OOO0 =OO000OOOOOOO00000 .cedent #line:100
                O00OO000O0000OOO0 ['cedent_type']='cond'#line:101
                O00OO000O0000OOO0 ['filter_value']=(1 <<OO000OOOOOOO00000 .data ["rows_count"])-1 #line:102
                O00OO000O0000OOO0 ['generated_string']='---'#line:103
                OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('cond')#line:104
                OO000OOOOOOO00000 .task_actinfo ['cedents'].append (O00OO000O0000OOO0 )#line:105
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('frst')#line:106
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:107
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('ante')#line:108
            OO000OOOOOOO00000 .task_actinfo ['cedents_to_do'].append ('succ')#line:109
        else :#line:110
            print ("Unsupported procedure")#line:111
            return #line:112
        print ("Will go for ",O0O0OO000OOO0000O .get ("proc"))#line:113
        OO000OOOOOOO00000 .task_actinfo ['optim']={}#line:116
        OOOOOOO00OO0O00OO =True #line:117
        for OO0000O000OO00O00 in OO000OOOOOOO00000 .task_actinfo ['cedents_to_do']:#line:118
            try :#line:119
                OO0O0O0O000OO0O0O =OO000OOOOOOO00000 .kwargs .get (OO0000O000OO00O00 )#line:120
                if OO000OOOOOOO00000 .verbosity ['debug']:#line:121
                    print (OO0O0O0O000OO0O0O )#line:122
                    print (f"...cedent {OO0000O000OO00O00} is type {OO0O0O0O000OO0O0O.get('type')}")#line:123
                    print (f"Will check cedent type {OO0000O000OO00O00} : {OO0O0O0O000OO0O0O.get('type')}")#line:124
                if OO0O0O0O000OO0O0O .get ('type')!='con':#line:125
                    OOOOOOO00OO0O00OO =False #line:126
                    if OO000OOOOOOO00000 .verbosity ['debug']:#line:127
                        print (f"Cannot optim due to cedent type {OO0000O000OO00O00} : {OO0O0O0O000OO0O0O.get('type')}")#line:128
            except :#line:129
                O0O00000O0O0OOO0O =1 <2 #line:130
        if OO000OOOOOOO00000 .options ['optimizations']==False :#line:132
            OOOOOOO00OO0O00OO =False #line:133
        O0OOO0O0OOOO00OOO ={}#line:134
        O0OOO0O0OOOO00OOO ['only_con']=OOOOOOO00OO0O00OO #line:135
        OO000OOOOOOO00000 .task_actinfo ['optim']=O0OOO0O0OOOO00OOO #line:136
        if OO000OOOOOOO00000 .verbosity ['debug']:#line:140
            print ("Starting to prepare data.")#line:141
            OO000OOOOOOO00000 ._prep_data (OO000OOOOOOO00000 .data .df )#line:142
            OO000OOOOOOO00000 .stats ['mid1_time']=time .time ()#line:143
            OO000OOOOOOO00000 .quantifiers =O0O0OO000OOO0000O .get ('self.quantifiers')#line:144
        print ("Starting to mine rules.")#line:145
        sys .stdout .flush ()#line:146
        time .sleep (0.01 )#line:147
        if OO000OOOOOOO00000 .options ['progressbar']:#line:148
            O0OOOOOO0O0OOO0OO =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:149
            OO000OOOOOOO00000 .bar =progressbar .ProgressBar (widgets =O0OOOOOO0O0OOO0OO ,max_value =100 ,fd =sys .stdout ).start ()#line:150
            OO000OOOOOOO00000 .bar .update (0 )#line:151
        OO000OOOOOOO00000 .progress_lower =0 #line:152
        OO000OOOOOOO00000 .progress_upper =100 #line:153
        OO000OOOOOOO00000 ._start_cedent (OO000OOOOOOO00000 .task_actinfo ,OO000OOOOOOO00000 .progress_lower ,OO000OOOOOOO00000 .progress_upper )#line:154
        if OO000OOOOOOO00000 .options ['progressbar']:#line:155
            OO000OOOOOOO00000 .bar .update (100 )#line:156
            OO000OOOOOOO00000 .bar .finish ()#line:157
        OO000OOOOOOO00000 .stats ['end_proc_time']=time .time ()#line:158
        print ("Done. Total verifications : "+str (OO000OOOOOOO00000 .stats ['total_cnt'])+", rules "+str (OO000OOOOOOO00000 .stats ['total_valid'])+", times: prep "+"{:.2f}".format (OO000OOOOOOO00000 .stats ['end_prep_time']-OO000OOOOOOO00000 .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (OO000OOOOOOO00000 .stats ['end_proc_time']-OO000OOOOOOO00000 .stats ['start_proc_time'])+"sec")#line:161
        O0O00OO0O0O0O00OO ={}#line:162
        OO0OO00O0O0O0OOOO ={}#line:163
        OO0OO00O0O0O0OOOO ["guid"]=OO000OOOOOOO00000 .guid #line:164
        OO0OO00O0O0O0OOOO ["task_type"]=O0O0OO000OOO0000O .get ('proc')#line:165
        OO0OO00O0O0O0OOOO ["target"]=O0O0OO000OOO0000O .get ('target')#line:166
        OO0OO00O0O0O0OOOO ["self.quantifiers"]=OO000OOOOOOO00000 .quantifiers #line:167
        if O0O0OO000OOO0000O .get ('cond')!=None :#line:168
            OO0OO00O0O0O0OOOO ['cond']=O0O0OO000OOO0000O .get ('cond')#line:169
        if O0O0OO000OOO0000O .get ('ante')!=None :#line:170
            OO0OO00O0O0O0OOOO ['ante']=O0O0OO000OOO0000O .get ('ante')#line:171
        if O0O0OO000OOO0000O .get ('succ')!=None :#line:172
            OO0OO00O0O0O0OOOO ['succ']=O0O0OO000OOO0000O .get ('succ')#line:173
        if O0O0OO000OOO0000O .get ('opts')!=None :#line:174
            OO0OO00O0O0O0OOOO ['opts']=O0O0OO000OOO0000O .get ('opts')#line:175
        if OO000OOOOOOO00000 .df is None :#line:176
            OO0OO00O0O0O0OOOO ['rowcount']=OO000OOOOOOO00000 .data ["rows_count"]#line:177
        else :#line:179
            OO0OO00O0O0O0OOOO ['rowcount']=len (OO000OOOOOOO00000 .df .index )#line:180
        O0O00OO0O0O0O00OO ["taskinfo"]=OO0OO00O0O0O0OOOO #line:181
        OOOO0OOO0O0OOO000 ={}#line:182
        OOOO0OOO0O0OOO000 ["total_verifications"]=OO000OOOOOOO00000 .stats ['total_cnt']#line:183
        OOOO0OOO0O0OOO000 ["valid_rules"]=OO000OOOOOOO00000 .stats ['total_valid']#line:184
        OOOO0OOO0O0OOO000 ["total_verifications_with_opt"]=OO000OOOOOOO00000 .stats ['total_ver']#line:185
        OOOO0OOO0O0OOO000 ["time_prep"]=OO000OOOOOOO00000 .stats ['end_prep_time']-OO000OOOOOOO00000 .stats ['start_prep_time']#line:186
        OOOO0OOO0O0OOO000 ["time_processing"]=OO000OOOOOOO00000 .stats ['end_proc_time']-OO000OOOOOOO00000 .stats ['start_proc_time']#line:187
        OOOO0OOO0O0OOO000 ["time_total"]=OO000OOOOOOO00000 .stats ['end_prep_time']-OO000OOOOOOO00000 .stats ['start_prep_time']+OO000OOOOOOO00000 .stats ['end_proc_time']-OO000OOOOOOO00000 .stats ['start_proc_time']#line:188
        O0O00OO0O0O0O00OO ["summary_statistics"]=OOOO0OOO0O0OOO000 #line:189
        O0O00OO0O0O0O00OO ["rules"]=OO000OOOOOOO00000 .rulelist #line:190
        O000O00O0OOOOO00O ={}#line:191
        O000O00O0OOOOO00O ["varname"]=OO000OOOOOOO00000 .data ["varname"]#line:192
        O000O00O0OOOOO00O ["catnames"]=OO000OOOOOOO00000 .data ["catnames"]#line:193
        O0O00OO0O0O0O00OO ["datalabels"]=O000O00O0OOOOO00O #line:194
        OO000OOOOOOO00000 .result =O0O00OO0O0O0O00OO #line:195
    def print_summary (OOOOO0O0OO0OOOOO0 ):#line:197
        ""#line:200
        if not (OOOOO0O0OO0OOOOO0 ._is_calculated ()):#line:201
            print ("ERROR: Task has not been calculated.")#line:202
            return #line:203
        print ("")#line:204
        print ("CleverMiner task processing summary:")#line:205
        print ("")#line:206
        print (f"Task type : {OOOOO0O0OO0OOOOO0.result['taskinfo']['task_type']}")#line:207
        print (f"Number of verifications : {OOOOO0O0OO0OOOOO0.result['summary_statistics']['total_verifications']}")#line:208
        print (f"Number of rules : {OOOOO0O0OO0OOOOO0.result['summary_statistics']['valid_rules']}")#line:209
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(OOOOO0O0OO0OOOOO0.result['summary_statistics']['time_total']))}")#line:210
        if OOOOO0O0OO0OOOOO0 .verbosity ['debug']:#line:211
            print (f"Total time needed : {OOOOO0O0OO0OOOOO0.result['summary_statistics']['time_total']}")#line:212
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(OOOOO0O0OO0OOOOO0.result['summary_statistics']['time_prep']))}")#line:213
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(OOOOO0O0OO0OOOOO0.result['summary_statistics']['time_processing']))}")#line:214
        print ("")#line:215
    def print_hypolist (OOO00OO000OOOOOO0 ):#line:217
        ""#line:220
        OOO00OO000OOOOOO0 .print_rulelist ();#line:221
    def print_rulelist (O000O0O00O0O0000O ,sortby =None ,storesorted =False ):#line:223
        ""#line:228
        if not (O000O0O00O0O0000O ._is_calculated ()):#line:229
            print ("ERROR: Task has not been calculated.")#line:230
            return #line:231
        def O00O000OO000OO00O (OOO000O00O0OO000O ):#line:233
            OOO0O0OO0O0O0000O =OOO000O00O0OO000O ["params"]#line:234
            return OOO0O0OO0O0O0000O .get (sortby ,0 )#line:235
        print ("")#line:237
        print ("List of rules:")#line:238
        if O000O0O00O0O0000O .result ['taskinfo']['task_type']=="4ftMiner":#line:239
            print ("RULEID BASE  CONF  AAD    Rule")#line:240
        elif O000O0O00O0O0000O .result ['taskinfo']['task_type']=="UICMiner":#line:241
            print ("RULEID BASE  AAD_SCORE  Rule")#line:242
        elif O000O0O00O0O0000O .result ['taskinfo']['task_type']=="CFMiner":#line:243
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:244
        elif O000O0O00O0O0000O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:245
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:246
        else :#line:247
            print ("Unsupported task type for rulelist")#line:248
            return #line:249
        O000OO00O00O0OOOO =O000O0O00O0O0000O .result ["rules"]#line:250
        if sortby is not None :#line:251
            O000OO00O00O0OOOO =sorted (O000OO00O00O0OOOO ,key =O00O000OO000OO00O ,reverse =True )#line:252
            if storesorted :#line:253
                O000O0O00O0O0000O .result ["rules"]=O000OO00O00O0OOOO #line:254
        for OOO0OO00000OOO0OO in O000OO00O00O0OOOO :#line:256
            O0O0O0OOOOO0OO000 ="{:6d}".format (OOO0OO00000OOO0OO ["rule_id"])#line:257
            if O000O0O00O0O0000O .result ['taskinfo']['task_type']=="4ftMiner":#line:258
                if O000O0O00O0O0000O .verbosity ['debug']:#line:259
                   print (f"{OOO0OO00000OOO0OO['params']}")#line:260
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["base"])+" "+"{:.3f}".format (OOO0OO00000OOO0OO ["params"]["conf"])+" "+"{:+.3f}".format (OOO0OO00000OOO0OO ["params"]["aad"])#line:261
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +" "+OOO0OO00000OOO0OO ["cedents_str"]["ante"]+" => "+OOO0OO00000OOO0OO ["cedents_str"]["succ"]+" | "+OOO0OO00000OOO0OO ["cedents_str"]["cond"]#line:262
            elif O000O0O00O0O0000O .result ['taskinfo']['task_type']=="UICMiner":#line:263
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["base"])+" "+"{:.3f}".format (OOO0OO00000OOO0OO ["params"]["aad_score"])#line:264
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +"     "+OOO0OO00000OOO0OO ["cedents_str"]["ante"]+" => "+O000O0O00O0O0000O .result ['taskinfo']['target']+"(*) | "+OOO0OO00000OOO0OO ["cedents_str"]["cond"]#line:265
            elif O000O0O00O0O0000O .result ['taskinfo']['task_type']=="CFMiner":#line:266
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["base"])+" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["s_up"])+" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["s_down"])#line:267
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +" "+OOO0OO00000OOO0OO ["cedents_str"]["cond"]#line:268
            elif O000O0O00O0O0000O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:269
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["base1"])+" "+"{:5d}".format (OOO0OO00000OOO0OO ["params"]["base2"])+"    "+"{:.3f}".format (OOO0OO00000OOO0OO ["params"]["ratioconf"])+"    "+"{:+.3f}".format (OOO0OO00000OOO0OO ["params"]["deltaconf"])#line:270
                O0O0O0OOOOO0OO000 =O0O0O0OOOOO0OO000 +"  "+OOO0OO00000OOO0OO ["cedents_str"]["ante"]+" => "+OOO0OO00000OOO0OO ["cedents_str"]["succ"]+" | "+OOO0OO00000OOO0OO ["cedents_str"]["cond"]+" : "+OOO0OO00000OOO0OO ["cedents_str"]["frst"]+" x "+OOO0OO00000OOO0OO ["cedents_str"]["scnd"]#line:271
            print (O0O0O0OOOOO0OO000 )#line:273
        print ("")#line:274
    def print_hypo (O0OOO00OO000O00OO ,O000O0O00O000OOOO ):#line:276
        ""#line:280
        O0OOO00OO000O00OO .print_rule (O000O0O00O000OOOO )#line:281
    def print_rule (OO0O0O000OOOOOOOO ,OO0000O0000OO0000 ):#line:284
        ""#line:288
        if not (OO0O0O000OOOOOOOO ._is_calculated ()):#line:289
            print ("ERROR: Task has not been calculated.")#line:290
            return #line:291
        print ("")#line:292
        if (OO0000O0000OO0000 <=len (OO0O0O000OOOOOOOO .result ["rules"])):#line:293
            if OO0O0O000OOOOOOOO .result ['taskinfo']['task_type']=="4ftMiner":#line:294
                print ("")#line:295
                O0O0O00O000O00000 =OO0O0O000OOOOOOOO .result ["rules"][OO0000O0000OO0000 -1 ]#line:296
                print (f"Rule id : {O0O0O00O000O00000['rule_id']}")#line:297
                print ("")#line:298
                print (f"Base : {'{:5d}'.format(O0O0O00O000O00000['params']['base'])}  Relative base : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_base'])}  CONF : {'{:.3f}'.format(O0O0O00O000O00000['params']['conf'])}  AAD : {'{:+.3f}'.format(O0O0O00O000O00000['params']['aad'])}  BAD : {'{:+.3f}'.format(O0O0O00O000O00000['params']['bad'])}")#line:299
                print ("")#line:300
                print ("Cedents:")#line:301
                print (f"  antecedent : {O0O0O00O000O00000['cedents_str']['ante']}")#line:302
                print (f"  succcedent : {O0O0O00O000O00000['cedents_str']['succ']}")#line:303
                print (f"  condition  : {O0O0O00O000O00000['cedents_str']['cond']}")#line:304
                print ("")#line:305
                print ("Fourfold table")#line:306
                print (f"    |  S  |  ¬S |")#line:307
                print (f"----|-----|-----|")#line:308
                print (f" A  |{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold'][0])}|{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold'][1])}|")#line:309
                print (f"----|-----|-----|")#line:310
                print (f"¬A  |{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold'][2])}|{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold'][3])}|")#line:311
                print (f"----|-----|-----|")#line:312
            elif OO0O0O000OOOOOOOO .result ['taskinfo']['task_type']=="CFMiner":#line:313
                print ("")#line:314
                O0O0O00O000O00000 =OO0O0O000OOOOOOOO .result ["rules"][OO0000O0000OO0000 -1 ]#line:315
                print (f"Rule id : {O0O0O00O000O00000['rule_id']}")#line:316
                print ("")#line:317
                OOO0OOO0OO000000O =""#line:318
                if ('aad'in O0O0O00O000O00000 ['params']):#line:319
                    OOO0OOO0OO000000O ="aad : "+str (O0O0O00O000O00000 ['params']['aad'])#line:320
                print (f"Base : {'{:5d}'.format(O0O0O00O000O00000['params']['base'])}  Relative base : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(O0O0O00O000O00000['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(O0O0O00O000O00000['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(O0O0O00O000O00000['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(O0O0O00O000O00000['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(O0O0O00O000O00000['params']['max'])}  Histogram minimum : {'{:5d}'.format(O0O0O00O000O00000['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_min'])} {OOO0OOO0OO000000O}")#line:322
                print ("")#line:323
                print (f"Condition  : {O0O0O00O000O00000['cedents_str']['cond']}")#line:324
                print ("")#line:325
                OO00O00000O0O0O0O =OO0O0O000OOOOOOOO .get_category_names (OO0O0O000OOOOOOOO .result ["taskinfo"]["target"])#line:326
                print (f"Categories in target variable  {OO00O00000O0O0O0O}")#line:327
                print (f"Histogram                      {O0O0O00O000O00000['params']['hist']}")#line:328
                if ('aad'in O0O0O00O000O00000 ['params']):#line:329
                    print (f"Histogram on full set          {O0O0O00O000O00000['params']['hist_full']}")#line:330
                    print (f"Relative histogram             {O0O0O00O000O00000['params']['rel_hist']}")#line:331
                    print (f"Relative histogram on full set {O0O0O00O000O00000['params']['rel_hist_full']}")#line:332
            elif OO0O0O000OOOOOOOO .result ['taskinfo']['task_type']=="UICMiner":#line:333
                print ("")#line:334
                O0O0O00O000O00000 =OO0O0O000OOOOOOOO .result ["rules"][OO0000O0000OO0000 -1 ]#line:335
                print (f"Rule id : {O0O0O00O000O00000['rule_id']}")#line:336
                print ("")#line:337
                OOO0OOO0OO000000O =""#line:338
                if ('aad_score'in O0O0O00O000O00000 ['params']):#line:339
                    OOO0OOO0OO000000O ="aad score : "+str (O0O0O00O000O00000 ['params']['aad_score'])#line:340
                print (f"Base : {'{:5d}'.format(O0O0O00O000O00000['params']['base'])}  Relative base : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_base'])}   {OOO0OOO0OO000000O}")#line:342
                print ("")#line:343
                print (f"Condition  : {O0O0O00O000O00000['cedents_str']['cond']}")#line:344
                print (f"Antecedent : {O0O0O00O000O00000['cedents_str']['ante']}")#line:345
                print ("")#line:346
                print (f"Histogram                                        {O0O0O00O000O00000['params']['hist']}")#line:347
                if ('aad_score'in O0O0O00O000O00000 ['params']):#line:348
                    print (f"Histogram on full set with condition             {O0O0O00O000O00000['params']['hist_cond']}")#line:349
                    print (f"Relative histogram                               {O0O0O00O000O00000['params']['rel_hist']}")#line:350
                    print (f"Relative histogram on full set with condition    {O0O0O00O000O00000['params']['rel_hist_cond']}")#line:351
                O00OO00OOO0OO00OO =OO0O0O000OOOOOOOO .result ['datalabels']['catnames'][OO0O0O000OOOOOOOO .result ['datalabels']['varname'].index (OO0O0O000OOOOOOOO .result ['taskinfo']['target'])]#line:352
                print (" ")#line:353
                print ("Interpretation:")#line:354
                for O000O00O000O0O00O in range (len (O00OO00OOO0OO00OO )):#line:355
                  O00000000O000O0OO =0 #line:356
                  if O0O0O00O000O00000 ['params']['rel_hist'][O000O00O000O0O00O ]>0 :#line:357
                      O00000000O000O0OO =O0O0O00O000O00000 ['params']['rel_hist'][O000O00O000O0O00O ]/O0O0O00O000O00000 ['params']['rel_hist_cond'][O000O00O000O0O00O ]#line:358
                  OO00O000O0O0OO00O =''#line:359
                  if not (O0O0O00O000O00000 ['cedents_str']['cond']=='---'):#line:360
                      OO00O000O0O0OO00O ="For "+O0O0O00O000O00000 ['cedents_str']['cond']+": "#line:361
                  print (f"    {OO00O000O0O0OO00O}{OO0O0O000OOOOOOOO.result['taskinfo']['target']}({O00OO00OOO0OO00OO[O000O00O000O0O00O]}) has occurence {'{:.1%}'.format(O0O0O00O000O00000['params']['rel_hist_cond'][O000O00O000O0O00O])}, with antecedent it has occurence {'{:.1%}'.format(O0O0O00O000O00000['params']['rel_hist'][O000O00O000O0O00O])}, that is {'{:.3f}'.format(O00000000O000O0OO)} times more.")#line:363
            elif OO0O0O000OOOOOOOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:364
                print ("")#line:365
                O0O0O00O000O00000 =OO0O0O000OOOOOOOO .result ["rules"][OO0000O0000OO0000 -1 ]#line:366
                print (f"Rule id : {O0O0O00O000O00000['rule_id']}")#line:367
                print ("")#line:368
                print (f"Base1 : {'{:5d}'.format(O0O0O00O000O00000['params']['base1'])} Base2 : {'{:5d}'.format(O0O0O00O000O00000['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(O0O0O00O000O00000['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(O0O0O00O000O00000['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(O0O0O00O000O00000['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(O0O0O00O000O00000['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(O0O0O00O000O00000['params']['ratioconf'])}")#line:369
                print ("")#line:370
                print ("Cedents:")#line:371
                print (f"  antecedent : {O0O0O00O000O00000['cedents_str']['ante']}")#line:372
                print (f"  succcedent : {O0O0O00O000O00000['cedents_str']['succ']}")#line:373
                print (f"  condition  : {O0O0O00O000O00000['cedents_str']['cond']}")#line:374
                print (f"  first set  : {O0O0O00O000O00000['cedents_str']['frst']}")#line:375
                print (f"  second set : {O0O0O00O000O00000['cedents_str']['scnd']}")#line:376
                print ("")#line:377
                print ("Fourfold tables:")#line:378
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:379
                print (f"----|-----|-----|  ----|-----|-----| ")#line:380
                print (f" A  |{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold1'][0])}|{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold2'][0])}|{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold2'][1])}|")#line:381
                print (f"----|-----|-----|  ----|-----|-----|")#line:382
                print (f"¬A  |{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold1'][2])}|{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold2'][2])}|{'{:5d}'.format(O0O0O00O000O00000['params']['fourfold2'][3])}|")#line:383
                print (f"----|-----|-----|  ----|-----|-----|")#line:384
            else :#line:385
                print ("Unsupported task type for rule details")#line:386
            print ("")#line:390
        else :#line:391
            print ("No such rule.")#line:392
    def get_ruletext (OO0O0O000O0000OOO ,O00O0OOOOO0OO0OO0 ):#line:394
        ""#line:400
        if not (OO0O0O000O0000OOO ._is_calculated ()):#line:401
            print ("ERROR: Task has not been calculated.")#line:402
            return #line:403
        if O00O0OOOOO0OO0OO0 <=0 or O00O0OOOOO0OO0OO0 >OO0O0O000O0000OOO .get_rulecount ():#line:404
            if OO0O0O000O0000OOO .get_rulecount ()==0 :#line:405
                print ("No such rule. There are no rules in result.")#line:406
            else :#line:407
                print (f"No such rule ({O00O0OOOOO0OO0OO0}). Available rules are 1 to {OO0O0O000O0000OOO.get_rulecount()}")#line:408
            return None #line:409
        OO000000OO0000000 =""#line:410
        OOOOOOO0OOOOO0OOO =OO0O0O000O0000OOO .result ["rules"][O00O0OOOOO0OO0OO0 -1 ]#line:411
        if OO0O0O000O0000OOO .result ['taskinfo']['task_type']=="4ftMiner":#line:412
            OO000000OO0000000 =OO000000OO0000000 +" "+OOOOOOO0OOOOO0OOO ["cedents_str"]["ante"]+" => "+OOOOOOO0OOOOO0OOO ["cedents_str"]["succ"]+" | "+OOOOOOO0OOOOO0OOO ["cedents_str"]["cond"]#line:414
        elif OO0O0O000O0000OOO .result ['taskinfo']['task_type']=="UICMiner":#line:415
            OO000000OO0000000 =OO000000OO0000000 +"     "+OOOOOOO0OOOOO0OOO ["cedents_str"]["ante"]+" => "+OO0O0O000O0000OOO .result ['taskinfo']['target']+"(*) | "+OOOOOOO0OOOOO0OOO ["cedents_str"]["cond"]#line:417
        elif OO0O0O000O0000OOO .result ['taskinfo']['task_type']=="CFMiner":#line:418
            OO000000OO0000000 =OO000000OO0000000 +" "+OOOOOOO0OOOOO0OOO ["cedents_str"]["cond"]#line:419
        elif OO0O0O000O0000OOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:420
            OO000000OO0000000 =OO000000OO0000000 +"  "+OOOOOOO0OOOOO0OOO ["cedents_str"]["ante"]+" => "+OOOOOOO0OOOOO0OOO ["cedents_str"]["succ"]+" | "+OOOOOOO0OOOOO0OOO ["cedents_str"]["cond"]+" : "+OOOOOOO0OOOOO0OOO ["cedents_str"]["frst"]+" x "+OOOOOOO0OOOOO0OOO ["cedents_str"]["scnd"]#line:422
        return OO000000OO0000000 #line:423
    def _annotate_chart (OO00O0O0O0OOOO00O ,O000OOOO0OOOOO000 ,O0O00O000OOOOO00O ,cnt =2 ):#line:425
        ""#line:432
        O0OO0000OOO0O0OO0 =O000OOOO0OOOOO000 .axes .get_ylim ()#line:433
        for O0OO0O00OOO00O000 in O000OOOO0OOOOO000 .patches :#line:435
            O0O00OOOOOOO0O00O ='{:.1f}%'.format (100 *O0OO0O00OOO00O000 .get_height ()/O0O00O000OOOOO00O )#line:436
            OO0000OO0O0000O0O =O0OO0O00OOO00O000 .get_x ()+O0OO0O00OOO00O000 .get_width ()/4 #line:437
            O00OO000O0O0OO00O =O0OO0O00OOO00O000 .get_y ()+O0OO0O00OOO00O000 .get_height ()-O0OO0000OOO0O0OO0 [1 ]/8 #line:438
            if O0OO0O00OOO00O000 .get_height ()<O0OO0000OOO0O0OO0 [1 ]/8 :#line:439
                O00OO000O0O0OO00O =O0OO0O00OOO00O000 .get_y ()+O0OO0O00OOO00O000 .get_height ()+O0OO0000OOO0O0OO0 [1 ]*0.02 #line:440
            O000OOOO0OOOOO000 .annotate (O0O00OOOOOOO0O00O ,(OO0000OO0O0000O0O ,O00OO000O0O0OO00O ),size =23 /cnt )#line:441
    def draw_rule (O0O00OOOO0OOOO00O ,O0O0OOOOO0O0OOO0O ,show =True ,filename =None ):#line:443
        ""#line:449
        if not (O0O00OOOO0OOOO00O ._is_calculated ()):#line:450
            print ("ERROR: Task has not been calculated.")#line:451
            return #line:452
        print ("")#line:453
        if (O0O0OOOOO0O0OOO0O <=len (O0O00OOOO0OOOO00O .result ["rules"])):#line:454
            if O0O00OOOO0OOOO00O .result ['taskinfo']['task_type']=="4ftMiner":#line:455
                OO000O000OOOO0OOO ,OOOO0000OOO00OOOO =plt .subplots (2 ,2 )#line:457
                OO000OO000OO0O0O0 =['S','not S']#line:458
                O00O0OO000000O0OO =['A','not A']#line:459
                OO000O00O000O00O0 =O0O00OOOO0OOOO00O .get_fourfold (O0O0OOOOO0O0OOO0O )#line:460
                OOO0O00O0OOOO0O00 =[OO000O00O000O00O0 [0 ],OO000O00O000O00O0 [1 ]]#line:462
                OO0OOO0O00000OO0O =[OO000O00O000O00O0 [2 ],OO000O00O000O00O0 [3 ]]#line:463
                OO0000O0O0OO00OOO =[OO000O00O000O00O0 [0 ]+OO000O00O000O00O0 [2 ],OO000O00O000O00O0 [1 ]+OO000O00O000O00O0 [3 ]]#line:464
                OOOO0000OOO00OOOO [0 ,0 ]=sns .barplot (ax =OOOO0000OOO00OOOO [0 ,0 ],x =OO000OO000OO0O0O0 ,y =OOO0O00O0OOOO0O00 ,color ='lightsteelblue')#line:465
                O0O00OOOO0OOOO00O ._annotate_chart (OOOO0000OOO00OOOO [0 ,0 ],OO000O00O000O00O0 [0 ]+OO000O00O000O00O0 [1 ])#line:467
                OOOO0000OOO00OOOO [0 ,1 ]=sns .barplot (ax =OOOO0000OOO00OOOO [0 ,1 ],x =OO000OO000OO0O0O0 ,y =OO0000O0O0OO00OOO ,color ="gray",edgecolor ="black")#line:469
                O0O00OOOO0OOOO00O ._annotate_chart (OOOO0000OOO00OOOO [0 ,1 ],sum (OO000O00O000O00O0 ))#line:471
                OOOO0000OOO00OOOO [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:473
                OOOO0000OOO00OOOO [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:474
                O0OO00OO0O0OOO00O =sns .color_palette ("Blues",as_cmap =True )#line:476
                OOO0O0000000OO0O0 =sns .color_palette ("Greys",as_cmap =True )#line:477
                OOOO0000OOO00OOOO [1 ,0 ]=sns .heatmap (ax =OOOO0000OOO00OOOO [1 ,0 ],data =[OOO0O00O0OOOO0O00 ,OO0OOO0O00000OO0O ],xticklabels =OO000OO000OO0O0O0 ,yticklabels =O00O0OO000000O0OO ,annot =True ,cbar =False ,fmt =".0f",cmap =O0OO00OO0O0OOO00O )#line:481
                OOOO0000OOO00OOOO [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:483
                OOOO0000OOO00OOOO [1 ,1 ]=sns .heatmap (ax =OOOO0000OOO00OOOO [1 ,1 ],data =np .asarray ([OO0000O0O0OO00OOO ]),xticklabels =OO000OO000OO0O0O0 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOO0O0000000OO0O0 )#line:487
                OOOO0000OOO00OOOO [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:489
                OOOO00OO00OOO00O0 =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']['ante']#line:491
                OOOO0000OOO00OOOO [0 ,0 ].set (title ="\n".join (wrap (OOOO00OO00OOO00O0 ,30 )))#line:492
                OOOO0000OOO00OOOO [0 ,1 ].set (title ='Entire dataset')#line:493
                O0000O00OO0OO000O =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']#line:495
                OO000O000OOOO0OOO .suptitle ("Antecedent : "+O0000O00OO0OO000O ['ante']+"\nSuccedent : "+O0000O00OO0OO000O ['succ']+"\nCondition : "+O0000O00OO0OO000O ['cond'],x =0 ,ha ='left',size ='small')#line:499
                OO000O000OOOO0OOO .tight_layout ()#line:500
            elif O0O00OOOO0OOOO00O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:502
                OO000O000OOOO0OOO ,OOOO0000OOO00OOOO =plt .subplots (2 ,2 )#line:504
                OO000OO000OO0O0O0 =['S','not S']#line:505
                O00O0OO000000O0OO =['A','not A']#line:506
                OO0O00O0OO00OO000 =O0O00OOOO0OOOO00O .get_fourfold (O0O0OOOOO0O0OOO0O ,order =1 )#line:508
                OOOOO0OOO00O00O0O =O0O00OOOO0OOOO00O .get_fourfold (O0O0OOOOO0O0OOO0O ,order =2 )#line:509
                OO00O0O000O00000O =[OO0O00O0OO00OO000 [0 ],OO0O00O0OO00OO000 [1 ]]#line:511
                OO00O0O0O0OO00O00 =[OO0O00O0OO00OO000 [2 ],OO0O00O0OO00OO000 [3 ]]#line:512
                OOOO000OOOO000000 =[OO0O00O0OO00OO000 [0 ]+OO0O00O0OO00OO000 [2 ],OO0O00O0OO00OO000 [1 ]+OO0O00O0OO00OO000 [3 ]]#line:513
                O0O0OOO00OOOOO0OO =[OOOOO0OOO00O00O0O [0 ],OOOOO0OOO00O00O0O [1 ]]#line:514
                O00000O0OOO0O0O0O =[OOOOO0OOO00O00O0O [2 ],OOOOO0OOO00O00O0O [3 ]]#line:515
                OO0O0000O0OOOOO0O =[OOOOO0OOO00O00O0O [0 ]+OOOOO0OOO00O00O0O [2 ],OOOOO0OOO00O00O0O [1 ]+OOOOO0OOO00O00O0O [3 ]]#line:516
                OOOO0000OOO00OOOO [0 ,0 ]=sns .barplot (ax =OOOO0000OOO00OOOO [0 ,0 ],x =OO000OO000OO0O0O0 ,y =OO00O0O000O00000O ,color ='orange')#line:517
                O0O00OOOO0OOOO00O ._annotate_chart (OOOO0000OOO00OOOO [0 ,0 ],OO0O00O0OO00OO000 [0 ]+OO0O00O0OO00OO000 [1 ])#line:519
                OOOO0000OOO00OOOO [0 ,1 ]=sns .barplot (ax =OOOO0000OOO00OOOO [0 ,1 ],x =OO000OO000OO0O0O0 ,y =O0O0OOO00OOOOO0OO ,color ="green")#line:521
                O0O00OOOO0OOOO00O ._annotate_chart (OOOO0000OOO00OOOO [0 ,1 ],OOOOO0OOO00O00O0O [0 ]+OOOOO0OOO00O00O0O [1 ])#line:523
                OOOO0000OOO00OOOO [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:525
                OOOO0000OOO00OOOO [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:526
                O0OO00OO0O0OOO00O =sns .color_palette ("Oranges",as_cmap =True )#line:528
                OOO0O0000000OO0O0 =sns .color_palette ("Greens",as_cmap =True )#line:529
                OOOO0000OOO00OOOO [1 ,0 ]=sns .heatmap (ax =OOOO0000OOO00OOOO [1 ,0 ],data =[OO00O0O000O00000O ,OO00O0O0O0OO00O00 ],xticklabels =OO000OO000OO0O0O0 ,yticklabels =O00O0OO000000O0OO ,annot =True ,cbar =False ,fmt =".0f",cmap =O0OO00OO0O0OOO00O )#line:532
                OOOO0000OOO00OOOO [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:534
                OOOO0000OOO00OOOO [1 ,1 ]=sns .heatmap (ax =OOOO0000OOO00OOOO [1 ,1 ],data =[O0O0OOO00OOOOO0OO ,O00000O0OOO0O0O0O ],xticklabels =OO000OO000OO0O0O0 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOO0O0000000OO0O0 )#line:538
                OOOO0000OOO00OOOO [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:540
                OOOO00OO00OOO00O0 =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']['frst']#line:542
                OOOO0000OOO00OOOO [0 ,0 ].set (title ="\n".join (wrap (OOOO00OO00OOO00O0 ,30 )))#line:543
                OOOO00000O00O000O =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']['scnd']#line:544
                OOOO0000OOO00OOOO [0 ,1 ].set (title ="\n".join (wrap (OOOO00000O00O000O ,30 )))#line:545
                O0000O00OO0OO000O =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']#line:547
                OO000O000OOOO0OOO .suptitle ("Antecedent : "+O0000O00OO0OO000O ['ante']+"\nSuccedent : "+O0000O00OO0OO000O ['succ']+"\nCondition : "+O0000O00OO0OO000O ['cond']+"\nFirst : "+O0000O00OO0OO000O ['frst']+"\nSecond : "+O0000O00OO0OO000O ['scnd'],x =0 ,ha ='left',size ='small')#line:552
                OO000O000OOOO0OOO .tight_layout ()#line:554
            elif (O0O00OOOO0OOOO00O .result ['taskinfo']['task_type']=="CFMiner")or (O0O00OOOO0OOOO00O .result ['taskinfo']['task_type']=="UICMiner"):#line:557
                OOOOO0O0O00O0OO0O =O0O00OOOO0OOOO00O .result ['taskinfo']['task_type']=="UICMiner"#line:558
                OO000O000OOOO0OOO ,OOOO0000OOO00OOOO =plt .subplots (2 ,2 ,gridspec_kw ={'height_ratios':[3 ,1 ]})#line:559
                OO0OO0000O00O0O0O =O0O00OOOO0OOOO00O .result ['taskinfo']['target']#line:560
                OO000OO000OO0O0O0 =O0O00OOOO0OOOO00O .result ['datalabels']['catnames'][O0O00OOOO0OOOO00O .result ['datalabels']['varname'].index (O0O00OOOO0OOOO00O .result ['taskinfo']['target'])]#line:562
                OO00O0OOO00O0OOO0 =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]#line:563
                O0O0OOOO0O0O0OOOO =O0O00OOOO0OOOO00O .get_hist (O0O0OOOOO0O0OOO0O )#line:564
                if OOOOO0O0O00O0OO0O :#line:565
                    O0O0OOOO0O0O0OOOO =OO00O0OOO00O0OOO0 ['params']['hist']#line:566
                else :#line:567
                    O0O0OOOO0O0O0OOOO =O0O00OOOO0OOOO00O .get_hist (O0O0OOOOO0O0OOO0O )#line:568
                OOOO0000OOO00OOOO [0 ,0 ]=sns .barplot (ax =OOOO0000OOO00OOOO [0 ,0 ],x =OO000OO000OO0O0O0 ,y =O0O0OOOO0O0O0OOOO ,color ='lightsteelblue')#line:569
                OO0OOO0O0O0OO00O0 =[]#line:571
                O0O0OO00OOO000000 =[]#line:572
                if OOOOO0O0O00O0OO0O :#line:573
                    OO0OOO0O0O0OO00O0 =OO000OO000OO0O0O0 #line:574
                    O0O0OO00OOO000000 =O0O00OOOO0OOOO00O .get_hist (O0O0OOOOO0O0OOO0O ,fullCond =True )#line:575
                else :#line:576
                    OO0OOO0O0O0OO00O0 =O0O00OOOO0OOOO00O .profiles ['hist_target_entire_dataset_labels']#line:577
                    O0O0OO00OOO000000 =O0O00OOOO0OOOO00O .profiles ['hist_target_entire_dataset_values']#line:578
                OOOO0000OOO00OOOO [0 ,1 ]=sns .barplot (ax =OOOO0000OOO00OOOO [0 ,1 ],x =OO0OOO0O0O0OO00O0 ,y =O0O0OO00OOO000000 ,color ="gray",edgecolor ="black")#line:579
                O0O00OOOO0OOOO00O ._annotate_chart (OOOO0000OOO00OOOO [0 ,0 ],sum (O0O0OOOO0O0O0OOOO ),len (O0O0OOOO0O0O0OOOO ))#line:581
                O0O00OOOO0OOOO00O ._annotate_chart (OOOO0000OOO00OOOO [0 ,1 ],sum (O0O0OO00OOO000000 ),len (O0O0OO00OOO000000 ))#line:582
                OOOO0000OOO00OOOO [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:584
                OOOO0000OOO00OOOO [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:585
                OOO000O0OOOOOO0O0 =[OO000OO000OO0O0O0 ,O0O0OOOO0O0O0OOOO ]#line:587
                O0O0O0O0O00OOOOOO =pd .DataFrame (OOO000O0OOOOOO0O0 ).transpose ()#line:588
                O0O0O0O0O00OOOOOO .columns =[OO0OO0000O00O0O0O ,'No of observatios']#line:589
                O0OO00OO0O0OOO00O =sns .color_palette ("Blues",as_cmap =True )#line:591
                OOO0O0000000OO0O0 =sns .color_palette ("Greys",as_cmap =True )#line:592
                OOOO0000OOO00OOOO [1 ,0 ]=sns .heatmap (ax =OOOO0000OOO00OOOO [1 ,0 ],data =np .asarray ([O0O0OOOO0O0O0OOOO ]),xticklabels =OO000OO000OO0O0O0 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =O0OO00OO0O0OOO00O )#line:596
                OOOO0000OOO00OOOO [1 ,0 ].set (xlabel =OO0OO0000O00O0O0O ,ylabel ='Count')#line:598
                OOOO0000OOO00OOOO [1 ,1 ]=sns .heatmap (ax =OOOO0000OOO00OOOO [1 ,1 ],data =np .asarray ([O0O0OO00OOO000000 ]),xticklabels =OO0OOO0O0O0OO00O0 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOO0O0000000OO0O0 )#line:602
                OOOO0000OOO00OOOO [1 ,1 ].set (xlabel =OO0OO0000O00O0O0O ,ylabel ='Count')#line:604
                O00O00OO0O0O00000 =""#line:605
                OOOO0O0000OO00O00 ='Entire dataset'#line:606
                if OOOOO0O0O00O0OO0O :#line:607
                    if len (OO00O0OOO00O0OOO0 ['cedents_struct']['cond'])>0 :#line:608
                        OOOO0O0000OO00O00 =OO00O0OOO00O0OOO0 ['cedents_str']['cond']#line:609
                        O00O00OO0O0O00000 =" & "+OO00O0OOO00O0OOO0 ['cedents_str']['cond']#line:610
                OOOO0000OOO00OOOO [0 ,1 ].set (title =OOOO0O0000OO00O00 )#line:611
                if OOOOO0O0O00O0OO0O :#line:612
                    OOOO00OO00OOO00O0 =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']['ante']+O00O00OO0O0O00000 #line:613
                else :#line:614
                    OOOO00OO00OOO00O0 =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']['cond']#line:615
                OOOO0000OOO00OOOO [0 ,0 ].set (title ="\n".join (wrap (OOOO00OO00OOO00O0 ,30 )))#line:616
                O0000O00OO0OO000O =O0O00OOOO0OOOO00O .result ["rules"][O0O0OOOOO0O0OOO0O -1 ]['cedents_str']#line:618
                OOOO0O0000OO00O00 ="Condition : "+O0000O00OO0OO000O ['cond']#line:619
                if OOOOO0O0O00O0OO0O :#line:620
                    OOOO0O0000OO00O00 =OOOO0O0000OO00O00 +"\nAntecedent : "+O0000O00OO0OO000O ['ante']#line:621
                OO000O000OOOO0OOO .suptitle (OOOO0O0000OO00O00 ,x =0 ,ha ='left',size ='small')#line:622
                OO000O000OOOO0OOO .tight_layout ()#line:624
            else :#line:625
                print ("Unsupported task type for rule details")#line:626
                return #line:627
            if filename is not None :#line:628
                plt .savefig (filename =filename )#line:629
            if show :#line:630
                plt .show ()#line:631
            print ("")#line:633
        else :#line:634
            print ("No such rule.")#line:635
    def get_rulecount (OOO000OO000000OOO ):#line:637
        ""#line:642
        if not (OOO000OO000000OOO ._is_calculated ()):#line:643
            print ("ERROR: Task has not been calculated.")#line:644
            return #line:645
        return len (OOO000OO000000OOO .result ["rules"])#line:646
    def get_fourfold (OOOOO0OOOO0OO0OO0 ,O00OOOOO0O00OOO0O ,order =0 ):#line:648
        ""#line:655
        if not (OOOOO0OOOO0OO0OO0 ._is_calculated ()):#line:656
            print ("ERROR: Task has not been calculated.")#line:657
            return #line:658
        if (O00OOOOO0O00OOO0O <=len (OOOOO0OOOO0OO0OO0 .result ["rules"])):#line:659
            if OOOOO0OOOO0OO0OO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:660
                OO000O0O0OO00O0O0 =OOOOO0OOOO0OO0OO0 .result ["rules"][O00OOOOO0O00OOO0O -1 ]#line:661
                return OO000O0O0OO00O0O0 ['params']['fourfold']#line:662
            elif OOOOO0OOOO0OO0OO0 .result ['taskinfo']['task_type']=="CFMiner":#line:663
                print ("Error: fourfold for CFMiner is not defined")#line:664
                return None #line:665
            elif OOOOO0OOOO0OO0OO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:666
                OO000O0O0OO00O0O0 =OOOOO0OOOO0OO0OO0 .result ["rules"][O00OOOOO0O00OOO0O -1 ]#line:667
                if order ==1 :#line:668
                    return OO000O0O0OO00O0O0 ['params']['fourfold1']#line:669
                if order ==2 :#line:670
                    return OO000O0O0OO00O0O0 ['params']['fourfold2']#line:671
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:672
                return None #line:673
            else :#line:674
                print ("Unsupported task type for rule details")#line:675
        else :#line:676
            print ("No such rule.")#line:677
    def get_hist (OOOOO000OOO000O00 ,O0OOO000OOOO00OO0 ,fullCond =True ):#line:679
        ""#line:686
        if not (OOOOO000OOO000O00 ._is_calculated ()):#line:687
            print ("ERROR: Task has not been calculated.")#line:688
            return #line:689
        if (O0OOO000OOOO00OO0 <=len (OOOOO000OOO000O00 .result ["rules"])):#line:690
            if OOOOO000OOO000O00 .result ['taskinfo']['task_type']=="CFMiner":#line:691
                O000OO0O0OO000O00 =OOOOO000OOO000O00 .result ["rules"][O0OOO000OOOO00OO0 -1 ]#line:692
                return O000OO0O0OO000O00 ['params']['hist']#line:693
            elif OOOOO000OOO000O00 .result ['taskinfo']['task_type']=="UICMiner":#line:694
                O000OO0O0OO000O00 =OOOOO000OOO000O00 .result ["rules"][O0OOO000OOOO00OO0 -1 ]#line:695
                O0OOOOO00OOO0OOOO =None #line:696
                if fullCond :#line:697
                    O0OOOOO00OOO0OOOO =O000OO0O0OO000O00 ['params']['hist_cond']#line:698
                else :#line:699
                    O0OOOOO00OOO0OOOO =O000OO0O0OO000O00 ['params']['hist']#line:700
                return O0OOOOO00OOO0OOOO #line:701
            elif OOOOO000OOO000O00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:702
                print ("Error: SD4ft-Miner has no histogram")#line:703
                return None #line:704
            elif OOOOO000OOO000O00 .result ['taskinfo']['task_type']=="4ftMiner":#line:705
                print ("Error: 4ft-Miner has no histogram")#line:706
                return None #line:707
            else :#line:708
                print ("Unsupported task type for rule details")#line:709
        else :#line:710
            print ("No such rule.")#line:711
    def get_hist_cond (O0O00OO00O00O0OOO ,OOOOO00OOO0O0OOOO ):#line:714
        ""#line:720
        if not (O0O00OO00O00O0OOO ._is_calculated ()):#line:721
            print ("ERROR: Task has not been calculated.")#line:722
            return #line:723
        if (OOOOO00OOO0O0OOOO <=len (O0O00OO00O00O0OOO .result ["rules"])):#line:725
            if O0O00OO00O00O0OOO .result ['taskinfo']['task_type']=="UICMiner":#line:726
                O00O00000OO000000 =O0O00OO00O00O0OOO .result ["rules"][OOOOO00OOO0O0OOOO -1 ]#line:727
                return O00O00000OO000000 ['params']['hist_cond']#line:728
            elif O0O00OO00O00O0OOO .result ['taskinfo']['task_type']=="CFMiner":#line:729
                O00O00000OO000000 =O0O00OO00O00O0OOO .result ["rules"][OOOOO00OOO0O0OOOO -1 ]#line:730
                return O00O00000OO000000 ['params']['hist']#line:731
            elif O0O00OO00O00O0OOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:732
                print ("Error: SD4ft-Miner has no histogram")#line:733
                return None #line:734
            elif O0O00OO00O00O0OOO .result ['taskinfo']['task_type']=="4ftMiner":#line:735
                print ("Error: 4ft-Miner has no histogram")#line:736
                return None #line:737
            else :#line:738
                print ("Unsupported task type for rule details")#line:739
        else :#line:740
            print ("No such rule.")#line:741
    def get_quantifiers (O000O00OOO0OO00O0 ,O000OO00O00OOOOOO ,order =0 ):#line:743
        ""#line:752
        if not (O000O00OOO0OO00O0 ._is_calculated ()):#line:753
            print ("ERROR: Task has not been calculated.")#line:754
            return None #line:755
        if (O000OO00O00OOOOOO <=len (O000O00OOO0OO00O0 .result ["rules"])):#line:757
            OO000O0O0OO0OO0O0 =O000O00OOO0OO00O0 .result ["rules"][O000OO00O00OOOOOO -1 ]#line:758
            if O000O00OOO0OO00O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:759
                return OO000O0O0OO0OO0O0 ['params']#line:760
            elif O000O00OOO0OO00O0 .result ['taskinfo']['task_type']=="CFMiner":#line:761
                return OO000O0O0OO0OO0O0 ['params']#line:762
            elif O000O00OOO0OO00O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:763
                return OO000O0O0OO0OO0O0 ['params']#line:764
            else :#line:765
                print ("Unsupported task type for rule details")#line:766
        else :#line:767
            print ("No such rule.")#line:768
    def get_varlist (OO000O0OO000OOOOO ):#line:770
        ""#line:774
        return OO000O0OO000OOOOO .result ["datalabels"]["varname"]#line:776
    def get_category_names (OO0000O0OO0O000O0 ,varname =None ,varindex =None ):#line:778
        ""#line:785
        OOOOO00OO00O000OO =0 #line:786
        if varindex is not None :#line:787
            if OOOOO00OO00O000OO >=0 &OOOOO00OO00O000OO <len (OO0000O0OO0O000O0 .get_varlist ()):#line:788
                OOOOO00OO00O000OO =varindex #line:789
            else :#line:790
                print ("Error: no such variable.")#line:791
                return #line:792
        if (varname is not None ):#line:793
            OO0OOO00O0OOOOOOO =OO0000O0OO0O000O0 .get_varlist ()#line:794
            OOOOO00OO00O000OO =OO0OOO00O0OOOOOOO .index (varname )#line:795
            if OOOOO00OO00O000OO ==-1 |OOOOO00OO00O000OO <0 |OOOOO00OO00O000OO >=len (OO0000O0OO0O000O0 .get_varlist ()):#line:796
                print ("Error: no such variable.")#line:797
                return #line:798
        return OO0000O0OO0O000O0 .result ["datalabels"]["catnames"][OOOOO00OO00O000OO ]#line:799
    def print_data_definition (O0O00OO0OO0OO00OO ):#line:801
        ""#line:804
        OOO00000O00O0O0O0 =O0O00OO0OO0OO00OO .get_varlist ()#line:805
        print (f"Dataset has {len(OOO00000O00O0O0O0)} variables.")#line:806
        for OOO0OOO0OO00O0O0O in OOO00000O00O0O0O0 :#line:807
            O0OOOO000O00O0000 =O0O00OO0OO0OO00OO .get_category_names (OOO0OOO0OO00O0O0O )#line:808
            OOO0O0O0OOO00O000 =""#line:809
            for O0O00000OO0OO00OO in O0OOOO000O00O0000 :#line:810
                OOO0O0O0OOO00O000 =OOO0O0O0OOO00O000 +str (O0O00000OO0OO00OO )+" "#line:811
            OOO0O0O0OOO00O000 =OOO0O0O0OOO00O000 [:-1 ]#line:812
            print (f"Variable {OOO0OOO0OO00O0O0O} has {len(O0OOOO000O00O0000)} categories: {OOO0O0O0OOO00O000}")#line:813
    def _is_calculated (O00000O0OOO0O00OO ):#line:815
        ""#line:820
        O0O0000O000OO0O0O =False #line:821
        if 'taskinfo'in O00000O0OOO0O00OO .result :#line:822
            O0O0000O000OO0O0O =True #line:823
        return O0O0000O000OO0O0O #line:824
    def save (O00OOO000O0O0OOOO ,OOO0OOOOOOOOO00O0 ,savedata =False ,embeddata =True ,fmt ='pickle'):#line:826
        if not (O00OOO000O0O0OOOO ._is_calculated ()):#line:827
            print ("ERROR: Task has not been calculated.")#line:828
            return None #line:829
        OOOOO0O0O0OOO0000 ={'program':'CleverMiner','version':O00OOO000O0O0OOOO .get_version_string ()}#line:830
        OOO0O0OOO0OO00O00 ={}#line:831
        OOO0O0OOO0OO00O00 ['control']=OOOOO0O0O0OOO0000 #line:832
        OOO0O0OOO0OO00O00 ['result']=O00OOO000O0O0OOOO .result #line:833
        OOO0O0OOO0OO00O00 ['stats']=O00OOO000O0O0OOOO .stats #line:835
        OOO0O0OOO0OO00O00 ['options']=O00OOO000O0O0OOOO .options #line:836
        OOO0O0OOO0OO00O00 ['profiles']=O00OOO000O0O0OOOO .profiles #line:837
        if savedata :#line:838
            if embeddata :#line:839
                OOO0O0OOO0OO00O00 ['data']=O00OOO000O0O0OOOO .data #line:840
                OOO0O0OOO0OO00O00 ['df']=O00OOO000O0O0OOOO .df #line:841
            else :#line:842
                OO0O00OO000O000OO ={}#line:843
                OO0O00OO000O000OO ['data']=O00OOO000O0O0OOOO .data #line:844
                OO0O00OO000O000OO ['df']=O00OOO000O0O0OOOO .df #line:845
                print (f"CALC HASH {datetime.now()}")#line:846
                OOOO0000000OOOO0O =O00OOO000O0O0OOOO ._get_fast_hash (OO0O00OO000O000OO )#line:848
                print (f"CALC HASH ...done {datetime.now()}")#line:849
                OOOO0000000O000O0 =os .path .join (O00OOO000O0O0OOOO .cache_dir ,OOOO0000000OOOO0O +'.clmdata')#line:850
                OOO000O00OO0O0O00 =open (OOOO0000000O000O0 ,'wb')#line:853
                pickle .dump (OO0O00OO000O000OO ,OOO000O00OO0O0O00 ,protocol =pickle .HIGHEST_PROTOCOL )#line:854
                OOO0O0OOO0OO00O00 ['datafile']=OOOO0000000O000O0 #line:857
        if fmt =='pickle':#line:859
            O00000OOO000000O0 =open (OOO0OOOOOOOOO00O0 ,'wb')#line:860
            pickle .dump (OOO0O0OOO0OO00O00 ,O00000OOO000000O0 ,protocol =pickle .HIGHEST_PROTOCOL )#line:861
        elif fmt =='json':#line:862
            O00000OOO000000O0 =open (OOO0OOOOOOOOO00O0 ,'w')#line:863
            json .dump (OOO0O0OOO0OO00O00 ,O00000OOO000000O0 )#line:864
        else :#line:865
            print (f"Unsupported format - {fmt}. Supported formats are pickle, json.")#line:866
    def load (O00OO00OO00OOO0OO ,O000O0000OO00O00O ,fmt ='pickle'):#line:870
        O0O00O00OO0OO000O =False #line:871
        if '://'in O000O0000OO00O00O :#line:872
            O0O00O00OO0OO000O =True #line:873
        if fmt =='pickle':#line:874
            if O0O00O00OO0OO000O :#line:875
                O0OO000O00O00000O =pickle .load (urllib .request .urlopen (O000O0000OO00O00O ))#line:876
            else :#line:877
                O0OOO0O000O00O0O0 =open (O000O0000OO00O00O ,'rb')#line:878
                O0OO000O00O00000O =pickle .load (O0OOO0O000O00O0O0 )#line:879
        elif fmt =='json':#line:880
            if O0O00O00OO0OO000O :#line:881
                O0OO000O00O00000O =json .load (urllib .request .urlopen (O000O0000OO00O00O ))#line:882
            else :#line:883
                O0OOO0O000O00O0O0 =open (O000O0000OO00O00O ,'r')#line:884
                O0OO000O00O00000O =json .load (O0OOO0O000O00O0O0 )#line:885
        else :#line:886
            print (f"Unsupported format - {fmt}. Supported formats are pickle, json.")#line:887
            return #line:888
        if not 'control'in O0OO000O00O00000O :#line:889
            print ('Error: not a CleverMiner save file (1)')#line:890
            return None #line:891
        O0OO00OOOOO0OO0O0 =O0OO000O00O00000O ['control']#line:892
        if not ('program'in O0OO00OOOOO0OO0O0 )or not ('version'in O0OO00OOOOO0OO0O0 ):#line:893
            print ('Error: not a CleverMiner save file (2)')#line:894
            return None #line:895
        if not (O0OO00OOOOO0OO0O0 ['program']=='CleverMiner'):#line:896
            print ('Error: not a CleverMiner save file (3)')#line:897
            return None #line:898
        O00OO00OO00OOO0OO .result =O0OO000O00O00000O ['result']#line:899
        O00OO00OO00OOO0OO .stats =O0OO000O00O00000O ['stats']#line:901
        O00OO00OO00OOO0OO .options =O0OO000O00O00000O ['options']#line:902
        if 'profiles'in O0OO000O00O00000O :#line:903
            O00OO00OO00OOO0OO .profiles =O0OO000O00O00000O ['profiles']#line:904
        if 'data'in O0OO000O00O00000O :#line:905
            O00OO00OO00OOO0OO .data =O0OO000O00O00000O ['data']#line:906
            O00OO00OO00OOO0OO ._initialized =True #line:907
        if 'df'in O0OO000O00O00000O :#line:908
            O00OO00OO00OOO0OO .df =O0OO000O00O00000O ['df']#line:909
        if 'datafile'in O0OO000O00O00000O :#line:910
            try :#line:911
                O00OOOO000OO0O0O0 =open (O0OO000O00O00000O ['datafile'],'rb')#line:912
                OOOO000OO0O0O0OO0 =pickle .load (O00OOOO000OO0O0O0 )#line:913
                O00OO00OO00OOO0OO .data =OOOO000OO0O0O0OO0 ['data']#line:914
                O00OO00OO00OOO0OO .df =OOOO000OO0O0O0OO0 ['df']#line:915
                print (f"...data loaded from file {O0OO000O00O00000O['datafile']}.")#line:916
            except :#line:917
                print (f"Error loading saved file. Linked data file does not exists or it is in incorrect structure or path. If you are transferring saved file to another computer, please embed also data.")#line:919
                exit (1 )#line:920
        print (f"File {O000O0000OO00O00O} loaded ok.")#line:921
    def get_version_string (O000O0OO00OO00OOO ):#line:924
        ""#line:929
        return O000O0OO00OO00OOO .version_string #line:930
    def get_rule_cedent_list (OO0OOOO00OOOOO0O0 ,OOO00O0OO000OOOO0 ):#line:932
        ""#line:938
        if not (OO0OOOO00OOOOO0O0 ._is_calculated ()):#line:939
            print ("ERROR: Task has not been calculated.")#line:940
            return #line:941
        if OOO00O0OO000OOOO0 <=0 or OOO00O0OO000OOOO0 >OO0OOOO00OOOOO0O0 .get_rulecount ():#line:942
            if OO0OOOO00OOOOO0O0 .get_rulecount ()==0 :#line:943
                print ("No such rule. There are no rules in result.")#line:944
            else :#line:945
                print (f"No such rule ({OOO00O0OO000OOOO0}). Available rules are 1 to {OO0OOOO00OOOOO0O0.get_rulecount()}")#line:946
            return None #line:947
        O0O0OOOOOO000OO00 =[]#line:948
        O0O0O0O00OOOO000O =OO0OOOO00OOOOO0O0 .result ["rules"][OOO00O0OO000OOOO0 -1 ]#line:949
        O0O0OOOOOO000OO00 =list (O0O0O0O00OOOO000O ['trace_cedent_dataorder'].keys ())#line:950
        return O0O0OOOOOO000OO00 #line:952
    def get_rule_variables (O0000OOOOOO000OOO ,OOOO0OOOO0OO00OOO ,O0O000000OO0OOO00 ,get_names =True ):#line:955
        ""#line:963
        if not (O0000OOOOOO000OOO ._is_calculated ()):#line:964
            print ("ERROR: Task has not been calculated.")#line:965
            return #line:966
        if OOOO0OOOO0OO00OOO <=0 or OOOO0OOOO0OO00OOO >O0000OOOOOO000OOO .get_rulecount ():#line:967
            if O0000OOOOOO000OOO .get_rulecount ()==0 :#line:968
                print ("No such rule. There are no rules in result.")#line:969
            else :#line:970
                print (f"No such rule ({OOOO0OOOO0OO00OOO}). Available rules are 1 to {O0000OOOOOO000OOO.get_rulecount()}")#line:971
            return None #line:972
        OOOOOOO0O00OO00OO =[]#line:973
        OO00OO0OOO00O00O0 =O0000OOOOOO000OOO .result ["rules"][OOOO0OOOO0OO00OOO -1 ]#line:974
        O0000O0O000O0O00O =O0000OOOOOO000OOO .result ["datalabels"]['varname']#line:975
        if not (O0O000000OO0OOO00 in OO00OO0OOO00O00O0 ['trace_cedent_dataorder']):#line:976
            print (f"ERROR: cedent {O0O000000OO0OOO00} not in result.")#line:977
            exit (1 )#line:978
        for O000O000O0OO0O0OO in OO00OO0OOO00O00O0 ['trace_cedent_dataorder'][O0O000000OO0OOO00 ]:#line:979
            if get_names :#line:980
                OOOOOOO0O00OO00OO .append (O0000O0O000O0O00O [O000O000O0OO0O0OO ])#line:981
            else :#line:982
                OOOOOOO0O00OO00OO .append (O000O000O0OO0O0OO )#line:983
        return OOOOOOO0O00OO00OO #line:985
    def get_rule_categories (O00OOO0OOO0OO00OO ,O00OO0000O000000O ,OO0OOOO00OO000000 ,O0O0O0OO0O0OO0O00 ,get_names =True ):#line:988
        ""#line:997
        if not (O00OOO0OOO0OO00OO ._is_calculated ()):#line:998
            print ("ERROR: Task has not been calculated.")#line:999
            return #line:1000
        if O00OO0000O000000O <=0 or O00OO0000O000000O >O00OOO0OOO0OO00OO .get_rulecount ():#line:1001
            if O00OOO0OOO0OO00OO .get_rulecount ()==0 :#line:1002
                print ("No such rule. There are no rules in result.")#line:1003
            else :#line:1004
                print (f"No such rule ({O00OO0000O000000O}). Available rules are 1 to {O00OOO0OOO0OO00OO.get_rulecount()}")#line:1005
            return None #line:1006
        OO00OOOOO0OO00O0O =[]#line:1007
        OOOOOOO00O0000O0O =O00OOO0OOO0OO00OO .result ["rules"][O00OO0000O000000O -1 ]#line:1008
        OO00O0OO0O0OO00OO =O00OOO0OOO0OO00OO .result ["datalabels"]['varname']#line:1009
        if O0O0O0OO0O0OO0O00 in OO00O0OO0O0OO00OO :#line:1010
            OO0OO00O00OO00O00 =OO00O0OO0O0OO00OO .index (O0O0O0OO0O0OO0O00 )#line:1011
            OO0O0OOOO0OOOO0O0 =O00OOO0OOO0OO00OO .result ['datalabels']['catnames'][OO0OO00O00OO00O00 ]#line:1012
            if not (OO0OOOO00OO000000 in OOOOOOO00O0000O0O ['trace_cedent_dataorder']):#line:1013
                print (f"ERROR: cedent {OO0OOOO00OO000000} not in result.")#line:1014
                exit (1 )#line:1015
            OOO000OOO0OOOOOOO =OOOOOOO00O0000O0O ['trace_cedent_dataorder'][OO0OOOO00OO000000 ].index (OO0OO00O00OO00O00 )#line:1016
            for OO0O0O000000OO0O0 in OOOOOOO00O0000O0O ['traces'][OO0OOOO00OO000000 ][OOO000OOO0OOOOOOO ]:#line:1017
                if get_names :#line:1018
                    OO00OOOOO0OO00O0O .append (OO0O0OOOO0OOOO0O0 [OO0O0O000000OO0O0 ])#line:1019
                else :#line:1020
                    OO00OOOOO0OO00O0O .append (OO0O0O000000OO0O0 )#line:1021
        else :#line:1022
            print (f"ERROR: variable not found: {OO0OOOO00OO000000},{O0O0O0OO0O0OO0O00}. Possible variables are {OO00O0OO0O0OO00OO}")#line:1023
            exit (1 )#line:1024
        return OO00OOOOO0OO00O0O #line:1025
    def get_dataset_variable_count (OO00OO0OOOOO0OO00 ):#line:1028
        ""#line:1033
        if not (OO00OO0OOOOO0OO00 ._is_calculated ()):#line:1034
            print ("ERROR: Task has not been calculated.")#line:1035
            return #line:1036
        OO0O0OO00000O0O0O =OO00OO0OOOOO0OO00 .result ["datalabels"]['varname']#line:1037
        return len (OO0O0OO00000O0O0O )#line:1038
    def get_dataset_variable_list (OOOO00OO0000O0O0O ):#line:1041
        ""#line:1046
        if not (OOOO00OO0000O0O0O ._is_calculated ()):#line:1047
            print ("ERROR: Task has not been calculated.")#line:1048
            return #line:1049
        O0O0OOO00000O0O0O =OOOO00OO0000O0O0O .result ["datalabels"]['varname']#line:1050
        return O0O0OOO00000O0O0O #line:1051
    def get_dataset_variable_name (O0OOO000OOO0O0O0O ,OOO0O0OO00000000O ):#line:1054
        ""#line:1060
        if not (O0OOO000OOO0O0O0O ._is_calculated ()):#line:1061
            print ("ERROR: Task has not been calculated.")#line:1062
            return #line:1063
        O0OO0OOO00OO00OOO =O0OOO000OOO0O0O0O .get_dataset_variable_list ()#line:1064
        if OOO0O0OO00000000O >=0 and OOO0O0OO00000000O <len (O0OO0OOO00OO00OOO ):#line:1065
            return O0OO0OOO00OO00OOO [OOO0O0OO00000000O ]#line:1066
        else :#line:1067
            print (f"ERROR: dataset has only {len(O0OO0OOO00OO00OOO)} variables, required index is {OOO0O0OO00000000O}, but available values are 0-{len(O0OO0OOO00OO00OOO)-1}.")#line:1068
            exit (1 )#line:1069
    def get_dataset_variable_index (OOO00OOOO0O000O0O ,OOOOO0O0OO0OOO00O ):#line:1071
        ""#line:1077
        if not (OOO00OOOO0O000O0O ._is_calculated ()):#line:1078
            print ("ERROR: Task has not been calculated.")#line:1079
            return #line:1080
        O00O00O00OOO0000O =OOO00OOOO0O000O0O .get_dataset_variable_list ()#line:1081
        if OOOOO0O0OO0OOO00O in O00O00O00OOO0000O :#line:1082
            return O00O00O00OOO0000O .index (OOOOO0O0OO0OOO00O )#line:1083
        else :#line:1084
            print (f"ERROR: attribute {OOOOO0O0OO0OOO00O} is not in dataset. The list of attribute names is  {O00O00O00OOO0000O}.")#line:1085
            exit (1 )#line:1086
    def get_dataset_category_list (OO000O000OO00OO0O ,OOO0O000O0O0OO0OO ):#line:1089
        ""#line:1095
        if not (OO000O000OO00OO0O ._is_calculated ()):#line:1096
            print ("ERROR: Task has not been calculated.")#line:1097
            return #line:1098
        O0000000OOOO0000O =OO000O000OO00OO0O .result ["datalabels"]['catnames']#line:1099
        O00O00000OOO000O0 =None #line:1100
        if isinstance (OOO0O000O0O0OO0OO ,int ):#line:1101
            O00O00000OOO000O0 =OOO0O000O0O0OO0OO #line:1102
        else :#line:1103
            O00O00000OOO000O0 =OO000O000OO00OO0O .get_dataset_variable_index (OOO0O000O0O0OO0OO )#line:1104
        if O00O00000OOO000O0 >=0 and O00O00000OOO000O0 <len (O0000000OOOO0000O ):#line:1106
            return O0000000OOOO0000O [O00O00000OOO000O0 ]#line:1107
        else :#line:1108
            print (f"ERROR: dataset has only {len(O0000000OOOO0000O)} variables, required index is {O00O00000OOO000O0}, but available values are 0-{len(O0000000OOOO0000O)-1}.")#line:1109
            exit (1 )#line:1110
    def get_dataset_category_count (O0OO00OOO00OO0O00 ,O0OO00OOO0OOO000O ):#line:1112
        ""#line:1118
        if not (O0OO00OOO00OO0O00 ._is_calculated ()):#line:1119
            print ("ERROR: Task has not been calculated.")#line:1120
            return #line:1121
        O0O0000O00OOOOO00 =None #line:1122
        if isinstance (O0OO00OOO0OOO000O ,int ):#line:1123
            O0O0000O00OOOOO00 =O0OO00OOO0OOO000O #line:1124
        else :#line:1125
            O0O0000O00OOOOO00 =O0OO00OOO00OO0O00 .get_dataset_variable_index (O0OO00OOO0OOO000O )#line:1126
        OO0OO0O00O0OO0O0O =O0OO00OOO00OO0O00 .get_dataset_category_list (O0O0000O00OOOOO00 )#line:1127
        return len (OO0OO0O00O0OO0O0O )#line:1128
    def get_dataset_category_name (OOO00O000OOOOO0O0 ,OOO00OOO0OO00O0OO ,OOOO0OOOOOOO0O000 ):#line:1131
        ""#line:1138
        if not (OOO00O000OOOOO0O0 ._is_calculated ()):#line:1139
            print ("ERROR: Task has not been calculated.")#line:1140
            return #line:1141
        O0OO000OOOO00O0OO =None #line:1142
        if isinstance (OOO00OOO0OO00O0OO ,int ):#line:1143
            O0OO000OOOO00O0OO =OOO00OOO0OO00O0OO #line:1144
        else :#line:1145
            O0OO000OOOO00O0OO =OOO00O000OOOOO0O0 .get_dataset_variable_index (OOO00OOO0OO00O0OO )#line:1146
        O00000000000000O0 =OOO00O000OOOOO0O0 .get_dataset_category_list (O0OO000OOOO00O0OO )#line:1148
        if OOOO0OOOOOOO0O000 >=0 and OOOO0OOOOOOO0O000 <len (O00000000000000O0 ):#line:1149
            return O00000000000000O0 [OOOO0OOOOOOO0O000 ]#line:1150
        else :#line:1151
            print (f"ERROR: variable has only {len(O00000000000000O0)} categories, required index is {OOOO0OOOOOOO0O000}, but available values are 0-{len(O00000000000000O0)-1}.")#line:1152
            exit (1 )#line:1153
    def get_dataset_category_index (OOOO000O0O0OOO000 ,OO0000000OO00OOOO ,O00OO00O0OOO0O00O ):#line:1156
        ""#line:1163
        if not (OOOO000O0O0OOO000 ._is_calculated ()):#line:1164
            print ("ERROR: Task has not been calculated.")#line:1165
            return #line:1166
        O0O0O0OOO00OO0000 =None #line:1167
        if isinstance (OO0000000OO00OOOO ,int ):#line:1168
            O0O0O0OOO00OO0000 =OO0000000OO00OOOO #line:1169
        else :#line:1170
            O0O0O0OOO00OO0000 =OOOO000O0O0OOO000 .get_dataset_variable_index (OO0000000OO00OOOO )#line:1171
        O0O00OO0O00O000O0 =OOOO000O0O0OOO000 .get_dataset_category_list (O0O0O0OOO00OO0000 )#line:1172
        if O00OO00O0OOO0O00O in O0O00OO0O00O000O0 :#line:1173
            return O0O00OO0O00O000O0 .index (O00OO00O0OOO0O00O )#line:1174
        else :#line:1175
            print (f"ERROR: value {O00OO00O0OOO0O00O} is invalid for the variable {OOOO000O0O0OOO000.get_dataset_variable_name(O0O0O0OOO00OO0000)}. Available category names are {O0O00OO0O00O000O0}.")#line:1176
            exit (1 )#line:1177
def clm_vars (OO00O0O0O00OOO0O0 ,minlen =1 ,maxlen =3 ,type ='con'):#line:1179
    ""#line:1187
    O00OO00OO0OOOO00O =[]#line:1188
    for O00O000O0O0O0000O in OO00O0O0O00OOO0O0 :#line:1189
        if isinstance (O00O000O0O0O0000O ,dict ):#line:1190
            OO0OO000OOOO0O0OO =O00O000O0O0O0000O #line:1191
        else :#line:1192
            OO0OO000OOOO0O0OO ={}#line:1193
            OO0OO000OOOO0O0OO ['name']=O00O000O0O0O0000O #line:1194
            OO0OO000OOOO0O0OO ['type']='subset'#line:1195
            OO0OO000OOOO0O0OO ['minlen']=1 #line:1196
            OO0OO000OOOO0O0OO ['maxlen']=1 #line:1197
        O00OO00OO0OOOO00O .append (OO0OO000OOOO0O0OO )#line:1198
    O0O0OO00OO00O0O0O ={}#line:1199
    O0O0OO00OO00O0O0O ['attributes']=O00OO00OO0OOOO00O #line:1200
    O0O0OO00OO00O0O0O ['minlen']=minlen #line:1201
    O0O0OO00OO00O0O0O ['maxlen']=maxlen #line:1202
    O0O0OO00OO00O0O0O ['type']=type #line:1203
    return O0O0OO00OO00O0O0O #line:1204
def clm_subset (O0OO0O0O0O0000OOO ,minlen =1 ,maxlen =1 ):#line:1206
    ""#line:1214
    OOOOO0OO00OOO000O ={}#line:1215
    OOOOO0OO00OOO000O ['name']=O0OO0O0O0O0000OOO #line:1216
    OOOOO0OO00OOO000O ['type']='subset'#line:1217
    OOOOO0OO00OOO000O ['minlen']=minlen #line:1218
    OOOOO0OO00OOO000O ['maxlen']=maxlen #line:1219
    return OOOOO0OO00OOO000O #line:1220
def clm_seq (OOO00O0000O0OOO0O ,minlen =1 ,maxlen =2 ):#line:1222
    ""#line:1230
    OO0O000000OO0O00O ={}#line:1231
    OO0O000000OO0O00O ['name']=OOO00O0000O0OOO0O #line:1232
    OO0O000000OO0O00O ['type']='seq'#line:1233
    OO0O000000OO0O00O ['minlen']=minlen #line:1234
    OO0O000000OO0O00O ['maxlen']=maxlen #line:1235
    return OO0O000000OO0O00O #line:1236
def clm_lcut (OOO0O000O0000OOOO ,minlen =1 ,maxlen =2 ):#line:1238
    ""#line:1246
    OOO00OOO0O000000O ={}#line:1247
    OOO00OOO0O000000O ['name']=OOO0O000O0000OOOO #line:1248
    OOO00OOO0O000000O ['type']='lcut'#line:1249
    OOO00OOO0O000000O ['minlen']=minlen #line:1250
    OOO00OOO0O000000O ['maxlen']=maxlen #line:1251
    return OOO00OOO0O000000O #line:1252
def clm_rcut (O00OO00000000O000 ,minlen =1 ,maxlen =2 ):#line:1254
    ""#line:1262
    OOO0OO00O00OOOOO0 ={}#line:1263
    OOO0OO00O00OOOOO0 ['name']=O00OO00000000O000 #line:1264
    OOO0OO00O00OOOOO0 ['type']='rcut'#line:1265
    OOO0OO00O00OOOOO0 ['minlen']=minlen #line:1266
    OOO0OO00O00OOOOO0 ['maxlen']=maxlen #line:1267
    return OOO0OO00O00OOOOO0 #line:1268

