# DD1321
# Uppgift, Lab7: Pokédex
# Författare: Elias Albag och Joakim Ergon
# Datum: blbala

import json, re, random, sys



class Pokemon:
    def __init__(self, data, msg = None, sp_msg = None):
        self.name = data['name']['english']
        self.id = data['id']
        self.type = data['type']
        self.hp = data['base']['HP']
        self.attack = data['base']['Attack']
        self.defence = data['base']['Defense']
        self.sp_attack = data['base']['Sp_Attack']
        self.sp_defense = data['base']['Sp_Defense']
        self.speed = data['base']['Speed']
        self.level = 1  
        self.msg = msg 
        self.sp_msg = sp_msg
    
    def __repr__(self):
        return f' {self.name.capitalize()}, {self.id}'
    
    def __lt__(self, other):
        if self.hp == other.hp:
            return self.number < other.number
        return self.hp < other.hp

class Pokedex:
    def __init__(self):
        self.pokemon_dict = self.create_pokemon_objects()

    def create_pokemon_objects(self):
        pokemon_dict = self.load_pokedex()
        html_list = self.loadHTML()
        pokemon_objects = {}
        for pokemon in pokemon_dict.items():
           
            msgH, sp_msgH = self.randomizeMsg(html_list)
            pokemon_objects[pokemon[0]] = Pokemon(pokemon[1], msg = msgH, sp_msg = sp_msgH)
            
            
        return pokemon_objects
    

    def __getitem__(self, key):
        print(key)
        if key.isnumeric() or type(key) == int:
            keyString = str(key)
            if keyString not in self.pokemon_dict:
                raise KeyError(f"Key {key} not in pokedex")
            for value in self.pokemon_dict.values():
                if value.id == keyString:
                    return value
            return f'Key {key} not in pokedex'

        else:
            keyUpper = str(key).capitalize()
            if key not in self.pokemon_dict or keyUpper not in self.pokemon_dict :
                raise KeyError(f"Key {key} not in pokedex")
        
            return self.pokemon_dict[key]
    
  

    def __lt__(self, other):
        pass

    def __repr__(self):
        return f"{self.pokemon_dict}"

    def load_pokedex(self):
        with open("pokedex.json", "r") as fil:
            pokelist = json.load(fil)
    #print("i load_pokedex: första pokemon i pokedex är:\n\t", pokelist[0])

        pokedict = {}
        for k in pokelist:
            pokedict[ k["name"]["english"].lower() ] = k        
    

        return pokedict
        
    
    def loadHTML(self):
        #skapa ett reguljärt uttryck som matchar alla pokemons msg och sp_msg
        regUttryck = re.compile('(<td><small>)[a-zA-Z0-9, ]+(\.|!|\?)')

        with open("List_of_moves_mod.html", "r") as fil:
            lines = fil.readlines()
        output = []
        for line in lines:
            msg = regUttryck.match(line)
            if msg:
                msgNy = str(msg).replace("<td><small>", "")
                output.append(msgNy)

        return output


    def randomizeMsg(self, lista):
        #tar ut ett random meddelande till msg attribut
        msg = random.choice(lista)
        sp_msg = random.choice(lista)
        return msg, sp_msg


def check_pokemon(key):
    pokemon = Pokedex()
    return pokemon[key]