from fastapi import FastAPI, HTTPException, status
from models import Pokemon


app = FastAPI()

pokemons = {
    1: {
        'nome': 'Charmander',
        'elemento': 'Fogo',
        'altura': 6
    },
    2: {
        'nome': 'Vaporeon',
        'elemento': 'Água',
        'altura': 1
    }
}

@app.get('/')
async def mensagem():
    return {"mensagem": "Deu Certo!"}

@app.get('/pokemon')
async def get_pokemons():
    return pokemons

@app.get('/pokemon/{pokemon_id}')
async def get_pokemons(pokemon_id: int):
    try:
        pokemon = pokemons[pokemon_id]
        return pokemon
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon não encontrado")
    
@app.post('/pokemon')
async def post_pokemon(pokemon: Pokemon):
    if pokemon.id not in pokemons:
        pokemons[pokemon.id] = pokemon
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um pokemon com esse id')
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info', reload=True)

