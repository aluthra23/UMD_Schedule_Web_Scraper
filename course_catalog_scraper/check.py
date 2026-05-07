import pandas as pd
import itertools

# Load latest re-uploaded course list
df = pd.read_csv("cs_courses.csv")

df['COURSE NUMBER'].to_csv('used_courses.csv', index=False)