import copy, random, pickle, os

g_savefile = "tildagame.pickle"

def playgame(pokedex):
    print("Welcome to the tilda flavored pokemon game")
    B, R = '\033[0;7m', '\033[0m'
    prompt = f"Choose a pokemon by entering its {B}pokemon name{R} or {B}pokedex id number{R}"
    prompt = prompt + f", or {B}load{R} a saved game.\n> " if os.path.isfile(g_savefile) else prompt + ".\n> "
    val = input(prompt)
    if val.upper().startswith("L"): pokemon = loadpokemon()
    else: pokemon = copy.copy(pokedex[val])
    while not val.lower().startswith("q"):
        print(pokemon, "smiles at you fondly")
        val = input(f"You may {B}fight{R} with other pokemon, {B}save{R} your pokemon or {B}quit{R}.\n> ")
        if val.upper().startswith("Q"): pass
        elif val.upper().startswith("S"): savepokemon(pokemon)
        elif val.upper().startswith("F"):
            winner = fight(pokemon, pokedex)
            if winner.id == pokemon.id:
                print("Your pokemon gains a level")
                pokemon.level += 1
            else:
                val = "quit"
    print("Game over")    

def fight(pokemon, pokedex):
    opponent = pokedex.random_opponent(pokemon)
    if opponent > pokemon: print(opponent, "looks huge and appears ready to fight. ")
    else: print(opponent, "looks small but appears ready to fight. ")
    p1 = copy.copy(pokemon)
    p2 = copy.copy(opponent)
    if (opponent.speed > pokemon.speed): p1, p2 = p2, p1
    for i in range(1, 100):
        if i % 3 == 0:
            print(p1.sp_msg.lower().replace("the user", str(p1)).replace("the target", str(p2)))
            dmg = pokedex.move(p1, p2, True) 
        else:
            print(p1.msg.lower().replace("the user", str(p1)).replace("the target", str(p2)))
            dmg = pokedex.move(p1, p2, False) 
        p2.hp -= dmg
        if p2.hp <= 0: p2.hp = 0
        print(f"   {p2} takes {dmg:.1f} damage and has {p2.hp:.1f} hit points left")
        if p2.hp < 1:
            print(f"{str(p2)} faints. {str(p1)} wins!")
            return p1
        p1, p2 = p2, p1

def savepokemon(pokemon):
    with open(g_savefile, "wb") as fil:
        pickle.dump(pokemon, fil)
        print(pokemon, " saved in", g_savefile)

def loadpokemon():
    with open(g_savefile, "rb") as fil:
        pokemon = pickle.load(fil)
        print(pokemon, "level", pokemon.level, "loaded")
        return pokemon
