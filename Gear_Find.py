#empty until we start working on that command
import pandas as pd

def findGear(gearLocCsv, toon_csv):
    gearLoc = pd.read_csv(gearLocCsv)
    names = pd.read_csv(toon_csv)  
    ident_names = [(i,i) for i in gearLoc["ITEM"].unique()]
    ident_df = pd.DataFrame(ident_names, columns=["ITEM", "NICKNAME"])
    names = names.append(ident_df).reset_index(drop=True)
    gearLoc = gearLoc.merge(names, on="ITEM", how="inner")
    
    return gearLoc




#x = findGear('gear_locations.csv','nicknames.csv')

#print(x)