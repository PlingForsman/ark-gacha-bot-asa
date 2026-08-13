
poly_items = ["riot"]
metal_items = ["fabricated","pump","assault"]

recipes = {
    "auto_turret": {"metal": 140, "poly": 20, "elec": 70, "paste": 50},
    "heavy_turret": {"metal": 400, "poly": 50, "elec": 200, "paste": 150, "auto_turret": 1},
    "tek_turret": {"metal": 100, "poly": 50 , "elec": 100, "paste": 50},
}


def find_low_item():
    #hover over items and find the one with red text
    
    ...
    
def max_craftable(item:str, recipes=recipes):
    recipe   = recipes[item]
    