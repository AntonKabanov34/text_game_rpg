import random

# при инициативе за играком шанс победить от 20 до 70 % с четом равного кол во здоровья, при увеличении здоровья моба до 30 получам 50 на 50

#Player_характеристики
health = 12
strehgt = 1
dextary = 1
intelect = 1
armor = 0
damage_min = 1
damage_max = 3

#all_показатели_%
krit_damage_chance = 1
krit_miss = 1
dodge_chance = 15  #функция 25%+уклонение из функции соревнования Ловкостей
armor_miss_chance = 15  #шанс поглатить урон + шанс поглатить урон у брони игрока или противника
index_armor_miss = 0.02

#Mob_характеристики
mob_health = 10
mob_strehgt = 1
mob_dextary = 1
mob_intelect = 1
mob_armor = 0
mob_damage_min = 1
mob_damage_max = 3


#Время жизни моба
def time_life_mob(dm_min, dm_max, mob_arm, mob_health):
    """Рассчитывает время жизни моба на основе характеристик игрока"""
    #Сколько ударов потребуется игроку, без модификаторов, чтобы положить моба
    sr_player_attack = (dm_min + dm_max) / 2
    #sr_mob_damage = max(0, mob_arm - sr_player_attack)
    time_live = mob_health / sr_player_attack
    return (time_live)


def absorbed(str, arm, armor_miss_chanse, index_armor_miss):
    """Рассчитывает натуральное поглощения урона"""
    dise = random.randint(1, 100)
    if dise <= armor_miss_chanse:
        out = 100 * ((str + arm) * index_armor_miss) / (1 + ((str + arm) * index_armor_miss))
        return round(out)
    else:
        return 0
    #out = ((str/7)*(random.randint(1,100)/100))+((arm/3)*(random.randint(1,100)/100))


def dodge(chance, dex_zach, dex_attack) -> bool:
    """Ловкость защищающегося минус ловкость атакущего"""
    #print(f'Ловкость защ {dex_zach}')
    #print(f'Ловкость атак {dex_attack}')
    c = chance + (dex_attack - dex_zach)
    dice = random.randint(1, 100)
    #print (f'Шанс уклониться по итогам соревнования Ловкостей: {c}')
    #print(f'Кубик на уклонение бросил: {dice}')
    if dice <= c:
        return True
    else:
        return False


def kritical_damage(krit_dam) -> int:
    """Проверяем попали ли мы в крит! Если да, возвращаем 2"""
    dice = random.randint(1, 100)
    c = krit_dam
    if dice <= c:
        return 2
    else:
        return 1


def kritical_negative(krit_mis, dam) -> int:
    """Проверяем на неудачу, возвращаем урон или 0"""
    dice = random.randint(1, 100)
    c = krit_mis
    if dice <= c:
        return dam
    else:
        return 0


def attack_frame(name, dam_min, dam_max, str_attack, str_zash, arm_zash,
                 krit_mis, chance, dex_zach, dex_attack,
                 arm_chance_zash) -> int:
    """Возвращаеть натуральное число - минус ХП"""
    #((o+c)+(крит_атакующего) + (неудача защищающего)) - Поглощение (защищающего)%

    if dodge(chance, dex_zach, dex_attack) == True:
        print(f'\n{name} промахнулся\n')
        return 0
    else:
        dice_weapon = random.randint(dam_min, dam_max)
        print(f'{name} бросил кубик оружия на: {dice_weapon}')

        a_1 = (dice_weapon + str_attack)
        print(f'Атака и сила {name} равны: {a_1}')
        a_2 = kritical_damage(krit_damage_chance)
        print(f'Шанс критического урона {name} вернул: {a_2}')
        a_neg = kritical_negative(krit_mis, a_1)
        a_3 = (a_1 * a_2) + a_neg
        print(f'Критическая неудача вернула : {a_neg}')
        print(f'Урон {name} до поглащения равен: {a_3}')
        adsor = absorbed(str_zash, arm_zash, arm_chance_zash, index_armor_miss) #index_armor_miss глобал
        print(f'->Противник поглотил {adsor}% урона')
        absor_2 = round(a_3 * (adsor/100))
        print(f'Противник натурально поглотил урона: {absor_2}')
        a_4 = a_3 - absor_2
        print(f'{name} нанес урона: {round(a_4)}')
        print('\n__________________________________________\n')
        out = round(a_4)

        return out if out > 0 else 0


#player_attack_frame = attack_frame('Игрок',damage_min, damage_max, strehgt, mob_strehgt, mob_armor, krit_miss, dodge_chance, mob_dextary, dextary, armor_miss_chance)
#mob_attack_frame = attack_frame('Моб', mob_damage_min, mob_damage_max, mob_strehgt, strehgt, armor, krit_miss, dodge_chance, dextary, mob_dextary, armor_miss_chance)


def battle(health, mob_health):
    print('Старт БОЯ - НАЧИНАЕТ ИГРОК\n')
    print(f'Время жизни моба: {round(time_life_mob(damage_min, damage_max, mob_armor, mob_health))}')
    health = health
    mob_health = mob_health

    marker = 1
    while True:
        if mob_health < 0 or health < 0:
            break
        elif health > 0:
            print(f'РАУНД {marker}\n')
            print('НАЧАЛО РАУНДА:')
            print(f'--------->Здоровье игрока: {health}')
            print(f'------>Здоровье моба: {mob_health}')
            print('\n')
            player_attack_frame = attack_frame('ИГРОК', damage_min, damage_max,
                                               strehgt, mob_strehgt, mob_armor,
                                               krit_miss, dodge_chance,
                                               mob_dextary, dextary,
                                               armor_miss_chance)
            mob_health = mob_health - player_attack_frame
            if mob_health > 0:
                mob_attack_frame = attack_frame('МОБ', mob_damage_min, mob_damage_max,
                                                mob_strehgt, strehgt, armor, krit_miss,
                                                dodge_chance, dextary, mob_dextary,
                                                armor_miss_chance)
                
                health = health - mob_attack_frame
                marker = marker + 1
        
                print('\nКОНЕЦ РАУНДА:')
                print(f'--------->Здоровье игрока: {health}')
                print(f'------>Здоровье моба: {mob_health}')
                print('\n')
        
                print('-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/\n')

        else:
            break


#Сперва уклонение! Если ТРУ, то удар = 0
#print('__________________________________________________________________________')
#print(dodge(dodge_chance, dextary, mob_dextary))
#print('____________________________________')
#print(absorbed(strehgt, armor))
#print('ИГРОК АТАКУЕТ ПРОТИВНИКА')
#print(f'Игрок нанес мобу урон: {player_attack_frame}')
#print(absorbed(strehgt, armor))
#print(f'Моб нанес игроку урон: {mob_attack_frame}')

#print(f'Кол-во атак по мобу до смерти: {time_life_mob(damage_min, damage_max, mob_armor, mob_health)}')
battle(health, mob_health)
