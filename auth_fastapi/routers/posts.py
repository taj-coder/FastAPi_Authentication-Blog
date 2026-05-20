from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from database import get_db
from routers.auth import get_current_user 

router = APIRouter(
    prefix="/posts",
    tags=["Posts Operations"]
)

# 
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes = True

class UserMinResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class PostResponse(PostBase):
    id: int
    owner_id: int | None = None
    owner: UserMinResponse | None = None  # Fetches the owner data dynamically

    class Config:
        from_attributes = True
# 

@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.DBUser = Depends(get_current_user) # authentication
):
    new_db_row = models.DBPost(
        title=post.title, 
        content=post.content,
        owner_id=current_user.id
    )
    db.add(new_db_row)
    db.commit()
    db.refresh(new_db_row)
    return new_db_row


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: models.DBUser = Depends(get_current_user)
):
    target_post = db.query(models.DBPost).filter(models.DBPost.id == post_id).first()
    
    if not target_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {post_id} was not found."
        )
        
    # Check ownership
    if target_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
        
    db.delete(target_post)
    db.commit()
    return None

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, 
    updated_post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: models.DBUser = Depends(get_current_user)
):
    post_query = db.query(models.DBPost).filter(models.DBPost.id == post_id)
    target_post = post_query.first()
    
    if not target_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {post_id} was not found."
        )
        
    # Check ownership
    if target_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action"
        )
        
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()



