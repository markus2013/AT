class GetLen:
    def __getitem__(self, index):
        return len(index)
    
gettor = GetLen()
print (gettor[1,2])
print (gettor[1,2,3])
