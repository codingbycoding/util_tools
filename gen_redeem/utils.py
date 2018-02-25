def testfun():
    print("abc")

    
def rc4(data, key):
    '''
    data:    data that to be encrypted or decrypted.
    key:     key to encrypt or decrypt. 
    '''
    
    #some parameters check here ...
    
    #if the data is a string, convert to hex format.
    if(type(data) is type("string")):
        tmpData=data
        data=[]
        for tmp in tmpData:
            data.append(ord(tmp))
            
    #if the key is a string, convert to hex format.
    if(type(key) is type("string")):
        tmpKey=key
        key=[]
        for tmp in tmpKey:
            key.append(ord(tmp))
            
    #the Key-Scheduling Algorithm
    x = 0
    box= list(range(256))
    for i in range(256):
        x = (x + box[i] + key[i % len(key)]) % 256
        box[i], box[x] = box[x], box[i]
        
    #the Pseudo-Random Generation Algorithm
    x = 0
    y = 0
    out = []
    for c in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(c ^ box[(box[x] + box[y]) % 256])

    return out
