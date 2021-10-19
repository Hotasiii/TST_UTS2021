import json
from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from Authentication.auth_bearer import JWTBearer
from Authentication.auth_handler import signJWT

with open("menu.json", "r") as read_file: 
    data = json.load(read_file)

with open("login_credential.json", "r") as read_file:
    LoginCredential = json.load(read_file)

app = FastAPI() 

@app.get('/')
def root():
    return{'Menu': 'Item'}

@app.get('/menu') 
async def read_all_menu(): 
    return data

@app.get('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags = ["posts"]) 
async def read_menu(item_id: int): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            return menu_item
    raise HTTPException(
        status_code=404, detail=f'Item not found'
        )

@app.post('/menu', dependencies=[Depends(JWTBearer())], tags = ["posts"])
async def post_menu(name:str):
    id = 1
    if(len(data["menu"]) > 0):
        id = data["menu"][len(data["menu"]) - 1]["id"] + 1
    new_data = {'id':id, 'name':name}
    data['menu'].append(dict(new_data))
    read_file.close()
    
    with open("menu.json", "w") as write_file: 
        json.dump(data,write_file, indent=4)
    write_file.close()

    return (new_data)
    raise HTTPException(
        status_code=500, detail=f'Internal Server Error'
        )

@app.put('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags = ["posts"]) 
async def update_menu(item_id: int, name:str): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            menu_item['name'] = name
            read_file.close()
            with open("menu.json", "w") as write_file: 
                json.dump(data,write_file, indent=4)
            write_file.close()

            return{"Message":"Data updated successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
        )

@app.delete('/menu/{item_id}', dependencies=[Depends(JWTBearer())], tags = ["posts"]) 
async def delete_menu(item_id: int): 
    for menu_item in data['menu']:
        if menu_item['id'] == item_id:
            data['menu'].remove(menu_item)
            read_file.close()
            with open("menu.json", "w") as write_file: 
                json.dump(data,write_file, indent=4)
            write_file.close()

            return{"Message":"Data deleted successfully"}
    raise HTTPException(
        status_code=404, detail=f'Item not found'
        )

@app.post('/users', tags=["user"])
async def create_user(username:str, email:str, password:str):

    new_login_credential = {'username': username, 'email': email, 'password': password}
    LoginCredential['login_credential'].append(dict(new_login_credential))
    read_file.close()

    with open("login_credential.jason", "w") as write_file:
        json.dump(LoginCredential, write_file, indent = 4)
    write_file.close()
    return(new_login_credential)

    raise HTTPException(
        status_code = 500, detail = f'Internal Server Error'
    )

def user_validation (username:str, password:str):
    for users in LoginCredential['login_credential']:
        if users['username'] == username and users['[password'] == password:
            return True
        return False

@app.post('/login/{username}', tags = ['user'])
async def login_user (username:str, password: str):
    if user_validation(username, password):
        user = LoginCredential['login_credential']
        return signJWT(user), {"Login successful!"}
    return {"error": "Login unsuccessful. Your Username or Password is incorrect."}