''' This script will read in the missions from missions.json and if that mission exists it will updata any values otherwise it will add that mission to the database and commit the changes'''

import json
from mobster import *
from mobster.models import *

# Open json file
with open('missions.json') as mission_file:
    # Load data
    missions = json.load(mission_file)
    # Loop over missions
    for mission in missions['missions']:
        # Create mission object from data
        mission_obj = Missions(
            mission_region=mission['mission_region'],
            mission_name=mission['mission_name'],
            mission_image=mission['mission_image'],
            mission_tier=mission['mission_tier'],
            mission_required_mastery=mission['mission_required_mastery'],
            mission_required_energy=mission['mission_required_energy'],
            mission_required_item_id=mission['mission_required_item_id'],
            mission_required_mobc=mission['mission_required_mobc'],
            mission_reward_min_xp=mission['mission_reward_min_xp'],
            mission_reward_max_xp=mission['mission_reward_max_xp'],
            mission_reward_min_cash=mission['mission_reward_min_cash'],
            mission_reward_max_cash=mission['mission_reward_max_cash'],
            mission_reward_skill_points=mission['mission_reward_skill_points'],
            mission_reward_mobc=mission['mission_reward_mobc'],
            mission_reward_item_id=mission['mission_reward_item_id'],
            mission_reward_turf_id=mission['mission_reward_turf_id'],
            mission_mastery_reward_min_xp=mission['mission_mastery_reward_min_xp'],
            mission_mastery_reward_max_xp=mission['mission_mastery_reward_max_xp'],
            mission_mastery_reward_min_cash=mission['mission_mastery_reward_min_cash'],
            mission_mastery_reward_max_cash=mission['mission_mastery_reward_max_cash'],
            mission_mastery_reward_skill_points=mission['mission_mastery_reward_skill_points'],
            mission_mastery_reward_mobc=mission['mission_mastery_reward_mobc'],
            mission_mastery_reward_item_id=mission['mission_mastery_reward_item_id'],
            mission_mastery_reward_turf_id=mission['mission_mastery_reward_turf_id']
            )

        # Query database for mission of the same name
        # dbmission = Mission.query.filter_by(mission_name=mission['mission_name']).first()
        
        # If item exists in db update it, otherwise add it
        #if mission['mission_name'] == dbmission.mission_name:
            #dbmission.mission_image = mission['mission_image']
            
        #else:
        db.session.add(mission_obj)  
            
        
    # Commit changes 
    db.session.commit()
 