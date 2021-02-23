import pandas as pd
import numpy as np
def AaylaGear(tier): #self explanatory; take the function input, compare it to the list of options, then return a value
    if tier == 1:
        return "MK 1 TaggeCo Holo Lens\nMK 1 TaggeCo Holo Lens\nMK 1 Nubian Security Scanner\nMK 1 Loronar Power Cell\nMK 1 Neuro Saav Electrobinoculars\nMK 1 CEC Fusion Furnace"
    elif tier == 2:
        return "MK 1 Neuro Saav Electrobinoculars\nMK 1 Neuro Saav Electrobinoculars\nMK 1 Chiewab Hypo Syringe\nMK 2 Neuro Saav Electrobinoculars\nMK 2 Arakyd Droid Caller\nMK 1 Sienar Holo Projector"
    elif tier == 3:
        return "MK 2 sorosuub keypad\nMK 4 Blastech Weapon Mod\nMK 3 Nubian Security Scanner\nMK 4 Loronar Power Cell\nMK 1 Chedak Comlink\nMK 6 Fabritech Data Pad"
    elif tier == 4:
        return "MK 2 Merr Sonn Thermal Detonator\nMK 5 biotech implant\nMK 2 Merr Sonn Shield Generator\nMK 3 Chiewab Hypo Syringe\nMK 6 BAW Armor Mod\nMK 4 Nubian Security Scanner"
    elif tier == 5:
        return "MK 3 Nubian Security Scanner\nMK 4 Loronar Power Cell\nMK 6 Blastech Weapon Mod\nMK 6 BAW Armor Mod\nMK 4 Chiewab Hypo Syringe\nMK 4 Merr Sonn Thermal Detonator"
    elif tier == 6:
        return "MK 4 Fabritech Data Pad\nMK 7 Blastech Weapon Mod\nMK 3 Sienar Holo Projector\nMK 3 Sienar Holo Projector\nMK 5 Nubian Security Scanner\nMK 5 Nubian Design Tech"
    elif tier == 7:
        return "MK 4 Nubian Design Tech\nMK 7 Fabritech Data Pad\nMK 1 Zaltin Bacta Gel\nMK 3 Sienar Holo Projector\nMK 4 sorosuub keypad\nMK 6 Merr Sonn Shield Generator"
    elif tier == 8:
        return "MK 4 Nubian Security Scanner\nMK 5 Chiewab Hypo Syringe\nMK 8 TaggeCo Holo Lens\nMK 6 Chiewab Hypo Syringe\nMK 3 Czerka Stun Cuffs\nMK 5 CEC Fusion Furnace"
    elif tier == 9:
        return "MK 7 Loronar Power Cell\nMK 4 sorosuub keypad\nMK 7 TaggeCo Holo Lens\nMK 3 Carbanti Sensor Array\nMK 9 Blastech Weapon Mod\nMK 4 Chedak Comlink"
    elif tier == 10:
        return "MK 4 Arakyd Droid Caller\nMK 6 Merr Sonn Shield Generator\nMK 3 Carbanti Sensor Array\nMK 5 AKT Stun Gun\nMK 5 Merr Sonn Thermal Detonator\nMK 8 Biotech Implant"
    elif tier == 11:
        return "MK 9 Fabritech Data Pad\nMK 6 Merr Sonn Thermal Detonator\nMK 8 TaggeCo Holo Lens\nMK 4 Sienar Holo Projector\nMk 9 Fabritech Data Pad\nMk 5 Chedak Comlink"
    elif tier == 12:
        return "Mk 12 ArmaTek Armor Plating\nMk 12 ArmaTek Multi-tool\nMk 12 ArmaTek Cybernetics\nMk 12 ArmaTek Holo Lens\nMk 12 ArmaTek Stun Gun\nPower Cell Injector (Plasma) - Aayla Secura"

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