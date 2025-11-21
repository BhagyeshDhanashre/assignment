from pydantic import BaseModel

class post_data_validation(BaseModel):
    user : str
    post_title : str

class user_data_validation(BaseModel):
    user_name : str

class post_data_update_validation(BaseModel):
    user : str
    post_id : int
    post_title : str
    
class delete_post_data_validation(BaseModel):
    user : str
    post_id : int



    