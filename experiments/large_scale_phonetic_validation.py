#!/usr/bin/env python3
"""
Large-Scale Phonetic-Semantic Validation Study
===============================================

A comprehensive test of the hypothesis:
"Word shapes correlate with semantic dimensions universally"

This study includes:
- 15+ languages from diverse families
- 50+ words per semantic dimension
- Statistical significance testing
- Multiple phonetic feature analysis
- Clear pass/fail criteria

Languages tested across major families:
- Indo-European: English, French, German, Spanish, Italian, Portuguese, Russian, Hindi
- Sino-Tibetan: Mandarin Chinese
- Semitic: Hebrew, Arabic
- Austronesian: Indonesian, Tagalog, Wedau
- Japonic: Japanese
- Koreanic: Korean
- Turkic: Turkish
- Uralic: Finnish

If phonetic-semantic correlation is universal:
- Power words should consistently have more hard consonants
- Love words should consistently have more vowels/soft sounds
- This should hold across unrelated language families
"""

import sys
import os
import numpy as np
from collections import defaultdict
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from experiments.enhanced_pattern_detector import EnhancedPatternDetector

# Phonetic categories (IPA-based universal categories)
SOFT_CONSONANTS = set('mnlrwyɱɳŋɲɴʎʟɻɽɾɰ')  # Nasals, liquids, glides
HARD_CONSONANTS = set('kptbdgqcɡɢʔʡ')  # Plosives/stops
FRICATIVES = set('szfvhθðʃʒxɣχʁħʕhɦβɸ')  # Fricatives
VOWELS = set('aeiouæɛɪɔʊəɐʌɑɒœøyɨʉɯ')

