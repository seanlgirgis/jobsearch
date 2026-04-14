import json
try:
    d = json.load(open('data/source_of_truth.json', encoding='utf-8'))
    print('1. JSON is valid')
except Exception as e:
    print('1. JSON invalid:', e)

print('2. Citi bullets:', len(d['experiences'][0]['highlights']))

simplex = next((e for e in d.get('experiences',[]) if 'simplex' in e.get('company','').lower()), {})
humber = next((e for e in d.get('experiences',[]) if 'humber' in e.get('company','').lower()), {})
print('3. Exclude Simplex:', simplex.get('exclude_from_resume'))
print('3. Exclude Humber:', humber.get('exclude_from_resume'))

raw = open('data/source_of_truth.json', encoding='utf-8').read()
if 'â€"' in raw or 'â†\'' in raw:
    print('4. Error: Corruption marks remain.')
else:
    print('4. No corruption marks found')

print('5. Preferred title:', d.get('personal_info', {}).get('preferred_title'))

p = next((p for p in d.get('projects',[]) if 'Serverless' in p.get('name','')), {})
print('6. Project timeframe:', p.get('timeframe'))
