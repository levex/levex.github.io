import random


chart = input("Code: ").split("@")
player_1_hits = chart[0].split("~")
player_2_hits = chart[1].split("~")
player_3_hits = chart[2].split("~")
player_4_hits = chart[3].split("~")
player_5_hits = chart[4].split("~")

attack_chart = [player_1_hits, player_2_hits, player_3_hits, player_4_hits, player_5_hits]

scale = int(chart[5])
bounce_odds = float(chart[6])
purple = int(chart[7])

slash_def_roll = 25916
stab_def_roll = 34276
crush_def_roll = 34276
range_def_roll = 65626
magic_def_roll = 28006

class rolls:
    def __init__(rolls, str_bns, acc_bns):
        rolls.str_bns = str_bns
        rolls.acc_bns = acc_bns
        rolls.att_lvl = 0

        rolls.shadow_max = 68
        rolls.shadow_acc = 81950

        rolls.zcb_max = 45
        rolls.zcb_acc = 32016


new_boots_shadow_no_ring = [68, 81950]
void_quiver_no_pot = [45, 32016]

TTT_Ultor = rolls(70, 50)
TOO_Ultor = rolls(66, 78)
OOO_Ultor = rolls(64, 88)
OOO_Bellator = rolls(58, 108)


gear_map = {
    "TOO - Ultor": TOO_Ultor,
    "TTT - Ultor": TTT_Ultor,
    "OOO - Ultor": OOO_Ultor,
    "OOO - Bellator": OOO_Bellator
}

player_1 = gear_map.get(chart[8])
player_1.att_lvl = int(chart[9])

player_2 = gear_map.get(chart[10])
player_2.att_lvl = int(chart[11])

player_3 = gear_map.get(chart[12])
player_3.att_lvl = int(chart[13])

player_4 = gear_map.get(chart[14])
player_4.att_lvl = int(chart[15])

player_5 = gear_map.get(chart[16])
player_5.att_lvl = int(chart[17])


team = [player_1, player_2, player_3, player_4, player_5]
burn_stack_limit = [0, 0, 0, 0, 0]
burn_ticks = [0, 0, 0, 0, 0]
bounce_check = [0, 0, 0, 0, 0]

# Misc functions
def acc_check(accuracy, defence_roll):
    return random.randint(0, accuracy) > random.randint(0, defence_roll)

def attack(player, attack):
    if attack == "S":
        if bounce_check[player] == 1:
            bounce_check[player] = 0
            return zcb(player, False)

        return scythe(player, False)

    if attack == "S!":
        return scythe(player, True)

    if attack == "C":
        return claw(player, False, True)

    if attack == "C!":
        return claw(player, True, True)

    if attack == "P":
        return claw(player, False, False)

    if attack == "P!":
        return claw(player, False, False)

    if attack == "B":
        return burning_claw(player, False, True)

    if attack == "B!":
        return burning_claw(player, True, True)

    if attack == "H":
        return chally(player, False, True)

    if attack == "H!":
        return chally(player, True, True)

    if attack == "N":
        return nox(player, False)

    if attack == "N!":
        return nox(player, True)

    if attack == "A":
        return aby_dagger(player, False)

    if attack == "A!":
        return aby_dagger(player, True)

    if attack == "T":
        return shadow(player)

    if attack == "Z":
        return zcb(player, True)

    if attack == "X" or " ":
        return 0

def thrall(x):
    ym = 0
    hit = 0
    while ym < x:
        hit += random.randint(0, 3)
        ym += 1
    return hit

# Melee hits
def scythe(player, horn):
    weapon_str = 75
    weapon_acc = 125

    max_hit = int(0.5 + (153 + 3) * ((team[player].str_bns + weapon_str + 64) / 640))

    eff_attack = int(team[player].att_lvl * 1.2) + 0 + 8
    accuracy = int(eff_attack * (team[player].acc_bns + weapon_acc + 64))
    def_roll = slash_def_roll

    hit = 0

    for splats in range(3):
        if acc_check(accuracy, def_roll) or horn:
            hit += max(1, random.randint(0, max_hit))
        horn = False
        max_hit = int(max_hit / 2)

    return hit