# Extended vocabulary: 50 words per dimension across 15+ languages
EXTENDED_VOCABULARY = {
    'Love': {
        # Germanic
        'english': ['love', 'mercy', 'compassion', 'gentle', 'tender', 'care', 'embrace', 'forgive', 'kind', 'warm', 
                    'affection', 'cherish', 'adore', 'heart', 'nurture', 'comfort', 'sympathy', 'sweetness', 'fondness', 'devotion'],
        'german': ['liebe', 'barmherzigkeit', 'mitgefuhl', 'sanft', 'zart', 'pflege', 'umarmung', 'vergeben', 'freundlich', 'warm',
                   'zuneigung', 'schatz', 'anbeten', 'herz', 'naehren', 'trost', 'sympathie', 'suesse', 'zartlich', 'hingabe'],
        
        # Romance
        'french': ['amour', 'misericorde', 'compassion', 'doux', 'tendre', 'soin', 'embrasser', 'pardonner', 'gentil', 'chaleur',
                   'affection', 'cherir', 'adorer', 'coeur', 'nourrir', 'confort', 'sympathie', 'douceur', 'tendresse', 'devotion'],
        'spanish': ['amor', 'misericordia', 'compasion', 'suave', 'tierno', 'cuidado', 'abrazar', 'perdonar', 'amable', 'calor',
                    'carino', 'querer', 'adorar', 'corazon', 'nutrir', 'consuelo', 'simpatia', 'dulzura', 'ternura', 'devocion'],
        'italian': ['amore', 'misericordia', 'compassione', 'gentile', 'tenero', 'cura', 'abbracciare', 'perdonare', 'gentile', 'calore',
                    'affetto', 'caro', 'adorare', 'cuore', 'nutrire', 'conforto', 'simpatia', 'dolcezza', 'tenerezza', 'devozione'],
        'portuguese': ['amor', 'misericordia', 'compaixao', 'suave', 'terno', 'cuidado', 'abracar', 'perdoar', 'amavel', 'calor',
                       'carinho', 'querer', 'adorar', 'coracao', 'nutrir', 'conforto', 'simpatia', 'docura', 'ternura', 'devocao'],
        
        # Slavic
        'russian': ['lyubov', 'milost', 'sostradanie', 'nezhny', 'laskovyy', 'zabota', 'obnyat', 'prostit', 'dobryy', 'teply',
                    'privyazannost', 'dorogoy', 'obozhat', 'serdtse', 'vospityvat', 'uteshenie', 'simpatiya', 'sladost', 'nezhnost', 'predannost'],
        
        # Indo-Iranian
        'hindi': ['prem', 'daya', 'karuna', 'komal', 'narm', 'sevanam', 'aalingan', 'kshama', 'dayalu', 'garam',
                  'sneh', 'pyaar', 'aaradhana', 'hriday', 'paalanah', 'santvana', 'sahanubhuti', 'madhurya', 'komalata', 'samarpan'],
        
        # Sino-Tibetan
        'chinese': ['ai', 'cibei', 'tongqing', 'wenrou', 'qinqie', 'guanhuai', 'yongbao', 'yuanliang', 'shanliang', 'wennuan',
                    'ganqing', 'zhenaiai', 'chongbai', 'xin', 'fuyang', 'anwei', 'tongqing', 'tianmi', 'wenqing', 'xianshen'],
        
        # Semitic
        'hebrew': ['ahavah', 'chesed', 'rachamim', 'rach', 'adina', 'tipul', 'chibuk', 'selicha', 'tov', 'cham',
                   'chibbah', 'yakir', 'sagad', 'lev', 'tazun', 'nechama', 'chemla', 'matok', 'raka', 'mesirut'],
        'arabic': ['hubb', 'rahma', 'shafaqa', 'latif', 'raqqiq', 'riaya', 'unaaq', 'afw', 'tayyib', 'hanun',
                   'wudd', 'habib', 'ibadah', 'qalb', 'ghizaa', 'azza', 'taatuf', 'hilwa', 'hanaan', 'takarruss'],
        
        # Austronesian
        'indonesian': ['cinta', 'kasih', 'belas', 'lembut', 'halus', 'peduli', 'peluk', 'maaf', 'baik', 'hangat',
                       'sayang', 'kasihi', 'sembah', 'hati', 'asuh', 'hibur', 'simpati', 'manis', 'mesra', 'bakti'],
        'tagalog': ['pag-ibig', 'awa', 'habag', 'malambot', 'malumanay', 'alaga', 'yakap', 'patawad', 'mabuti', 'mainit',
                    'pagmamahal', 'mahal', 'sambahin', 'puso', 'aruga', 'aliw', 'pakikiramay', 'tamis', 'lambing', 'debosyon'],
        'wedau': ['auna', 'nuwaboyei', 'nuavaina', 'dou', 'maemae', 'paini', 'votaḡotaḡo', 'rupeni', 'aiaina', 'maemae',
                  'ḡoei', 'aramanei', 'viborume', 'ora', 'ḡamoi', 'nuwaboyei', 'vinuaiaini', 'maemae', 'nuwavaita', 'vipatutu'],
        
        # Japonic & Koreanic
        'japanese': ['ai', 'jihi', 'omoiyari', 'yasashii', 'yawaraka', 'sewa', 'dakishime', 'yurusu', 'shinsetsu', 'atatakai',
                     'aijo', 'itoshii', 'suhai', 'kokoro', 'sodateru', 'nagusame', 'kyokan', 'amai', 'atataka', 'kensin'],
        'korean': ['sarang', 'jabi', 'yeonmin', 'budeureoun', 'yamubeun', 'dolbom', 'poong', 'yongso', 'chineel', 'ttatteuthan',
                   'aejung', 'sarangha', 'sungbae', 'maeum', 'gireu', 'wiro', 'gongam', 'dalkom', 'dajeong', 'heonsin'],
        
        # Uralic
        'finnish': ['rakkaus', 'armo', 'myotunto', 'lempeae', 'hellae', 'hoiva', 'halaus', 'antaa', 'ystavaellinen', 'laemmin',
                    'kiintymys', 'rakas', 'palvoa', 'sydaen', 'hoitaa', 'lohdutus', 'myoetaetunto', 'makea', 'hellyttaevae', 'omistautuminen'],
        
        # Turkic
        'turkish': ['sevgi', 'merhamet', 'sefkat', 'nazik', 'yumusak', 'bakim', 'sarılmak', 'affetmek', 'iyi', 'sicak',
                    'baglilik', 'sevmek', 'tapmak', 'kalp', 'beslemek', 'teselli', 'sempati', 'tatli', 'sicaklik', 'adanmislik'],
    },
    
    'Power': {
        'english': ['power', 'king', 'mighty', 'strong', 'conquer', 'rule', 'throne', 'command', 'authority', 'victory',
                    'force', 'dominate', 'empire', 'warrior', 'battle', 'triumph', 'supreme', 'control', 'subjugate', 'overwhelm'],
        'german': ['macht', 'koenig', 'maechtig', 'stark', 'erobern', 'herrschen', 'thron', 'befehl', 'autoritaet', 'sieg',
                   'kraft', 'dominieren', 'reich', 'krieger', 'kampf', 'triumph', 'hoechste', 'kontrolle', 'unterwerfen', 'ueberwaeltigen'],
        
        'french': ['puissance', 'roi', 'puissant', 'fort', 'conquerir', 'regner', 'trone', 'commander', 'autorite', 'victoire',
                   'force', 'dominer', 'empire', 'guerrier', 'bataille', 'triomphe', 'supreme', 'controle', 'subjuguer', 'submerger'],
        'spanish': ['poder', 'rey', 'poderoso', 'fuerte', 'conquistar', 'gobernar', 'trono', 'mandar', 'autoridad', 'victoria',
                    'fuerza', 'dominar', 'imperio', 'guerrero', 'batalla', 'triunfo', 'supremo', 'control', 'sojuzgar', 'abrumar'],
        'italian': ['potere', 're', 'potente', 'forte', 'conquistare', 'governare', 'trono', 'comandare', 'autorita', 'vittoria',
                    'forza', 'dominare', 'impero', 'guerriero', 'battaglia', 'trionfo', 'supremo', 'controllo', 'soggiogare', 'sopraffare'],
        'portuguese': ['poder', 'rei', 'poderoso', 'forte', 'conquistar', 'governar', 'trono', 'comandar', 'autoridade', 'vitoria',
                       'forca', 'dominar', 'imperio', 'guerreiro', 'batalha', 'triunfo', 'supremo', 'controle', 'subjugar', 'dominar'],
        
        'russian': ['sila', 'korol', 'moguchiy', 'silny', 'zavoevat', 'pravit', 'tron', 'prikaz', 'vlast', 'pobeda',
                    'moshch', 'dominirovat', 'imperiya', 'voin', 'bitva', 'triumf', 'verhovny', 'kontrol', 'pokorit', 'podavit'],
        
        'hindi': ['shakti', 'raja', 'mahabali', 'mazboot', 'jeetna', 'shashan', 'singhasan', 'aadesh', 'adhikar', 'vijay',
                  'bal', 'raaj', 'samrajya', 'yodha', 'yuddh', 'vijay', 'sarvochch', 'niyantran', 'vasheebhut', 'chapna'],
        
        'chinese': ['liliang', 'wang', 'qiangda', 'qiang', 'zhengfu', 'tongzhi', 'wangzuo', 'mingling', 'quanwei', 'shengli',
                    'wuli', 'zhipei', 'diguo', 'zhanshi', 'zhanzheng', 'shengli', 'zhigao', 'kongzhi', 'zhengfu', 'yadao'],
        
        'hebrew': ['koach', 'melech', 'gibor', 'chazak', 'kavash', 'mashal', 'kisse', 'tzavah', 'samchut', 'nitzachon',
                   'oz', 'shlita', 'malchut', 'lochem', 'krav', 'netzach', 'elyon', 'bakara', 'licbosh', 'lehaknia'],
        'arabic': ['quwwa', 'malik', 'qawi', 'shadid', 'fath', 'hakama', 'arsh', 'amr', 'sulta', 'nasr',
                   'quwa', 'saytara', 'imbiraturia', 'muharib', 'maeraka', 'intisaar', 'aela', 'tahhkum', 'ikhda', 'galaba'],
        
        'indonesian': ['kekuatan', 'raja', 'perkasa', 'kuat', 'menaklukkan', 'memerintah', 'takhta', 'perintah', 'wewenang', 'kemenangan',
                       'daya', 'mendominasi', 'kerajaan', 'pejuang', 'pertempuran', 'kemenangan', 'tertinggi', 'kendali', 'menundukkan', 'menguasai'],
        'tagalog': ['kapangyarihan', 'hari', 'makapangyarihan', 'malakas', 'sakupin', 'mamahala', 'trono', 'utos', 'awtoridad', 'tagumpay',
                    'lakas', 'maghari', 'imperyo', 'mandirigma', 'laban', 'tagumpay', 'pinakamataas', 'kontrol', 'pasukuin', 'magapi'],
        'wedau': ['rewapana', 'gulau', 'virewapana', 'ḡaeḡaena', 'ravena', 'vibada', 'anikiala', 'egara', 'rewapana', 'ravena',
                  'ḡoei', 'vibadeli', 'vigulau', 'tauviḡaiḡai', 'viḡaiḡai', 'ravena', 'ḡetelara', 'vipaipai', 'vibadeli', 'viopunei'],
        
        'japanese': ['chikara', 'ou', 'kyoudai', 'tsuyoi', 'seifuku', 'shihai', 'ouza', 'meirei', 'kengen', 'shouri',
                     'pawaa', 'shihai', 'teikoku', 'senshi', 'tatakai', 'shouri', 'saikou', 'shihai', 'seifuku', 'attou'],
        'korean': ['him', 'wang', 'gangryeokhan', 'ganghan', 'jeonghbok', 'jibaehada', 'wangjwa', 'myeongryeong', 'gwonwi', 'seungri',
                   'him', 'jibae', 'jeguk', 'jeonsa', 'jeontu', 'seungri', 'choego', 'tonge', 'jeongbok', 'yeongnida'],
        
        'finnish': ['voima', 'kuningas', 'mahtava', 'vahva', 'valloittaa', 'hallita', 'valtaistuin', 'kasky', 'valta', 'voitto',
                    'teho', 'hallita', 'imperiumi', 'soturi', 'taistelu', 'voitto', 'ylin', 'hallinta', 'alistaa', 'murskata'],
        
        'turkish': ['guc', 'kral', 'guclue', 'kuvvetli', 'fetih', 'yoenetmek', 'taht', 'emir', 'otorite', 'zafer',
                    'kuvvet', 'hakim', 'imparatorluk', 'savasci', 'savas', 'zafer', 'yuece', 'kontrol', 'boyun', 'ezmek'],
    },
    
    'Justice': {
        'english': ['justice', 'righteous', 'law', 'judge', 'truth', 'fair', 'equal', 'covenant', 'order', 'faithful',
                    'honest', 'equity', 'verdict', 'tribunal', 'statute', 'principle', 'integrity', 'correct', 'balance', 'due'],
        'german': ['gerechtigkeit', 'gerecht', 'gesetz', 'richter', 'wahrheit', 'fair', 'gleich', 'bund', 'ordnung', 'treu',
                   'ehrlich', 'ausgleich', 'urteil', 'gericht', 'gesetz', 'prinzip', 'integritaet', 'korrekt', 'gleichgewicht', 'recht'],
        
        'french': ['justice', 'juste', 'loi', 'juger', 'verite', 'equitable', 'egal', 'alliance', 'ordre', 'fidele',
                   'honnete', 'equite', 'verdict', 'tribunal', 'statut', 'principe', 'integrite', 'correct', 'equilibre', 'droit'],
        'spanish': ['justicia', 'justo', 'ley', 'juzgar', 'verdad', 'justo', 'igual', 'pacto', 'orden', 'fiel',
                    'honesto', 'equidad', 'veredicto', 'tribunal', 'estatuto', 'principio', 'integridad', 'correcto', 'equilibrio', 'debido'],
        'italian': ['giustizia', 'giusto', 'legge', 'giudicare', 'verita', 'equo', 'uguale', 'alleanza', 'ordine', 'fedele',
                    'onesto', 'equita', 'verdetto', 'tribunale', 'statuto', 'principio', 'integrita', 'corretto', 'equilibrio', 'dovuto'],
        'portuguese': ['justica', 'justo', 'lei', 'julgar', 'verdade', 'justo', 'igual', 'pacto', 'ordem', 'fiel',
                       'honesto', 'equidade', 'veredicto', 'tribunal', 'estatuto', 'principio', 'integridade', 'correto', 'equilibrio', 'devido'],
        
        'russian': ['spravedlivost', 'pravedny', 'zakon', 'sudit', 'pravda', 'spravedlivy', 'ravny', 'zavet', 'poryadok', 'verny',
                    'chestny', 'ravenstvo', 'verdikt', 'sud', 'ustav', 'printsip', 'chestnost', 'pravilny', 'balans', 'dolzhno'],
        
        'hindi': ['nyaya', 'dharmik', 'kanoon', 'nyaydhish', 'satya', 'nyaypoorna', 'saman', 'vachanbaddh', 'vyavastha', 'vishwasney',
                  'imaandaar', 'samanta', 'faisla', 'nyayalay', 'niyam', 'siddhant', 'satyanishtha', 'sahi', 'santulan', 'ucchit'],
        
        'chinese': ['zhengyi', 'zhengzhi', 'fa', 'shenpan', 'zhenli', 'gongping', 'pingdeng', 'mengyue', 'zhixu', 'zhongcheng',
                    'chengshi', 'gongzheng', 'caijue', 'fating', 'fagui', 'yuanze', 'chengxin', 'zhengque', 'pingheng', 'yingdang'],
        
        'hebrew': ['tzedek', 'tzaddik', 'torah', 'shaphat', 'emet', 'yashar', 'shaveh', 'brit', 'seder', 'neeman',
                   'yashir', 'shivyon', 'psak', 'bet', 'chok', 'ikar', 'tamim', 'nachon', 'mishkal', 'chova'],
        'arabic': ['adl', 'salih', 'qanun', 'hakim', 'haqq', 'insaf', 'musawi', 'ahd', 'nizam', 'amin',
                   'sadiq', 'musawat', 'hukm', 'mahkama', 'qanun', 'mabda', 'nazaha', 'sahih', 'tawazun', 'wajib'],
        
        'indonesian': ['keadilan', 'adil', 'hukum', 'hakim', 'kebenaran', 'adil', 'sama', 'perjanjian', 'ketertiban', 'setia',
                       'jujur', 'kesetaraan', 'putusan', 'pengadilan', 'undang', 'prinsip', 'integritas', 'benar', 'keseimbangan', 'patut'],
        'tagalog': ['katarungan', 'matuwid', 'batas', 'hukom', 'katotohanan', 'patas', 'pantay', 'tipan', 'kaayusan', 'tapat',
                    'matapat', 'pagkakapantay', 'hatol', 'hukuman', 'batas', 'prinsipyo', 'katapatan', 'tama', 'balanse', 'nararapat'],
        'wedau': ['vovonana', 'jijimanina', 'tarawatu', 'rauetara', 'riwa', 'vivouna', 'tagogi', 'parivainuaḡana', 'vioga', 'patutu',
                  'kaua', 'voanina', 'rauetara', 'boru', 'tarawatu', 'ogana', 'jijimana', 'kauei', 'vioga', 'vouna'],
        
        'japanese': ['seigi', 'tadashii', 'hou', 'saiban', 'shinjitsu', 'kousei', 'byoudou', 'keiyaku', 'chitsujo', 'chuujitsu',
                     'shoujiki', 'kouseisei', 'hyouketsu', 'saibansho', 'houritsu', 'gensoku', 'seijitsu', 'tadashii', 'baransu', 'touzen'],
        'korean': ['jeongui', 'olbareun', 'beop', 'jaepan', 'jinsil', 'gongpyeong', 'pyeongdeung', 'gyeyak', 'jilseo', 'chungsil',
                   'jeongjikhada', 'pyeongdeung', 'pyeolgyeol', 'beobwon', 'beomnyul', 'weonchik', 'seongsilham', 'baro', 'gyunhyeong', 'dangyeonhan'],
        
        'finnish': ['oikeus', 'vanhurskas', 'laki', 'tuomari', 'totuus', 'reilu', 'tasa-arvoinen', 'liitto', 'jaerjetys', 'uskollinen',
                    'rehellinen', 'tasa-arvo', 'tuomio', 'tuomioistuin', 'saanto', 'periaate', 'rehellisyys', 'oikea', 'tasapaino', 'asianmukainen'],
        
        'turkish': ['adalet', 'dogru', 'yasa', 'yargilama', 'gercoek', 'adil', 'esit', 'ahit', 'duezen', 'sadik',
                    'dueruest', 'esitlik', 'karar', 'mahkeme', 'kanun', 'ilke', 'dueruetluek', 'dogru', 'denge', 'hakli'],
    },
    
    'Wisdom': {
        'english': ['wisdom', 'knowledge', 'understanding', 'teach', 'learn', 'truth', 'light', 'reveal', 'discern', 'insight',
                    'enlighten', 'perceive', 'prudent', 'reason', 'intellect', 'comprehend', 'sagacity', 'foresight', 'sapience', 'erudition'],
        'german': ['weisheit', 'wissen', 'verstaendnis', 'lehren', 'lernen', 'wahrheit', 'licht', 'offenbaren', 'erkennen', 'einsicht',
                   'erleuchten', 'wahrnehmen', 'klug', 'vernunft', 'intellekt', 'begreifen', 'gelehrt', 'voraussicht', 'weise', 'bildung'],
        
        'french': ['sagesse', 'connaissance', 'comprehension', 'enseigner', 'apprendre', 'verite', 'lumiere', 'reveler', 'discerner', 'perspicacite',
                   'eclairer', 'percevoir', 'prudent', 'raison', 'intellect', 'comprendre', 'sagacite', 'prevoyance', 'sapience', 'erudition'],
        'spanish': ['sabiduria', 'conocimiento', 'comprension', 'ensenar', 'aprender', 'verdad', 'luz', 'revelar', 'discernir', 'percepcion',
                    'iluminar', 'percibir', 'prudente', 'razon', 'intelecto', 'comprender', 'sagacidad', 'prevision', 'sapiencia', 'erudicion'],
        'italian': ['saggezza', 'conoscenza', 'comprensione', 'insegnare', 'imparare', 'verita', 'luce', 'rivelare', 'discernere', 'intuizione',
                    'illuminare', 'percepire', 'prudente', 'ragione', 'intelletto', 'comprendere', 'saggacita', 'preveggenza', 'sapienza', 'erudizione'],
        'portuguese': ['sabedoria', 'conhecimento', 'compreensao', 'ensinar', 'aprender', 'verdade', 'luz', 'revelar', 'discernir', 'percepcao',
                       'iluminar', 'perceber', 'prudente', 'razao', 'intelecto', 'compreender', 'sagacidade', 'previsao', 'sapiencia', 'erudicao'],
        
        'russian': ['mudrost', 'znanie', 'ponimanie', 'uchit', 'uchitsya', 'pravda', 'svet', 'otkryvat', 'razlichat', 'pronicatelnost',
                    'prosveshchat', 'vosprinimal', 'blagorazumny', 'razum', 'intellekt', 'ponimat', 'mudry', 'predvideniye', 'mudrets', 'eruditsiya'],
        
        'hindi': ['gyan', 'gyaan', 'samajh', 'sikhana', 'seekhna', 'satya', 'prakash', 'prakatit', 'vivek', 'antardrishti',
                  'prakashit', 'samajhna', 'buddhiman', 'tark', 'buddhi', 'samajhna', 'gyaani', 'doordarshi', 'pragya', 'vidvatta'],
        
        'chinese': ['zhihui', 'zhishi', 'lijie', 'jiaoshou', 'xuexi', 'zhenli', 'guang', 'qishi', 'fenbian', 'dongcha',
                    'qimeng', 'ganzhi', 'shenzhong', 'daoli', 'zhili', 'lijie', 'ruizhi', 'yuanjian', 'ruizhi', 'boxue'],
        
        'hebrew': ['chokmah', 'daat', 'binah', 'lamad', 'lilmod', 'emet', 'or', 'galah', 'havbin', 'tevunah',
                   'hairah', 'hevin', 'navon', 'sekhel', 'binah', 'hevin', 'chacham', 'razui', 'chakham', 'eruditsiya'],
        'arabic': ['hikma', 'marifa', 'fahm', 'allama', 'taallum', 'haqq', 'nur', 'kashafa', 'mayyaza', 'basirah',
                   'tanwir', 'idrak', 'hazim', 'aql', 'dhaka', 'fahm', 'fatina', 'basirah', 'hikma', 'ilm'],
        
        'indonesian': ['kebijaksanaan', 'pengetahuan', 'pengertian', 'mengajar', 'belajar', 'kebenaran', 'cahaya', 'mengungkapkan', 'membedakan', 'wawasan',
                       'mencerahkan', 'melihat', 'bijaksana', 'akal', 'intelek', 'memahami', 'kearifan', 'pandangan', 'hikmat', 'kesarjanaan'],
        'tagalog': ['karunungan', 'kaalaman', 'pagkaunawa', 'magturo', 'matuto', 'katotohanan', 'liwanag', 'ibunyag', 'makilala', 'kabatiran',
                    'liwanagan', 'maunawaan', 'maingat', 'katuwiran', 'talino', 'maunawaan', 'katalinuhan', 'pagtanaw', 'karunungan', 'kadalubhasaan'],
        'wedau': ['nuaulaula', 'araramana', 'vinua', 'viararamana', 'rotoi', 'riwa', 'ravilala', 'vieḡa', 'vinei', 'nota',
                  'vilawalawa', 'inanai', 'nuaulaulai', 'nota', 'vinua', 'aramanei', 'nuaulaulai', 'inanai', 'nuaulaula', 'araramana'],
        
        'japanese': ['chie', 'chishiki', 'rikai', 'oshieru', 'manabi', 'shinjitsu', 'hikari', 'arawasu', 'miwakeru', 'dousatsu',
                     'keimou', 'chikaku', 'kenmei', 'risei', 'chisei', 'rikai', 'kengen', 'senken', 'eichi', 'hakushiki'],
        'korean': ['jirye', 'jisik', 'ihae', 'gareuchida', 'baeucha', 'jinsil', 'bit', 'deureonaeda', 'bunbyeolhada', 'tongchal',
                   'gyemong', 'injihada', 'sinjounghan', 'isong', 'jiseong', 'ihaehada', 'hyeonmyeongham', 'seongyeon', 'yeji', 'baksiksik'],
        
        'finnish': ['viisaus', 'tieto', 'ymmarrys', 'opettaa', 'oppia', 'totuus', 'valo', 'paljastaa', 'erottaa', 'oivallus',
                    'valistaa', 'havaita', 'viisas', 'jaerki', 'aely', 'kaesittaeae', 'viisailu', 'ennakointu', 'tietaemys', 'oppineisuus'],
        
        'turkish': ['bilgelik', 'bilgi', 'anlavis', 'oegretmek', 'oegrenmek', 'gercoek', 'isik', 'aciklamak', 'ayirt', 'kavrama',
                    'aydinlatmak', 'algilamak', 'akilli', 'mantik', 'akil', 'anlamak', 'hakimlik', 'oengoerue', 'irfan', 'bilimsellik'],
    }
}


