#!/usr/bin/python2.6

import ldap
import sys

def index(req):
    somehtml = """
<html><body>
<form action="./python-test.py/show" method="get">
<h3>Super duper ldap query, CN:</h3>
<p><input type="text" name="cn">
<input type="submit" value="Submit"></p>
</form>
</body></html>
"""
    return somehtml

def show(req):
    username = str(req.form.getfirst('cn','0'))
    outputstring = """
<html><body>
<p><h3>Username:</h3> %s </p>
<p><h3>Email:</h3> %s </p>
<p><a href="http://afrolegs.com/python-test.py">Back</a></p>
</body></html>
""" % (username, retrieve_information(username))
    return outputstring

def retrieve_information(cn):
    static_options = {
        'ldap_uri': "ldap://masterldap.csee.wvu.edu",
        'people_dn': "ou=People,dc=csee,dc=wvu,dc=edu",
        }

    LDAP_OBJ = connect_to_ldap(static_options)

    result_set=[]

    try:
        result_id = LDAP_OBJ.search(static_options["people_dn"], ldap.SCOPE_SUBTREE, "cn=%s" % (cn), ["mailLocalAddress"])
        while 1:
            result_type, result_data = LDAP_OBJ.result(result_id, 0)
            if (result_data == []):
                break
            else:
                if result_type == ldap.RES_SEARCH_ENTRY:
                    result_set.append(result_data)
                    
        if len(result_set) == 0:
            print("User: %s does not exist in ldap." % (username))
            email = "ERROR user does not exist."
        else:
            for i in range(len(result_set)):
                for entry in result_set[i]:
                    email = entry[1]['mailLocalAddress'][0]
                    
    except ldap.LDAPError, e:
        email = "ERROR connecting to ldap."

    return email
    

def connect_to_ldap(static_configs):
    try:
        l = ldap.initialize(static_configs["ldap_uri"])
    except ldap.LDAPError, e:
        print("(!) Error occured while connecting to ldap")
        print(e)
        print("(!) BAILING!")
        sys.exit(1)
    return l

if __name__ == "__main__":
    print retrieve_information("abutcher")
