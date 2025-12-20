import random

min_walk = 39
max_walk = 100

if min_walk > max_walk:
    print("Error - min walk larger than max walk")
    quit()

class rolls:
    def __init__(player):
        player.bgs_max = 88
        player.bgs_acc = 89042
        player.scythe_max = 55
        player.scythe_acc = 44140
        player.pneck_max = 46
        player.pneck_acc = 36784
        player.bolt_max = 51
        player.bolt_acc = 33285 # Bolt rag not spec
        player.claw_max = 50
        player.claw_acc = 31737
        player.chally_max = 75
        player.chally_acc = 40587


loadout = rolls()

bgs = []
regen = []
down_hp = []
wins = []
fails = []
onepointone_wins = []
onepointone_fails = []
player_cooldown = [0, 0, 0, 0, 0]
player_spec = [0, 0, 0, 0, 0]

# Misc functions
def acc_check(accuracy, defence_roll):
    return random.randint(0, accuracy) > random.randint(0, defence_roll)

## WALK HITS
def walk_bgs(player):
    player_spec[player] -= 50
    player_cooldown[player] = 6

    max_hit = loadout.bgs_max
    accuracy = loadout.bgs_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (slash_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, max_hit))
        bgs.append(hit)

    return int(hit / 2)


def force_bgs(player, hit):
    player_spec[player] -= 50
    player_cooldown[player] = 6

    true_bgs = (hit * 2) + random.randint(0, 1)

    bgs.append(true_bgs)

    return hit


def walk_scythe(player):
    player_cooldown[player] = 5

    max_hit = loadout.scythe_max
    accuracy = loadout.scythe_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (slash_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += max(1, int(random.randint(0, max_hit) / 2))
    if acc_check(accuracy, def_roll):
        hit += max(1, int(random.randint(0, int(max_hit / 2)) / 2))
    if acc_check(accuracy, def_roll):
        hit += max(1, int(random.randint(0, int(max_hit / 4)) / 2))

    return hit


def pneck_scythe(player):
    player_cooldown[player] = 5

    max_hit = loadout.pneck_max
    accuracy = loadout.pneck_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (slash_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += max(1, int(random.randint(0, max_hit) / 2))
    if acc_check(accuracy, def_roll):
        hit += max(1, int(random.randint(0, int(max_hit / 2)) / 2))
    if acc_check(accuracy, def_roll):
        hit += max(1, int(random.randint(0, int(max_hit / 4)) / 2))

    return hit


def walk_bolt_rag(player):
    player_cooldown[player] = 5

    max_hit = loadout.bolt_max
    accuracy = loadout.bolt_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (range_def + 64)

    if random.random() < 0.066:
        hit = 55

    elif acc_check(accuracy, def_roll):
        hit = max(1, random.randint(0, max_hit))
    else:
        hit = 0

    return int(hit / 2)


### DOWN HITS
def scythe(player):
    player_cooldown[player] = 5

    max_hit = loadout.scythe_max
    accuracy = loadout.scythe_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (slash_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, max_hit))
    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, int(max_hit / 2)))
    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, int(max_hit / 4)))

    return hit


def zcb_spec(player):
    player_spec[player] -= 75
    player_cooldown[player] = 5

    accuracy = loadout.bolt_acc * 2
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (range_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += 110

    return hit


def claw(player):
    player_spec[player] -= 50
    player_cooldown[player] = 4

    max_hit = loadout.claw_max
    accuracy = loadout.claw_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (slash_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        splat_1 = random.randint(int(max_hit / 2), (max_hit - 1))
        splat_2 = int(splat_1 / 2)
        splat_3 = int(splat_2 / 2)
        splat_4 = random.randint(splat_3, splat_3 + 1)
        hit = splat_1 + splat_2 + splat_3 + splat_4

    elif acc_check(accuracy, def_roll):
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

    return hit


def chally(player):
    player_spec[player] -= 30
    player_cooldown[player] = 7

    bonus_dmg = int(loadout.chally_max * 0.1)
    max_hit = loadout.chally_max - bonus_dmg
    accuracy = loadout.chally_acc
    def_level = max(defence - sum(bgs), 0)
    def_roll = (def_level + 9) * (slash_def + 64)

    hit = 0

    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, max_hit)) + bonus_dmg

    if acc_check(accuracy, def_roll):
        hit += max(1, random.randint(0, max_hit)) + bonus_dmg

    return hit

down = 0

full_code = str(input("Code: "))

split_code = full_code.split(",")

scale = int(split_code[0])

mode = str(split_code[1])

if mode == "Reg":
    slash_def = 20
    range_def = 800
    defence = 100
    turn_cooldown = 32
    if scale == 5:
        base_hp = 2000
    elif scale == 4:
        base_hp = 1750
    else:
        base_hp = 1500

elif mode == "HMT":
    slash_def = 20
    range_def = 800
    defence = 100
    turn_cooldown = 16
    if scale == 5:
        base_hp = 2400
    elif scale == 4:
        base_hp = 2100
    else:
        base_hp = 1800

else:
    slash_def = 5
    range_def = 800
    defence = 80
    turn_cooldown = 32
    if scale == 5:
        base_hp = 1280
    elif scale == 4:
        base_hp = 1088
    elif scale == 3:
        base_hp = 864
    elif scale == 2:
        base_hp = 608
    else:
        base_hp = 320

back_up_bgs_on = int(split_code[2])

chally_percent = int(split_code[3])

chally_thresh = base_hp * (chally_percent * 0.01)