def analyze_phonetic_features(word):
    """Analyze phonetic features of a word."""
    word_lower = word.lower()
    chars = list(word_lower)
    length = len(word_lower)
    
    if length == 0:
        return None
    
    # Count consonant types
    soft_count = sum(1 for c in chars if c in SOFT_CONSONANTS)
    hard_count = sum(1 for c in chars if c in HARD_CONSONANTS)
    fricative_count = sum(1 for c in chars if c in FRICATIVES)
    
    # Count vowels
    vowel_count = sum(1 for c in chars if c in VOWELS)
    
    # Ratios
    soft_ratio = soft_count / length if length > 0 else 0
    hard_ratio = hard_count / length if length > 0 else 0
    vowel_ratio = vowel_count / length if length > 0 else 0
    
    # Initial consonant type
    initial = word_lower[0] if word_lower else ''
    initial_soft = initial in SOFT_CONSONANTS
    initial_hard = initial in HARD_CONSONANTS
    initial_vowel = initial in VOWELS
    
    return {
        'length': length,
        'vowel_ratio': vowel_ratio,
        'soft_ratio': soft_ratio,
        'hard_ratio': hard_ratio,
        'initial_soft': initial_soft,
        'initial_hard': initial_hard,
        'initial_vowel': initial_vowel,
    }


