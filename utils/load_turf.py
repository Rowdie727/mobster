''' This script will read in the turf from turf.json and if that turf exists it will updata any values otherwise it will add that turf to the database and commit the changes'''

import json
from mobster import *
from mobster.models import *

# Open json file
with open('turf.json') as turf_file:
    # Load data
    turfs = json.load(turf_file)
    # Loop over items
    for turf in turfs['turf']:
        # Create item object from data
        #turf_obj = Turf(turf_name=turf['turf_name'], turf_image=turf['turf_image'], turf_cost=turf['turf_cost'], turf_sell=turf['turf_sell'], turf_income=turf['turf_income'], level_required=turf['level_required'])
        
        # Query database for item of the same name
        dbturf = Turf.query.filter_by(turf_name=turf['turf_name']).first()
        
        # If item exists in db update it, otherwise add it
        if turf['turf_name'] == dbturf.turf_name:
            dbturf.turf_image = turf['turf_image']
            dbturf.turf_cost = turf['turf_cost']
            dbturf.turf_sell = turf['turf_sell']
            dbturf.turf_income = turf['turf_income']
            dbturf.level_required = turf['level_required']
        #else:
            #db.session.add(turf_obj)  
            
        
    # Commit changes 
    db.session.commit()