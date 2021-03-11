import pandas as pd
import numpy as np

def join_gear_char(gear_csv, toon_csv):

    gear = pd.read_csv(gear_csv)
    names = pd.read_csv(toon_csv)    
    
    # in case the name is itself so that way we do not need to include it in the nickname file
    ident_names = [(i,i) for i in gear["TOON"].unique()]
    ident_df = pd.DataFrame(ident_names, columns=["TOON", "NICKNAME"])
    names = names.append(ident_df).reset_index(drop=True)
    gear = gear.merge(names, on="TOON", how="inner")
    return gear

def find_gear(df, tier):
    idx = df["LEVEL"] == tier
    if np.sum(idx) == 0: # Check if gear tier is found
        return f"No Gear found for Tier {tier}"
    else:
        toon = df[idx].iloc[0]
        gear = ""
        for key, value in toon.items():
            if "GEARSLOT" in key: # We only want to use gear columns
                gear += value.replace("-"," ").title() + "\n"
    return gear
