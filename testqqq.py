# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
df = pd.DataFrame({ 'A': ['A0', 'A1', 'A2', 'A3','A4'],
                     'B': ['B0', 'B1', 'B2', 'B3','B4'],
                     'C': ['C0', 'C1', 'C2', 'C3','C4'],
                     'D': ['D0', 'D1', 'D2', 'D3','D4']})
df.set_index('A', inplace=True)
print(df)
print(df.index.values)