# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 22:09:25 2021

@author: fkvzl
"""

 
list1 = ['physics', 'chemistry', 1997, 2000]
list2 = [1, 2, 3, 4, 5, -6, -7 ]
l=[x for x in list2 if x<0]
print (sum(l))