import pandas as pd

def load_names(file):
    df = pd.read_excel(file)

    if "Name" not in df.columns:
        raise Exception("Excel must contain 'Name' column")

    names = df["Name"].dropna().tolist()
    
    # remove duplicates
    names = list(set(names))
    
    return names