import uuid
name = "test_name"
namespace = "test_namespace"
# name.split()
s= uuid.uuid1().__str__()
# s.  [0:22]

def createToken(find_id,lost_id):
	token=str(find_id)+hex(int(lost_id))[1:]
	s= uuid.uuid1().__str__().replace('-','')
	return token+s[0:(32-len(token))]

print createToken(120,'200')