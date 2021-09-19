import json
from requests import get
data = get('https://ergast.com/api/f1/2021/constructors.json').text
data = json.loads(data)

# print(json.dumps(data, indent=4, sort_keys=True))
constructors_list = data['MRData']['ConstructorTable']['Constructors']
# print(constructors_list)
for i in constructors_list:
	print(f"{i['name']} ({i['nationality']})")
# fn, ln, code, driverId, number


# id = 'max_verstappen'
#
# for i in x:
# 	if i['Driver']['driverId'] == id:
# 		v = i
# 		break
#
# dd = v['Driver']
# fn = dd['givenName']
# ln = dd['familyName']
# number = dd['permanentNumber']
# dob = dd['dateOfBirth']
# nat = dd['nationality']
# dpos = v['position']
# dpts = v['points']
# dw = v['wins']
#
# cd = v['Constructors'][0]
# cnat = cd['nationality']
# cname = cd['name']
# print(fn, ln, number, dob, nat, dpos, dpts, dw, cnat, cname)

# print(x[0].keys())
# for i in x[0].values():
# 	print(i)