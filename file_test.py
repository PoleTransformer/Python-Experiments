import pickle

content = ['bob','zhao','louis','rossmann']
file = open('data','wb')
pickle.dump(content,file)
file.close()

file = open('data','rb')
file_unload = pickle.load(file)
print(file_unload)