def claw(player, horn, spec):
    weapon_str = 56
    weapon_acc = 57

    max_hit = int(0.5 + (153 + 3) * ((team[player].str_bns + weapon_str + 64) / 640))

    eff_attack = int(team[player].att_lvl * 1.2) + 0 + 8
    accuracy = int(eff_attack * (team[player].acc_bns + weapon_acc + 64))
    def_roll = slash_def_roll

    hit = 0
    if spec:
        if acc_check(accuracy, def_roll):
            splat_1 = random.randint(int(max_hit / 2), (max_hit - 1))
            splat_2 = int(splat_1 / 2)
            splat_3 = int(splat_2 / 2)
            splat_4 = random.randint(splat_3, splat_3 + 1)
            hit = splat_1 + splat_2 + splat_3 + splat_4

        elif acc_check(accuracy, def_roll) or horn:
            splat_1 = 0
            splat_2 = random.randint(int(max_hit * 0.375), int(max_hit * 0.875))
            splat_3 = int(splat_2 / 2)
            splat_4 = random.randint(splat_3, splat_3 + 1)
            hit = splat_1 + splat_2 + splat_3 + splat_4

        elif acc_check(accuracy, def_roll):
            splat_1 = 0
            splat_2 = 0
            splat_3 = random.randint(int(max_hit * 0.25), int(max_hit * 0.75))
            splat_4 = random.randint(splat_3, splat_3 + 1)
            hit = splat_1 + splat_2 + splat_3 + splat_4

        elif acc_check(accuracy, def_roll):
            first = 0
            second = 0
            third = 0
            fourth = random.randint(int(max_hit * 0.25), int(max_hit * 1.25))
            hit = first + second + third + fourth

        elif random.randint(0, 1) == 1:
                hit += 2

    else:
        if acc_check(accuracy, def_roll):
            hit += max(1, random.randint(0, max_hit))

    return hit

def burning_claw(player, horn, spec):
    weapon_str = 32
    weapon_acc = 54

    max_hit = int(0.5 + (153 + 3) * ((team[player].str_bns + weapon_str + 64) / 640))

    eff_attack = int(team[player].att_lvl * 1.2) + 0 + 8
    accuracy = int(eff_attack * (team[player].acc_bns + weapon_acc + 64))
    def_roll = slash_def_roll

    hit = 0
    splats = 0
    burn_chance = 0
    burn_stacks = 0

    if spec:
        if acc_check(accuracy, def_roll):
            damage_roll = random.randint(int(max_hit * 0.75), int(max_hit * 1.75))
            hit += int(damage_roll * 0.5)
            hit += int(damage_roll * 0.25)
            hit += int(damage_roll * 0.25)
            splats = 3
            burn_chance = 0.15

        elif acc_check(accuracy, def_roll) or horn:
            damage_roll = random.randint(int(max_hit * 0.5), int(max_hit * 1.5))
            hit += int(damage_roll * 0.5) - 1
            hit += int(damage_roll * 0.5) - 1
            hit += 2
            splats = 2
            burn_chance = 0.30

        elif acc_check(accuracy, def_roll):
            damage_roll = random.randint(int(max_hit * 0.25), int(max_hit * 1.25))
            hit += damage_roll - 2
            hit += 1
            hit += 1
            splats = 1
            burn_chance = 0.45

        else:
            last_hit_splat = random.randint(0, 4)
            if last_hit_splat >= 3:
                hit += 2
            elif last_hit_splat >= 1:
                hit += 1

        for _ in range(splats):
            if random.random() < burn_chance:
                burn_stacks += 1

        burn_stack_limit[player] = min(5, burn_stack_limit[player])

        burn = max(min(5 - burn_stack_limit[player], burn_stacks) * (8 - burn_ticks[player]), 0)

        burn_stack_limit[player] += burn_stacks
        burn_ticks[player] += 1

        hit += burn

    return hit

