import random
print("welcome to would you rather")
print("Choose wisely, or you may face consequences")


player_health = 500
rounds_played = 0
resource = 1000
shield = 500
maxrounds = 0

#List of consequences

events = [
    {
        "type":"combat",
        "description":"Enemy deployed 5 troops",
        "attack_damage": 50,
        "defend_damage": 0,
        "resource_reward_attack":75,
        "resource_reward_defend":40,
        "shield_regen":5
    },
    {  
        "type":"combat",
        "description":"Bomb goes off",
        "attack_damage": 200,
        "defend_damage": 20,
        "resource_reward_attack":0,
        "resource_reward_defend":-50,
        "shield_regen":10
    },
    {   "type":"combat",
        "description":"Sniper spotted",
        "attack_damage": 150,
        "defend_damage": 20,
        "resource_reward_attack":30,
        "resource_reward_defend":10,
        "shield_regen":30
    },
    {  "type":"combat",
        "description":"Drone strike inbound",
        "attack_damage": 0,
        "defend_damage": 0,
        "resource_reward_attack":-500,
        "resource_reward_defend":-250,
        "shield_regen":0
    },
    
    {   "type":"combat",
        "description":"intercepted enemey supply",
        "attack_damage": 0,
        "defend_damage": 0,
        "resource_reward_attack":600,
        "resource_reward_defend":0,
        "shield_regen":60
    },
    {   "type":"shopkeeper",
        "description":"you see a shopkeeper",
        "shield_cost": 100,
        "shield_amount": 50,
        "health_cost":100,
        "health_amount":20,
        "skip_cost":40
    },
     {  "type":"merchant",
        "description":"you see a merchant",
        "shield_cost": 50,
        "shield_amount": 25,
        "health_cost":50,
        "health_amount":10,
        "skip_cost":80
    },
    {   "type":"shopkeeper",
        "description":"Command Center offers you some deals",
        "shield_cost": 500,
        "shield_amount": 750,
        "health_cost":500,
        "health_amount":500,
        "skip_cost":40
    },
]
while True:
    print("[1] Easy")
    print("[2] Medium")
    print("[3] Hard")
    print("[4] Endless")
    choiceM = input("what difficulty would you like? [1-4] >>>>")
    if choiceM == "1" or "2" or "3" or "4":
        if choiceM == "1":
            maxrounds = 10
            break
        elif choiceM == "2":
            maxrounds = 25
            break
        elif choiceM == "3":
            maxrounds = 50
            
            break
        elif choiceM == "4":
            maxrounds = 999999999999999999999999999999999999999
            break
    else:
        print("Choose 1-4")
        continue
        
    

while player_health > 0:

    rounds_played += 1
    event = random.choice(events)
    print(f"\n EVENT: {event['description']}") 
    print(f"health:{player_health}  shield:{shield}  resources:{resource}  rounds played:{rounds_played}")
    if event["type"] in("merchant","shopkeeper"):
        while True:
            print("What would you like to purchase?")
            print(f"[1] Buy shield (+{event['shield_amount']}) for (+{event['shield_cost']}) resources ")
            print(f"[2] Buy health (+{event['health_amount']}) for (+{event['health_cost']}) resources ")
            print(f"[3] Skip this round for (+{event['skip_cost']}) resources")
            print("[4] Leave and Continue")
            choice = input(">>>> ").strip()
            
            if choice == "1":
                if resource >= event["shield_cost"]:
                    resource -= event["shield_cost"]
                    shield += event["shield_amount"]
                    print(f'Shield increased by {event["shield_amount"]}')
                else:
                    print("!Not enough resources!!")
                print(f"health:{player_health}  shield:{shield}  resources:{resource}")
            
            elif choice == "2":
                if player_health < 500:
                    if resource >= event["health_cost"]:
                        resource -= event["health_cost"]
                        player_health += event["health_amount"]
                        if player_health >= 500:
                            player_health = 500
                        print(f'Health increased by {event["health_amount"]}')
                    else:
                        print("!Not enough resources!!")
                    print(f"health:{player_health}  shield:{shield}  resources:{resource}")
                else:
                    print("Max Health")
                    print(f"health:{player_health}  shield:{shield}  resources:{resource}")
            elif choice == "3":
                if resource >= event["skip_cost"]:
                    resource -= event["skip_cost"]
                    print("you pay to skip this round's danger")
                    rounds_played += 1
                    break   
                else:
                    print("!Not enough resources!!")
                print(f"health:{player_health}  shield:{shield}  resources:{resource}")
            elif choice == "4":
                print(" you leave the shop and move on")
                break
            else:
                print('Pick 1-4')
            
        continue

    choice = ""
    while choice not in ("a", "d"):
        choice = input("Do you choose to [a]ttack or [d]efend.\n").strip().lower()
        if choice not in ("a", "d"):
            print("invalid input! please enter 'a' for attack or 'd' for defend.\n")

    if choice == "a":
        raw_damage = event["attack_damage"]
        res_gain = event["resource_reward_attack"]
        print("you choosed to attack")
    else:
        raw_damage = event["defend_damage"]
        res_gain = event["resource_reward_defend"]
        regen = event["shield_regen"]
        shield += regen
        print(f" you chose to defend and reinforce your shield by {regen} points!")
    shield_absorbed = 0
    shield_absorbed = min(shield, raw_damage)
    shield -= shield_absorbed
    total_damage = raw_damage - shield_absorbed
    player_health -= total_damage
    resource += res_gain
    if rounds_played >= maxrounds:
        print("You Win!")
        break
if player_health <= 0:
    print("You Died 😭🙏💔🥀🥀🥀")
    

    

    
        



        
    