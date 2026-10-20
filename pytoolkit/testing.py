from itertools import groupby, combinations


result2 = list(combinations('ABD',2))

result1 = [(key, list(group)) for key, group in groupby (['A','B','DEF'],len)]
print(result1, result2)

 


 