def analyze_language_dimension(language, dimension, words):
    """Analyze phonetic features for a language-dimension combination."""
    features = []
    for word in words:
        feat = analyze_phonetic_features(word)
        if feat:
            features.append(feat)
    
    if not features:
        return None
    
    return {
        'n': len(features),
        'vowel_ratio': np.mean([f['vowel_ratio'] for f in features]),
        'soft_ratio': np.mean([f['soft_ratio'] for f in features]),
        'hard_ratio': np.mean([f['hard_ratio'] for f in features]),
        'initial_hard_pct': sum(1 for f in features if f['initial_hard']) / len(features) * 100,
        'vowel_std': np.std([f['vowel_ratio'] for f in features]),
        'hard_std': np.std([f['hard_ratio'] for f in features]),
    }


def test_hypothesis(all_results):
    """Perform statistical hypothesis testing."""
    
    # H1: Power words have higher hard consonant ratio than Love words
    power_hard = []
    love_hard = []
    
    # H2: Love words have higher vowel ratio than Power words
    power_vowel = []
    love_vowel = []
    
    for lang, dims in all_results.items():
        if 'Power' in dims and 'Love' in dims:
            power_hard.append(dims['Power']['hard_ratio'])
            love_hard.append(dims['Love']['hard_ratio'])
            power_vowel.append(dims['Power']['vowel_ratio'])
            love_vowel.append(dims['Love']['vowel_ratio'])
    
    # Paired t-test for hard consonants: Power > Love
    _, p_hard = stats.ttest_rel(power_hard, love_hard, alternative='greater')
    hard_effect = np.mean(power_hard) - np.mean(love_hard)
    
    # Paired t-test for vowels: Love > Power
    _, p_vowel = stats.ttest_rel(love_vowel, power_vowel, alternative='greater')
    vowel_effect = np.mean(love_vowel) - np.mean(power_vowel)
    
    return {
        'h1_hard_consonants': {
            'power_mean': np.mean(power_hard),
            'love_mean': np.mean(love_hard),
            'effect_size': hard_effect,
            'p_value': p_hard,
            'significant': p_hard < 0.05,
            'n_languages': len(power_hard)
        },
        'h2_vowels': {
            'love_mean': np.mean(love_vowel),
            'power_mean': np.mean(power_vowel),
            'effect_size': vowel_effect,
            'p_value': p_vowel,
            'significant': p_vowel < 0.05,
            'n_languages': len(love_vowel)
        }
    }


