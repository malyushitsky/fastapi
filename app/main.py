from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/', operation_id="root_get", summary='Root')
def root():
    return 'Succesfull connection'


@app.post('/post', operation_id="get_post_post_post", summary='Get Post')
def post():
    max_id = -1
    for i in post_db:
        if i.id > max_id:
            max_id = i.id
    ts = datetime.now().minute

    timestamp = Timestamp(id=max_id+1, timestamp=ts)
    post_db.append(timestamp)

    return post_db[-1]


@app.get('/dog', operation_id="get_dogs_dog_get", summary='Get Dogs')
def get_dogs(kind: DogType = None):
    dogs_lst = []
    if kind is None:
        for dog in dogs_db.values():
            dogs_lst.append(dog)
    else:
        for id, dog in dogs_db.items():
            if dog.kind.value == kind:
                dogs_lst.append(dogs_db[id])

    return dogs_lst


@app.post('/dog', response_model=Dog, operation_id="create_dog_dog_post", summary='Create Dog')
def create_dog(dog: Dog):
    pk = dog.pk
    max_id = -1
    for id, cur_dog in dogs_db.items():
        if id > max_id:
            max_id = id
        if cur_dog.pk == pk:
            raise HTTPException(status_code=409,
                                detail='The specified PK already exists.')

    dogs_db[max_id+1] = dog

    return dog


@app.get('/dog/{pk}', response_model=Dog, operation_id="get_dog_by_pk_dog_pk_get", summary='Get Dog By Pk')
def get_dog_pk(pk: int):
    dog = None
    for id, cur_dog in dogs_db.items():
        if cur_dog.pk == pk:
            dog = dogs_db[id]
            return dog

    if dog is None:
        raise HTTPException(status_code=410,
                            detail='The dog with specified PK is not exists.')


@app.patch('/dog/{pk}', response_model=Dog, operation_id="update_dog_dog_pk_patch", summary='Update Dog')
def update_dog_pk(pk: int, dog_upd: Dog):
    dog = None
    dog_id = None
    for id, cur_dog in dogs_db.items():
        if cur_dog.pk == pk:
            dog = dogs_db[id]
            dog_id = id

    if dog is None:
        raise HTTPException(status_code=410,
                            detail='The dog with specified PK is not exists.')
    else:
        dogs_db[dog_id] = dog_upd
        return dogs_db[dog_id]



