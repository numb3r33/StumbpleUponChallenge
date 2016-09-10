LDA_DATASETS = [
    "max(all)+boilerplate*10", 
    "max(all)+meta-description*10", 
    "max(h1, title)",
    "max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description * 10 + meta-keywords * 10 + max(boilerplate, boilerpipe) * 5", 
     
]

DATASETS = [
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description * 10 + meta-keywords * 5',
    'max(all)+boilerplate*10',
    'max(all)+meta-description*10',
    'max(h1, title)',
    
    'title',
    'h1',
    'other',
    'meta-description',
    'meta-keywords',
    'h2',
    'h3',
    'img',
    'a',
    'boilerplate',
    'max(all)',

    'max(boilerplate, meta-description)', 
    'max(boilerplate, meta-description, meta-keywords)', 

    'max(all)+h1*5',
    'max(all)+title*5',
    'max(all)+other*5',
    'max(all)+meta-description*5',
    'max(all)+boilerplate*5',
    
    'max(all)+h1*10',
    'max(all)+title*10',
    'max(all)+other*10',

    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords + img + a +  boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords + img + a +  boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords + img + a +  boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords*5 + img + a  + boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords*10 + img + a  + boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords*10 + a  + boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords*10  + boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description + meta-keywords*10 + boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description * 10 + meta-keywords + boilerplate',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description * 10 + meta-keywords * 10 + boilerplate * 0.5 ',
    'max(title, h1) * 10 + max(title, h1, h2) + max(title, h1, h2, h3) + meta-description * 10 + meta-keywords * 10',
    'max(title, h1) * 10 + meta-description * 10 + meta-keywords * 10',
]