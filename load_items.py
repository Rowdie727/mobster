''' This script will read in the items from items.json and if that items exists it will updata any values otherwise it will add that item to the database and commit the changes'''

import json
from mobster import *
from mobster.models import *

# Open json file
with open('items.json') as item_file:
    # Load data
    items = json.load(item_file)
    # Loop over items
    for item in items['items']:
        # Create item object from data
        item_obj = Item(item_name=item['item_name'], item_image=item['item_image'], item_type=item['item_type'], item_attack=item['item_attack'], item_defense=item['item_defense'], item_cost=item['item_cost'], item_sell=item['item_sell'], item_decay=item['item_decay'], item_repair=item['item_repair'], level_required=item['level_required'])
        
        # Query database for item of the same name
        dbitem = Item.query.filter_by(item_name=item['item_name']).first()
        
        # If item exists in db update it, otherwise add it
        if item['item_name'] == dbitem.item_name:
            dbitem.item_image = item['item_image']
            dbitem.item_type = item['item_type']
            dbitem.item_attack = item['item_attack']
            dbitem.item_defense = item['item_defense']
            dbitem.item_cost = item['item_cost']
            dbitem.item_sell = item['item_sell']
            dbitem.item_decay = item['item_decay']
            dbitem.item_repair = item['item_repair']
            dbitem.level_required = item['level_required']
        else:
            db.session.add(item_obj)  
            
        
    # Commit changes 
    db.session.commit()
 

        
        
        