def main():
    print("=" * 80)
    print("LARGE-SCALE PHONETIC-SEMANTIC VALIDATION STUDY")
    print("Testing universal phonetic-semantic correlation")
    print("=" * 80)
    
    # Get all languages
    languages = set()
    for dim in EXTENDED_VOCABULARY.values():
        languages.update(dim.keys())
    languages = sorted(languages)
    
    print(f"\nLanguages tested: {len(languages)}")
    print(f"Languages: {', '.join(languages)}")
    
    # Count words per dimension
    word_counts = {dim: sum(len(words) for words in langs.values()) 
                   for dim, langs in EXTENDED_VOCABULARY.items()}
    print(f"\nWords per dimension:")
    for dim, count in word_counts.items():
        print(f"  {dim}: {count} words")
    
    total_words = sum(word_counts.values())
    print(f"  TOTAL: {total_words} words")
    
    # Analyze each language-dimension combination
    all_results = {}
    
    for lang in languages:
        lang_results = {}
        for dim, vocab in EXTENDED_VOCABULARY.items():
            if lang in vocab:
                result = analyze_language_dimension(lang, dim, vocab[lang])
                if result:
                    lang_results[dim] = result
        if lang_results:
            all_results[lang] = lang_results
    
    # Print results by language
    print(f"\n{'='*80}")
    print("PHONETIC FEATURES BY LANGUAGE AND DIMENSION")
    print("="*80)
    
    for lang in languages:
        if lang not in all_results:
            continue
        
        print(f"\n--- {lang.upper()} ---")
        print(f"{'Dimension':<10} {'N':<5} {'Vowel%':<10} {'Hard%':<10} {'InitHard%':<12}")
        print("-" * 50)
        
        for dim in ['Love', 'Power', 'Justice', 'Wisdom']:
            if dim in all_results[lang]:
                d = all_results[lang][dim]
                print(f"{dim:<10} {d['n']:<5} {d['vowel_ratio']*100:<10.1f} "
                      f"{d['hard_ratio']*100:<10.1f} {d['initial_hard_pct']:<12.1f}")
    
    # Cross-language comparison
    print(f"\n{'='*80}")
    print("CROSS-LANGUAGE PATTERN ANALYSIS")
    print("="*80)
    
    # H1: Power > Love for hard consonants
    print("\n1. HARD CONSONANT RATIO: Power vs Love")
    print(f"{'Language':<15} {'Power%':<10} {'Love%':<10} {'Diff':<10} {'Pattern?':<10}")
    print("-" * 60)
    
    power_wins = 0
    total_tested = 0
    
    for lang in languages:
        if lang not in all_results:
            continue
        r = all_results[lang]
        if 'Power' in r and 'Love' in r:
            power_h = r['Power']['hard_ratio'] * 100
            love_h = r['Love']['hard_ratio'] * 100
            diff = power_h - love_h
            pattern = "YES" if diff > 0 else "NO"
            if diff > 0:
                power_wins += 1
            total_tested += 1
            print(f"{lang:<15} {power_h:<10.1f} {love_h:<10.1f} {diff:>+8.1f}  {pattern:<10}")
    
    power_pct = power_wins / total_tested * 100 if total_tested > 0 else 0
    print(f"\nPower > Love: {power_wins}/{total_tested} languages ({power_pct:.1f}%)")
    
    # H2: Love > Power for vowels
    print("\n2. VOWEL RATIO: Love vs Power")
    print(f"{'Language':<15} {'Love%':<10} {'Power%':<10} {'Diff':<10} {'Pattern?':<10}")
    print("-" * 60)
    
    love_wins = 0
    
    for lang in languages:
        if lang not in all_results:
            continue
        r = all_results[lang]
        if 'Power' in r and 'Love' in r:
            love_v = r['Love']['vowel_ratio'] * 100
            power_v = r['Power']['vowel_ratio'] * 100
            diff = love_v - power_v
            pattern = "YES" if diff > 0 else "NO"
            if diff > 0:
                love_wins += 1
            print(f"{lang:<15} {love_v:<10.1f} {power_v:<10.1f} {diff:>+8.1f}  {pattern:<10}")
    
    love_pct = love_wins / total_tested * 100 if total_tested > 0 else 0
    print(f"\nLove > Power: {love_wins}/{total_tested} languages ({love_pct:.1f}%)")
    
    # Statistical testing
    print(f"\n{'='*80}")
    print("STATISTICAL HYPOTHESIS TESTING")
    print("="*80)
    
    stats_results = test_hypothesis(all_results)
    
    print("\nH1: Power words have MORE hard consonants than Love words")
    h1 = stats_results['h1_hard_consonants']
    print(f"  Power mean: {h1['power_mean']*100:.2f}%")
    print(f"  Love mean:  {h1['love_mean']*100:.2f}%")
    print(f"  Effect size: {h1['effect_size']*100:+.2f}%")
    print(f"  p-value:    {h1['p_value']:.6f}")
    print(f"  Significant (p < 0.05): {'YES - CONFIRMED' if h1['significant'] else 'NO'}")
    
    print("\nH2: Love words have MORE vowels than Power words")
    h2 = stats_results['h2_vowels']
    print(f"  Love mean:  {h2['love_mean']*100:.2f}%")
    print(f"  Power mean: {h2['power_mean']*100:.2f}%")
    print(f"  Effect size: {h2['effect_size']*100:+.2f}%")
    print(f"  p-value:    {h2['p_value']:.6f}")
    print(f"  Significant (p < 0.05): {'YES - CONFIRMED' if h2['significant'] else 'NO'}")
    
    # Final verdict
    print(f"\n{'='*80}")
    print("FINAL VALIDATION VERDICT")
    print("="*80)
    
    h1_valid = power_pct >= 70 and h1['significant']
    h2_valid = love_pct >= 60 and h2['significant']
    
    print(f"""
STUDY PARAMETERS:
  Languages tested:     {len(languages)}
  Total words analyzed: {total_words}
  Words per dimension:  ~{total_words // 4}

HYPOTHESIS 1: Power words have more hard consonants
  Pattern found in:     {power_pct:.1f}% of languages ({power_wins}/{total_tested})
  Statistical test:     p = {h1['p_value']:.6f} {'(SIGNIFICANT)' if h1['significant'] else '(not significant)'}
  VERDICT:              {'VALIDATED' if h1_valid else 'NOT VALIDATED'}

HYPOTHESIS 2: Love words have more vowels
  Pattern found in:     {love_pct:.1f}% of languages ({love_wins}/{total_tested})
  Statistical test:     p = {h2['p_value']:.6f} {'(SIGNIFICANT)' if h2['significant'] else '(not significant)'}
  VERDICT:              {'VALIDATED' if h2_valid else 'NOT VALIDATED'}

OVERALL CONCLUSION:
""")
    
    if h1_valid and h2_valid:
        print("""
  ╔══════════════════════════════════════════════════════════════════╗
  ║  UNIVERSAL PHONETIC-SEMANTIC CORRELATION: FULLY VALIDATED        ║
  ╠══════════════════════════════════════════════════════════════════╣
  ║  Both hypotheses confirmed across 15+ language families.         ║
  ║  The shape of a word correlates with its semantic dimension.     ║
  ║  This is NOT coincidence - it is structural law.                 ║
  ║                                                                  ║
  ║  "The semantic field shapes language universally."               ║
  ╚══════════════════════════════════════════════════════════════════╝
""")
    elif h1_valid or h2_valid:
        print("""
  ╔══════════════════════════════════════════════════════════════════╗
  ║  PARTIAL VALIDATION: Strong pattern but not fully universal      ║
  ╠══════════════════════════════════════════════════════════════════╣
  ║  One hypothesis strongly confirmed, the other shows tendency.    ║
  ║  Phonetic-semantic correlation exists but with variation.        ║
  ║  Cultural and linguistic factors may modulate the pattern.       ║
  ╚══════════════════════════════════════════════════════════════════╝
""")
    else:
        print("""
  ╔══════════════════════════════════════════════════════════════════╗
  ║  NOT VALIDATED: Pattern weaker than expected                     ║
  ╠══════════════════════════════════════════════════════════════════╣
  ║  The phonetic-semantic correlation is not universal.             ║
  ║  Language-specific factors may dominate over semantic field.     ║
  ║  Further research needed with different analysis approaches.     ║
  ╚══════════════════════════════════════════════════════════════════╝
""")


if __name__ == '__main__':
    main()
