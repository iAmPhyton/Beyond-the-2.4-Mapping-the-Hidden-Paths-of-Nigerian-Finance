Barriers to Entry: A Livelihood Analysis of Nigerian Finance 🇳🇬

Project Overview
- Recent reports indicate that only 2.4% of Nigerians earn above ₦200k per month. But income is only half the story. The bigger question is access: Who gets into the formal financial system, and who gets left behind?
- This project analyzes the EFInA Access to Financial Services in Nigeria dataset to visualize the barriers to entry across livelihoods, geography, and education.

Key Insights & Visualizations:
1. The "Informal Leak" (Sankey Diagram)
Question: Do business owners bank formally?
Finding: Contrary to expectation, a large segment of "Business Owners" flows directly into Informal Savings (Ajo/Esusu) rather than formal bank savings. This suggests that the formal banking sector is failing to capture the liquidity of Nigeria's informal economy.

2. The Shape of Inequality (Violin Plot)
Question: What does wealth distribution actually look like?
Finding: By plotting Wealth Scores against Livelihoods, we see that "Farming" has a heavy bottom density (mass poverty), while "Formal Labor" shows a "guitar shape" indicating a healthier middle-class distribution.

3. The Education Equalizer (Heatmap)
Question: Is location destiny?
Finding: Data shows that Education trumps Geography. A university graduate in the North East (typically a lower-access region) has higher banking penetration than an uneducated resident in the South West.

Tools & Libraries:
- Python: Core analysis.
- Pandas: Data cleaning and SPSS (.sav) file handling.
- Plotly: Interactive flow diagrams (Sankey).
- Seaborn/Matplotlib: Statistical visualizations (Violins, Heatmaps).
- Pyreadstat: For parsing complex survey metadata.

Technical Challenges:
One of the major challenges in this analysis was data granularity. Initially, I intended to build a "Financial Demographic Pyramid," but I discovered that the `Age` variable in the public dataset was pre-binned into broad categories (15-17 vs 18+), making granular age analysis impossible.
- Solution: I pivoted the analysis to focus on Livelihood Clusters (`target_groups`) and Education Levels, where the data quality was high enough to support robust conclusions.

Data Source: EFInA Access to Financial Services in Nigeria Survey.

- Author Name: Chukwuemeka Eugene Obiyo
- Email: praise609@gmail.com
- Linkedin: www.linkedin.com/in/chukwuemekao/
