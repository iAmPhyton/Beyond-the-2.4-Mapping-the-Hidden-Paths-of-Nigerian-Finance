import pandas as pd 
survey = pd.read_spss('2023_survey.sav')
print(survey.head()) 

import pandas as pd 
survey = pd.read_spss('2023_survey.sav')
print(survey) 

#this finds any column with "age" in the name (case insensitive)
age_cols = [col for col in survey.columns if 'age' in col.lower()] 
print(age_cols) 

#only columns that are numbers
print(survey.select_dtypes(include=['int64', 'float64']))

print(list(survey.columns)) 

import plotly.graph_objects as go 
cols_survey = {
    'income': 'target_groups',      #griculture, trading
    'access': 'fas',         #banked, excluded
    'usage': 'saving_strand' #saved at bank, saved at home
}

survey_clean = survey.dropna(subset=[cols_survey['income'], cols_survey['access'], cols_survey['usage']])

#filtering small data points if necessary
survey_clean = survey_clean[survey_clean[cols_survey['income']] != 'Refused']

#data preparation for sankey
#flow 1: sector -> FAS (acess)
survey_flow1 = survey_clean.groupby([cols_survey['income'], cols_survey['access']]).size().reset_index(name='count')
survey_flow1.columns = ['source', 'target', 'count'] 

#flow 2: FAS (access) -> saving method
survey_flow2 = survey_clean.groupby([cols_survey['access'], cols_survey['usage']]).size().reset_index(name='count')
survey_flow2.columns = ['source', 'target', 'count'] 

#combining both flows
links = pd.concat([survey_flow1, survey_flow2], axis=0) 

#creating unique list of all labels (nodes) involved
unique_nodes = list(pd.concat([links['source'], links['target']]).unique())

#mapping labels to numbers
node_map = {label: i for i, 
            label in enumerate(unique_nodes)}
#transforming data to use the numbers
links['source_id'] = links['source'].map(node_map)
links['target_id'] = links['target'].map(node_map)

#visuals
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=30,
        thickness=29,
        line=dict(color='black', width=0.5),
        label=unique_nodes,
        color="teal"
    ),
    link=dict(
        source=links['source_id'],
        target=links['target_id'],
        value=links['count'],
        color='rgba(100, 100, 100, 0.2)'
        ) 
)])
fig.update_layout(
    title_text="The Financial Journey: Sector -> Access -> Savings Habit",
    font_size=12,
    height=800,
    margin=dict(l=50, r=50, t=50, b=50)
)

fig.show() 

#visuals 2
import seaborn as sns
#comparing livelihoods (x) against wealth (y)
x_col = 'target_groups'
y_col = 'wealthscore'

#visuals 2 (Violin plots)
import matplotlib.pyplot as plt 
plt.figure(figsize=(12, 6))
sns.violinplot(
    data=survey,
    x=x_col,
    y=y_col,
    palette="viridis",
    inner="quartile",
    linewidth=1.5
)
plt.title('Wealth Inequality by Livelyhood', fontsize=14, fontweight='bold')
plt.xlabel('Livelihood Group', fontsize=12)
plt.ylabel('Wealth Score', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show() 

#checking potential education columns
print("--- Column C1 ---")
print(survey['c1'].unique()[:10])

print("\n--- Column C5 ---")
print(survey['c5'].unique()[:10])

#checking region too (should be North West, South East)
print("\n--- Column Region ---")
print(survey['region'].unique()[:10])

#grouping by the mystery code (c4) to get the average wealth
print(survey.groupby('c1')['wealthscore'].mean().sort_values(ascending=False))

#creating a mapping dictionary
#converting the numbers to text
edu_map = {
    1.0: 'No Formal',
    2.0: 'Some Primary',
    3.0: 'Completed Primary',
    4.0: 'Some Secondary',
    5.0: 'Completed Secondary',
    6.0: 'OND/NCE',
    7.0: 'HND/BSc (Uni)',
    8.0: 'Post-Graduate', 
    9.0: 'Quranic Only',
    10.0: 'Vocational'
}
survey['is_banked_binary'] = survey['banked'].apply(lambda x: 1 if x == 1 else 0)

#visuals
#creating a new column with the text labels
survey['education_level'] = survey['c1'].map(edu_map)

#heatmap visual
#comparing region vs. education on "Banked"
heatmap_data = survey.groupby(['region', 'education_level'])['is_banked_binary'].mean().unstack()

#reordering columns Low -> High Education
col_order = ['No Formal', 'Completed Primary', 'Completed Secondary', 'OND/NCE', 'HND/BSc (Uni)']
#filtering only for the columns that actually exist
available_cols = [c for c in col_order if c in heatmap_data.columns]
heatmap_data = heatmap_data[available_cols]

plt.figure(figsize=(12, 6))
sns.heatmap(
    heatmap_data, 
    annot=True, 
    fmt=".0%", 
    cmap="RdYlGn",
    linewidths=.5,
    vmin=0, vmax=1
) 

plt.title('Banking Penetration: Does Location Matter More Than School?', fontsize=14)
plt.xlabel('Education Level')
plt.ylabel('Geopolitical Zone')
plt.show()

#checking gender and age
print("--- Gender (e6) ---")
print(survey['e6'].value_counts())

print("\n--- Age Group ---")
print(survey['agegroup'].value_counts())

#checking unique values to see if they are 1, 1.0, or "1"
print("--- RAW GENDER VALUES (c2b) ---")
print(survey['e6'].unique()[:10]) 

print("\n--- RAW AGE VALUES (c2a) ---")
print(survey['agegroup'].unique()[:20])

#looping through every single column to find the "Real" Age
possible_age_cols = []

for col in survey.columns:
    #checking if the column is numeric (numbers)
    if pd.api.types.is_numeric_dtype(survey[col]):
        #calculating basic stats
        col_min = survey[col].min()
        col_max = survey[col].max()
        col_mean = survey[col].mean()
        
        #LOGIC: Ages usually range from 15 to 100, with an average around 30-40
        if (col_min >= 10) and (col_max <= 50) and (10 < col_mean < 50):
            possible_age_cols.append(f"{col} (Range: {col_min}-{col_max}, Mean: {col_mean:.1f})")

print("--- FOUND THESE POTENTIAL AGE COLUMNS ---")
for c in possible_age_cols:
    print(c)
    
#checking what is inside 'e6' to be sure it's gender
print("\n--- CHECKING GENDER COLUMN (e6) ---")
print(survey['e6'].unique()[:10])

