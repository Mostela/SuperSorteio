from fastapi import FastAPI, Response

from database.memory import MemoryDb
from database.postgres import Game, ListNumber
from dto.user import ProfileGame

app = FastAPI()
database_memory = MemoryDb()


@app.get("/health", status_code=200)
async def healthcheck():
    Game.create_table(safe=True)
    ListNumber.create_table(safe=True)
    return {}


@app.post("/", status_code=201)
async def create_game(body: ProfileGame, response: Response):
    # Check numbers
    final_numbers = ()
    if 0 < len(body.numberList) <= 6:
        for numbers in body.numberList:
            check_number = 0 < numbers < 60
            if not check_number or numbers in final_numbers:
                response.status_code = 200
                return {'message': 'List numbers not ok'}
            final_numbers += (numbers,)

        # Check user
        if database_memory.get(body.guidUser) != body.keyGame:
            response.status_code = 400
            return {'message': 'KeyGame not found'}

        # Save user
        game = Game.create(guid_user=body.guidUser)
        for item in final_numbers:
            ListNumber.create(game=game, number_chosen=item)

        return body
    response.status_code = 200
    return {'message': 'Invalid list numbers'}