spec = split_code[4]
starting_specs = [int(spec.split()[0]), int(spec.split()[1]), int(spec.split()[2]), int(spec.split()[3]),
                  int(spec.split()[4])]

on_boss_delay = split_code[5]
down_delay = [int(on_boss_delay.split()[0]), int(on_boss_delay.split()[1]), int(on_boss_delay.split()[2]),
              int(on_boss_delay.split()[3]), int(on_boss_delay.split()[4])]

walk_hits = split_code[6].split()

p1_hits = walk_hits[0].split("~")
p2_hits = walk_hits[1].split("~")
p3_hits = walk_hits[2].split("~")
p4_hits = walk_hits[3].split("~")
p5_hits = walk_hits[4].split("~")

chart = [p1_hits, p2_hits, p3_hits, p4_hits, p5_hits]
scaled_chart = []

for i in range(0, scale):
    chart.append(chart[i])

print()
print("Scale: ", scale)
print("Mode: ", mode)
print()
print("Min walk:", max(min_walk, 39))
print("Max walk:", min(max_walk, 47))
print()


def walk():
    # turn_first = 31
    # down_first = 39
    # down_last = 47

    # turn_odds = 1/16
    # down_odds = 1/4

    tick = 0
    turn_timer = turn_cooldown - 1
    while 1:
        if random.randint(1, 16) == 1 and turn_timer == 0:
            tick += 5
            turn_timer += turn_cooldown - 4
        if random.randint(1, 4) == 4 and tick >= 39:
            return tick
        if tick >= 47:
            return tick

        tick += 1
        turn_timer = max(0, turn_timer - 1)


def walk_attack(attack, player):
    if attack == "S":
        return walk_scythe(player)

    if attack == "P":
        return pneck_scythe(player)

    if attack == "B":
        if sum(bgs) < 100 - back_up_bgs_on:
            return walk_bgs(player)
        else:
            return walk_scythe(player)

    if attack == "Z":
        return walk_bolt_rag(player)

    if attack == "T":
        return walk_bolt_rag(player)

    if attack == "x":
        return 0

    else:
        return force_bgs(player, int(attack))


S = "S"
P = "P"
B = "B"
Z = "Z"
T = "T"
l = "!"


def down_attack(player, down_time, hp):
    hit = ""

    if player_cooldown[player] == 0:

        if player_spec[player] == 105 or player_spec[player] == 75 or player_spec[player] == 125:
            hit = zcb_spec(player)

        elif player_spec[player] == 100 or player_spec[player] == 50 or player_spec[player] == 55 or player_spec[player] == 80 or player_spec[player] == 130:
            hit = claw(player)

        elif player_spec[player] == 30 and hp <= chally_thresh:
            hit = chally(player)

        elif player_spec[player] == 30 and down_time <= 5:
            hit = chally(player)

        else:
            if down_time > 0:
                hit = scythe(player)
            else:
                hit = walk_scythe(player)

    if hit == "":
        return 0
    else:
        return hit


def sim():
    timer = 1
    player = 0

    hp = base_hp

    down_tick = max(min(walk(), max_walk), min_walk)

    random.shuffle(scaled_chart)

    while timer != down_tick:

        tick = timer - 1
        hit = chart[player]

        if hit[tick] != "x":
            dmg = walk_attack(eval(hit[tick]), player)
            player_cooldown[player] = 5
        else:
            dmg = 0
        hp = hp - dmg

        player += 1

        if player >= scale:
            if timer % 5 == 0 and sum(bgs) != 0:
                new_defence = min(sum(bgs), 100) - 1

                bgs.clear()

                bgs.append(new_defence)

            player = 0
            timer += 1

            for i in range(0, scale):
                player_cooldown[i] = max(0, player_cooldown[i] - 1)

    for i in range(0, scale):
        player_spec[i] += starting_specs[i]

    down_percent = round((hp / base_hp) * 100, 2)

    down_hp.append(down_percent)

    def down_sim(timer, hp):

        down_time = 32

        for i in range(0, 5):
            player_cooldown[i] = max(down_delay[i], player_cooldown[i])

        while hp > 0:
            for i in range(0, scale):
                hp -= down_attack(i, down_time, hp)

            for i in range(0, 5):
                player_cooldown[i] = max(0, player_cooldown[i] - 1)

            timer += 1
            down_time -= 1

            if timer % 5 == 0 and sum(bgs) != 0:
                old_def = max(0, sum(bgs))

                new_defence = min(sum(bgs), 100) - 1

                bgs.clear()

                bgs.append(new_defence)

            if down_time == 0:
                bgs.clear()

        if down_time < 0:
            fails.append(1)
        else:
            wins.append(1)

        if down_time <= -5:
            onepointone_fails.append(1)
        else:
            onepointone_wins.append(1)

        for i in range(0, 5):
            player_cooldown[i] = 0

        timer += 3

        bgs.clear()

        for i in range(0, scale):
            player_spec[i] = 0

        return round(timer * 0.6, 2)

    return down_sim(timer, hp)

sims = 25_000

room_times = []

slowest_time = 0

for i in range(0, 100):
    room_times.append(slowest_time)
    slowest_time = round(slowest_time + 0.6, 1)

total = 0


for x in range(0, sims):
    room_times.append(sim())

avg = sum(room_times) / sims

avg_down = sum(down_hp) / sims

for count, elem in sorted(((e, room_times.count(e)) for e in set(room_times)), reverse=False):
    print('%s=%d,' % (count, elem - 1))

print("+")
print(sum(wins), "@", sum(fails), "@", round(avg, 2), "@", round(avg_down, 2), "@", sum(onepointone_wins), "@",
      sum(onepointone_fails))