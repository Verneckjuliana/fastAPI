from fastapi import FastAPI, HTTPException, status, Path, Header, Depends
from models import Pokemon
from typing import Optional, Any, List
from time import sleep

def fake_db():
    try:
        print("Abrindo Banco de dados")
        sleep(1)
    finally:
        print("Fechando Banco de dados")
        sleep(1)

app = FastAPI(title="API de Pokemons", version='0.0.1', description='API para Estudo do FastAPI')

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

@app.get('/pokemon', description='Retorna uma lista com Pokemons cadastrados ou uma lista vazia', response_model=List[Pokemon])
async def get_pokemons(db: Any = Depends(fake_db)):
    return pokemons

@app.get('/pokemon/{pokemon_id}')
async def get_pokemons(pokemon_id: int = Path(..., title='Pegar o Pokemon pelo ID', gt=0, lt=3, description='Selecionar o Pokemon pelo ID, onde o ID deve ser 1 ou 2')):
    try:
        pokemon = pokemons[pokemon_id]
        return pokemon
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pokemon não encontrado")
    
@app.post('/pokemon', status_code=status.HTTP_201_CREATED)
async def post_pokemon(pokemon: Optional [Pokemon] = None):
    if pokemon.id not in pokemons:
        next_id = len(pokemons) + 1
        pokemons[next_id] = pokemon
        del pokemon.id
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Já existe um pokemon com esse id')
    
@app.put('pokemon/{pokemon_id}')
async def put_pokemon(pokemon_id: int, pokemon: Pokemon):
    if pokemon_id in pokemons:
        pokemons[pokemon_id] = pokemon
        pokemon.id = pokemon_id
        return pokemon
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Não existe um pokemon com esse id')
    
@app.delete('/pokemon/{pokemon_id}', status_code=status.HTTP_204_NO_CONTENT)
async def del_pokemon(pokemon_id: int, pokemon: Pokemon):
    if pokemon_id in pokemons:
        del pokemons[pokemon_id]
        return{'message: f"Delete o Pokemon {pokemon_id}"'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe um pokemon com o id {pokemon_id}')
    
@app.get('/calculadora/soma')
async def calcular(n1:int, n2:int, n3: Optional[int] = None):
    if n3 == None: 
        soma = n1 + n2 
        return {'Resultado': soma}
    else:
        soma = n1 + n2 + n3
        return{'Resultado': soma}    
    
@app.get('/calculadora/subtracao')
async def calcular(n1:int, n2:int, n3: Optional[int] = None):
    if n3 == None: 
        subtracao = n1 - n2 
        return {'Resultado': subtracao}
    else:
        subtracao = n1 - n2 - n3
        return{'Resultado': subtracao}  
    
@app.get('/calculadora/multiplicacao')
async def calcular(n1:int, n2:int, n3: Optional[int] = None):
    if n3 == None: 
        multiplicacao = n1 * n2 
        return {'Resultado': multiplicacao}
    else:
        multiplicacao = n1 * n2 * n3
        return{'Resultado': multiplicacao}
    
@app.get('/calculadora/divisao')
async def calcular(n1:int, n2:int, n3: Optional[int] = None):
    if n3 == None: 
        divisao = n1 / n2 
        return {'Resultado': divisao}
    else:
        divisao = (n1 / n2) / n3
        return{'Resultado': divisao}
    
@app.get('/headerEx')
async def headerEx(juliana: str = Header(...,)):
    return {f'juliana': {juliana}}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='127.0.0.1', port=8000, log_level='info', reload=True)

