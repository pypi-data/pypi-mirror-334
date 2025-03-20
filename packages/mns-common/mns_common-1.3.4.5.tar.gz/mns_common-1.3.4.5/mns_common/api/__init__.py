import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
import warnings
import pandas as pd

# 禁用 SettingWithCopyWarning
warnings.filterwarnings('ignore', category=pd.errors.SettingWithCopyWarning)
