from fastapi import FastAPI,HTTPException
from database import get_connection
import re
import models

app = FastAPI()

@app.post("/create/user")
def create(user: models.user_data_validation):

    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', user.user_name):
        raise HTTPException(status_code=400, detail="Invalid username. Only letters, numbers, and underscores allowed, and must start with a letter or underscore.")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS "{user.user_name}" (
            post_id SERIAL PRIMARY KEY,
            post_title VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Successfully created a new user"}

@app.post("/create/post")
def create_post(post : models.post_data_validation):

    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', post.user):
        raise HTTPException(status_code=400, detail="Invalid username. Only letters, numbers, and underscores allowed, and must start with a letter or underscore.")
    
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"insert into {post.user} (post_title) values(%s)",(post.post_title,))
    conn.commit()
    #post_data = cursor.execute(f"select * from {post.user} where")
    return "succesfully created a new post"



@app.get("/read/posts/{user}")
def read(user:str):

    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', user):
        raise HTTPException(status_code=400, detail="Invalid username. Only letters, numbers, and underscores allowed, and must start with a letter or underscore.")
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"select * from {user}")
    post_data = cursor.fetchall()
    #print(post_data)
    cursor.close()
    conn.close()
    
    return post_data

@app.post("/update")
def update(post: models.post_data_update_validation):
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', post.user):
        raise HTTPException(status_code=400, detail="Invalid username. Only letters, numbers, and underscores allowed, and must start with a letter or underscore.")
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"update {post.user} set post_title=%s where post_id=%s",(post.post_title,post.post_id),)
    conn.commit()
    rows = cursor.rowcount

    if(rows):
        cursor.execute(f"select * from {post.user} where post_id=%s",(post.post_id,))
        updated_Data = cursor.fetchone()
        cursor.close()
        conn.close()
        return updated_Data
    else:
        cursor.close()
        conn.close()
        return "please enter the correct details"


   
    
    
@app.post("/delete")
def delete(post: models.delete_post_data_validation):
    if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', post.user):
        raise HTTPException(status_code=400, detail="Invalid username. Only letters, numbers, and underscores allowed, and must start with a letter or underscore.")
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(f"delete from {post.user} where post_id=%s",(post.post_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return "Successfully deleted the post"
