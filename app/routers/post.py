from .. import model,schema,oAuth2
from fastapi import FastAPI, Response, status, HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func


router = APIRouter(
    prefix = "/posts",
     tags=['Posts']
)

#@router.get("/",response_model=List[schema.Post])
#@router.get("/")
@router.get("/",response_model=List[schema.PostOut])
def getPosts(db : Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""): 
    #cursor.execute(""" SELECT * FROM public."Post" ORDER BY id ASC  """)
    #posts = cursor.fetchall()
    print(f"limit={limit}")
    print(f"search string={search}")
    #posts = db.query(model.Post).filter(current_user.id == model.Post.owner_id).all()
    #posts = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = (db.query(model.Post,func.count(model.Post.id).label("Vote")).join(model.Vote,model.Vote.post_id==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all())
    #print(results)
    #return posts
    #Quick fix to manually json format Post and Vote
    #return [{"post":row.Post,"vote": row.Vote} for row in results]
    return results


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.Post)
def createPost(post: schema.CreatePost,db : Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    #post_dict = post.dict()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)
    #return {"data": post_dict}
    #cursor.execute(""" INSERT INTO public."Post" (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))

    #new_post = cursor.fetchone()

    #conn.commit()

    #new_post = model.Post(title=post.title,content=post.content,published=post.published)
    #print(f"############# Entering CReate Post ##############")
    #print(current_user.id)
    #print(current_user.email)
    new_post = model.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}",response_model=schema.PostOut)
def getSinglePost(id: int,db : Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM public."Post" where id = %s  """,(str(id)))
    # singlePost = cursor.fetchone()

    #singlePost = db.query(model.Post).filter(model.Post.id==id).first()
    # OR below code
    #singlePost = db.query(model.Post).get(id)
    #print(singlePost)


    singlePost = db.query(model.Post,func.count(model.Post.id).label("Vote")).join(model.Vote,model.Vote.post_id==model.Post.id,isouter=True).group_by(model.Post.id).filter(model.Post.id==id).first()

    print(singlePost)

    if not singlePost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" NO post is present with id==>{id}")

    if singlePost.Post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                        detail="Not authorized to perform requested action!!!!")

    return singlePost


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deleteSinglePost(id: int, respopnse: Response,db : Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    # deleteing post
    # find the index of the required id in the array
    # my_posts.pop(index)
    #index = findPostIndex(id)
    # cursor.execute(""" DELETE FROM public."Post" where id = %s  RETURNING * """,(str(id)))
    # deletedPost = cursor.fetchone()

    # conn.commit()

    deletedPost = db.query(model.Post).filter(model.Post.id==id)

    print(f"############# Entering Delete Post ##############")

    #print(f"owner id:{deletedPost.first().owner_id}")
    #print(f"Logged in user id:{current_user.id}")

    if  deletedPost.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" NO post is present with id==>{id} to be deleted")

    if deletedPost.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="Not authorized to perform requested action!!!!")

    #my_posts.pop(index)
    deletedPost.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}",response_model=schema.Post)
def updateSinglePost(id: int, post: schema.CreatePost,db : Session = Depends(get_db),current_user: int = Depends(oAuth2.get_current_user)):
    # updating post
    # find the index of the required id in the array
    # my_posts.pop(index)
    #index = findPostIndex(id)
    # cursor.execute(""" UPDATE public."Post" SET title=%s , content=%s, published=%s where id = %s  RETURNING * """,(post.title,post.content,post.published,str(id)))
    # updatedPost = cursor.fetchone()
    # conn.commit()

    updated_Post = db.query(model.Post).filter(model.Post.id==id)

    updatedPost = updated_Post.first()

    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f" NO post is present with id==>{id} to be updated")

    if updatedPost.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                        detail="Not authorized to perform requested action!!!!")

    #updatedPost.update({'title':'this is my new updated title','content':'this is my new updated content'},synchronize_session=False)

    updated_Post.update(post.dict(),synchronize_session=False)

    db.commit()

    #post_dict = post.dict()
    #post_dict["id"] = id
    #my_posts[index] = post_dict
    #return {"message": my_posts[index]}
    return updated_Post.first()

