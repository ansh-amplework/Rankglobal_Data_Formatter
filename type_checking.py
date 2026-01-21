import json
with open("finalized_companies.json","r", encoding="utf-8") as f1, open("seed_urls.json","r", encoding="utf-8") as f2:
    data = json.load(f1)
    urls_data = json.load(f2)
for item in data['companies']:
    url = item.get('company_name')
    for link in urls_data:
        if url.lower() in link.lower():
            urls_data.remove(link)
with open("seed_urls.json","w") as fp:
    json.dump(urls_data,fp,indent=4)
