async def convert_name(name):
    names = {
        'afrodafro': 'Afrodafro',
        'itskevzii': 'ItsKevZii',
        'fjell': 'Fjell',
        'cxu': 'CXu',
        'hundur': 'Hundur',
        'zecryptic': 'ZeCryptic',
        'warrock': 'Warrock',
        'catbagasm': 'CatBagasm',
        '-gn': '-GN',
        'sebu': 'Sebu',
        'japron': 'JAPRON',
        'pierse': 'Pierse',
        'kjeks': 'kjeks',
        'gilmat': 'gilmat',
        'barkingmaddog': 'BarkingMadDog',
        'cocaine dog': 'Cocaine dog',
        'lksbackstab': 'LKSBackstab',
        'matboksen': 'Matboksen',
        'eiw': 'EiW',
        'utanishu': 'Utanishu',
        'njulsen': 'Njulsen',
        'surv': 'Surv',
        'kurean': 'Kurean',
        'melvr': 'Melvr',
        'duskyui': 'Duskyui',
        'yokespai': 'YokesPai',
        'espaas': 'Espaas',
        'markus': 'Markus',
        'rezk': 'Rezk',
        'pinguinzi': 'Pinguinzi',
        'fex': 'Fex',
        'whyv': 'WhyV',
        'vxb': 'VXB',
        'aksel': 'Aksel',
        'nicked16': 'nicked16',
        'jegler': 'Jegler',
        'levan': 'Levan',
        'stian': 'Stian',
        '-pc': '-PC',
        'weertypoi': 'Weertypoi',
        'krokou': 'Krokou',
        'monor': 'Monor',
        'razito': 'Razito',
        'myre': 'myre',
        'whatisdiss': 'Whatisdiss',
        'yuucliwood': 'Yuucliwood',
        'lgdaniel': 'LGDaniel',
        'villizen': 'Villizen',
        'hoohleno': 'hoohleno',
        'tobi': 'Tobi'
    }
    try:
        return names[name]
    except KeyError:
        return name


async def convert_score(key):
    scores = {
        '1': 10,
        '2': 9,
        '3': 8,
        '4': 7,
        '5': 6,
        '6': 5,
        '7': 4,
        '8': 3,
        '9': 2,
        '10': 1
    }
    return scores[key]