def chally(player, horn, spec):
    weapon_str = 118
    weapon_acc = 110

    max_hit = int(0.5 + (153 + 3) * ((team[player].str_bns + weapon_str + 64) / 640))

    eff_attack = int(team[player].att_lvl * 1.2) + 0 + 8
    accuracy = int(eff_attack * (team[player].acc_bns + weapon_acc + 64))
    def_roll = slash_def_roll

    hit = 0

    if spec:
        bonus_damage = int(max_hit * 0.1)
        if acc_check(accuracy, def_roll) or horn:
            hit += max(1, random.randint(0, max_hit)) + bonus_damage

        if acc_check(int(accuracy * 0.75), def_roll):
            hit += max(1, random.randint(0, max_hit)) + bonus_damage

    else:
        if acc_check(accuracy, def_roll):
            hit += max(1, random.randint(0, max_hit))

    return hit

def nox(player, horn):
    weapon_str = 142
    weapon_acc = 132

    max_hit = int(0.5 + (153 + 3) * ((team[player].str_bns + weapon_str + 64) / 640))

    eff_attack = int(team[player].att_lvl * 1.2) + 0 + 8
    accuracy = int(eff_attack * (team[player].acc_bns + weapon_acc + 64))
    def_roll = slash_def_roll

    hit = 0

    if acc_check(accuracy, def_roll) or horn:
        hit += max(1, random.randint(0, max_hit))

    return hit

def aby_dagger(player, horn):
    weapon_str = 75
    weapon_acc = 40

    max_hit = int(0.5 + (153 + 3) * ((team[player].str_bns + weapon_str + 64) / 640))

    max_hit = int(max_hit * 0.85)

    eff_attack = int(team[player].att_lvl * 1.2) + 0 + 8
    accuracy = int(eff_attack * (team[player].acc_bns + weapon_acc + 64))
    def_roll = slash_def_roll

    hit = 0

    if acc_check(accuracy, def_roll) or horn:
        hit += max(1, random.randint(0, max_hit))
        hit += max(1, random.randint(0, max_hit))

    return hit


# Range hits
def zcb(player, spec):
    max_hit = team[player].zcb_max
    accuracy = team[player].zcb_acc
    def_roll = range_def_roll

    hit = 0

    if spec:
        if acc_check(accuracy * 2, def_roll):
            hit = 110

    else:
        if random.random() < 0.066:
            hit = 110

        elif acc_check(accuracy, def_roll):
            hit = max(1, random.randint(0, max_hit))

    return hit


# Mage hits
def shadow(player):
    max_hit = team[player].shadow_max
    accuracy = team[player].shadow_acc
    def_roll = magic_def_roll

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, max_hit))

    return hit

# Sim
def sim():
    scale_variables = {
        1: 2625,
        2: 2625,
        3: 2625,
        4: 3062,
        5: 3500,
    }

    full_hp = scale_variables.get(scale)

    max_hp = 35
    min_hp = 10
    start = 0
    kill_odds_list = []

    while start != int((full_hp * (min_hp / 100))):
        start = int(full_hp * (max_hp / 100))
        count = 0
        wins = 0
        fails = 0
        sims = 10000

        while count < sims:
            hp = start
            hp -= thrall(scale * 7)

            # Purple
            if purple == 1:
                hp -= random.randint(65, 75)

            # Bounce stuff
            bounce = False

            if random.random() < bounce_odds:
                bounce = True

            if bounce:
                bounced_player = random.randrange(scale)
                bounce_check[bounced_player] = 1

            # Attacks
            for player in range(scale):
                for hit in attack_chart[player]:
                    hp -= attack(player, hit)

            # Reset burn
            for i in range(scale):
                burn_ticks[i] = 0
                burn_stack_limit[i] = 0

            if hp < 1:
                wins += 1
            else:
                fails += 1
            count += 1

            odds = round((wins / sims) * 100, 2)

        kill_odds_list.append(odds)

        max_hp = round(max_hp - 0.5, 1)

    print()
    for item in kill_odds_list:
        print(item)

sim()