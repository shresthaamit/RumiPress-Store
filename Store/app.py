# # i = 0
# # while i < 5:
# #     print(i)
# #     i += 1
# #     if i == 3:
# #         break
# #     else:
# #         print(0)
# a=[1,2,3,4,5]
# for i in range(len(a), 1, -2):
#     print(a[i])
i = 8
for j in range(-10,i,10):
    print (j)

class test:
    def __init__(self,a="Hello World"):
        self.a=a
    def display(self):
        print(self.a)
obj=test()
obj.display()

string = "my name is x"
for i in string.split():
   print (i)