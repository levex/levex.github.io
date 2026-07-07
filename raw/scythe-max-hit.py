import argparse
import math

# Scythe of Vitur: +75 strength; the other slots in a typical max melee
# setup add more, so let the total be overridden with --str-bonus.
SCYTHE_STR_BONUS = 75
AGGRESSIVE_STYLE_BONUS = 3


def max_hit(strength_level: int, prayer_multiplier: float,
            equipment_str_bonus: int = SCYTHE_STR_BONUS,
            style_bonus: int = AGGRESSIVE_STYLE_BONUS,
            slayer: bool = False, salve: bool = False) -> int:
    effective = math.floor(strength_level * prayer_multiplier) + style_bonus + 8
    base = math.floor(0.5 + effective * (equipment_str_bonus + 64) / 640)
    # Salve (e) and slayer helm don't stack; salve (e) is 6/5, slayer helm 7/6
    if salve:
        base = math.floor(base * 6 / 5)
    elif slayer:
        base = math.floor(base * 7 / 6)
    return base


def scythe_hits(base_max: int) -> tuple[int, int, int]:
    # vs 2x2+: two hits; vs 3x3+: all three
    return base_max, base_max // 2, base_max // 4


def main():
    parser = argparse.ArgumentParser(description="Scythe of Vitur max hit calculator")
    parser.add_argument("strength", type=int, help="strength level (after potions)")
    parser.add_argument("prayer", type=float,
                        help="prayer strength multiplier, e.g. 1.23 for Piety")
    parser.add_argument("--str-bonus", type=int, default=SCYTHE_STR_BONUS,
                        help=f"total equipment strength bonus (default {SCYTHE_STR_BONUS}, scythe only)")
    parser.add_argument("--style-bonus", type=int, default=AGGRESSIVE_STYLE_BONUS,
                        help="attack style bonus: 3 aggressive, 1 controlled, 0 accurate/defensive")
    parser.add_argument("--slayer", action="store_true",
                        help="wearing a slayer helm with an active task (7/6 max hit multiplier)")
    parser.add_argument("--salve", action="store_true",
                        help="wearing a salve amulet (e) vs undead (6/5 max hit multiplier, "
                             "does not stack with --slayer)")
    args = parser.parse_args()

    base = max_hit(args.strength, args.prayer, args.str_bonus, args.style_bonus,
                   slayer=args.slayer, salve=args.salve)
    h1, h2, h3 = scythe_hits(base)

    print(f"Base max hit: {h1}")
    print(f"Hits vs 1x1:  {h1}          (total {h1})")
    print(f"Hits vs 2x2:  {h1}+{h2}       (total {h1 + h2})")
    print(f"Hits vs 3x3+: {h1}+{h2}+{h3}    (total {h1 + h2 + h3})")


if __name__ == "__main__":
    main()
