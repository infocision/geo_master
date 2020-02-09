

# def longestCommonPrefix(a):
#     size = len(a)
#
#     # if size is 0, return empty string
#     if (size == 0):
#         return ""
#
#     if (size == 1):
#         return a[0]
#
#         # sort the array of strings
#     a.sort()
#
#     # find the minimum length from
#     # first and last string
#     end = min(len(a[0]), len(a[size - 1]))
#
#     # find the common prefix between
#     # the first and last string
#     i = 0
#     while (i < end and
#            a[0][i] == a[size - 1][i]):
#         i += 1
#
#     pre = a[0][0: i]
#     return pre
#
# input = ["apple", "ape", "april"]
# print(longestCommonPrefix(input))

# a=[1,2,3,4,8,6,6,9,7,8]
# lenth=0
# for i in a:
#     lenth=lenth+1
# print(lenth)
#
#
# a=['app','apple','apply']
# sml=a[0]
# for i in a:
#     if len(i)<len(sml):
#         sml=i
# ind=0
#
# for i,x in enumerate(sml):
#     for j in a:
#         if sml[i]==j[i]:
#             ind=i
#         else:
#             break
# print(sml[:ind+1])

# a=[1,2,3,4,8,6,6,9,7,8]
# a.sort()
# lst=[]
# ind= -1
# for i in a[0:len(a)//2]:
#     lst.append(a[ind])
#     lst.append(i)
#     ind=ind-1
# print(a)
#
# palin=435
# pal=1
# for i in range(1,palin):
#     if str(palin+i)==str(palin+1)[::-1]:
#         pal=palin+i
#         break
#     elif str(palin-i)==str(palin-1)[::-1]:
#         pal = palin-i
#         break
# print(pal)

lst=[[2,3,4],[2,1,7],[2,1]]
tpl=[]
print(lst.append(2))















