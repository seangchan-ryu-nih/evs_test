import requests

EVSREST_V1_URL = 'https://evsrestapi.nci.nih.gov/evsrestapi/api/v1/ctrp/concept/'


def get_new_subtype_set():
    url = f"{EVSREST_V1_URL}C175325/inverseassociations" 
    response = requests.get(url)
    subtype_set = {x['relatedConceptCode'] for x in response.json()}
    return subtype_set

def get_new_maintype_set():
    url = f"{EVSREST_V1_URL}C175324/inverseassociations" 
    response = requests.get(url)
    maintype_set = {x['relatedConceptCode'] for x in response.json()}
    return maintype_set

def _construct_type_map(cpaths, maintype_set, maintype_map):
    subtype_path = []
    maintypes = set()

    for data in cpaths:
        concepts = data['concepts']
        for i, concept in enumerate(concepts):
            c_code = concept['code']
            if c_code in maintype_set:
                subtype_path.append(concepts[:i+1])
                maintypes.add(c_code)
                maintype_map[c_code].add(concepts[0]['code'])
                break
    return maintypes, subtype_path

def find_relationship():
    subtypes = get_new_subtype_set()
    print(subtypes)
    maintypes = get_new_maintype_set()
    maintype_map = dict.fromkeys(maintypes, set())
    print(maintypes)
    subtype_map = {}
    
    for c_code in subtypes:
        url = f"{EVSREST_V1_URL}{c_code}/pathToRoot"
        response = requests.get(url)
        subtype_map[c_code] = (_construct_type_map(response.json()["paths"], maintypes, maintype_map))
    return subtype_map, maintype_map


if __name__ == '__main__':

    d_by_subtype, d_by_maintype = find_relationship()

    for sub_type, value in d_by_subtype.items():
        
        print(f"{sub_type} has maintypes {value[0]}")
        nodup = []
        for new_path in value[1]:
            data = []
            for d in new_path:
                data.append((d['label'], d['code']))
            if data not in nodup:
                nodup.append(data)

        for d in nodup:
            print(d)
        
        print()
    
    #for key, value in d_by_maintype.items():
        #print(f"{key}: {value}")
