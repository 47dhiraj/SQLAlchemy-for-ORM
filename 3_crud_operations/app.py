from models import session, User, Comment, Post, Category, Tag


from sqlalchemy import select


from sqlalchemy.exc import SQLAlchemyError





## *********************************** CRUD OPERATIONS ***********************************










## ******************************** ALL FUNCTION DEFINITIONS ********************************




## ************************************** CREATES USER **************************************


def add_user(db_session, username: str, email: str):

    stmt = select(User).where(User.username == username, User.email == email)
    user = db_session.scalars(stmt).first()
    

    if user:
        print(f"User with username: {username} and email: {email} already exists")
        return
    
    new_user = User(username=username, email=email)
    db_session.add(new_user)
    

    try:

        db_session.commit()
        print(f"User '{username}' added.")

    except SQLAlchemyError as e:

        db_session.rollback()
        print(f"Error adding user: {e}")
        raise
             
    





## *********************************** CREATES CATEGORY ***********************************


def add_category(db_session, category_name: str):

    stmt = select(Category).where(Category.name == category_name)
    existing = db_session.scalars(stmt).first()
    

    if existing:
        print(f"Category '{category_name}' already exists.")
        return existing


    category = Category(name=category_name)
    db_session.add(category)
   

    try:
        db_session.commit()
        print(f"Category '{category_name}' added.")

    except SQLAlchemyError as e:

        db_session.rollback()
        print(f"Error adding category: {e}")
        raise








## *********************************** CREATES TAG ***********************************


def add_tag(db_session, name: str):

    stmt = select(Tag).where(Tag.name == name)
    existing_tag = db_session.scalars(stmt).first()
    

    if existing_tag:
        print(f"Tag '{name}' already exists.")
        return existing_tag


    new_tag = Tag(name=name)
    db_session.add(new_tag)
    

    try:

        db_session.commit()
        print(f"Tag '{name}' added.")
        return new_tag
    
    except SQLAlchemyError as e:

        db_session.rollback()
        print(f"Error adding tag: {e}")
        raise








## *********************************** CREATES POST ***********************************


def add_post(db_session, username: str, title: str, content: str, category_name: str, tag_names: list[str] = None):
    
    if tag_names is None:
        tag_names = []


    try:

        user = db_session.scalars(select(User).where(User.username == username)).first()
        category = db_session.scalars(select(Category).where(Category.name == category_name)).first()


        if not user or not category:

            print(f"Error: User '{username}' or Category '{category_name}' not found.")
            return

        new_post = Post(title=title, content=content, user=user, category=category)


        for name in tag_names:

            tag = db_session.scalars(select(Tag).where(Tag.name == name)).first()

            if not tag:
                tag = Tag(name=name)
                db_session.add(tag) 

            new_post.tags.append(tag)


        db_session.add(new_post)
        db_session.commit()

        print(f"Post '{title}' added by '{username}'.")

        return new_post

    except SQLAlchemyError as e:

        db_session.rollback()
        print(f"Database error: {e}")
        raise









## *********************************** CREATES COMMENT ***********************************


def add_comment(db_session, username: str, post_id: int, content: str):

    try:

        user_stmt = select(User).where(User.username == username)
        user = db_session.scalars(user_stmt).first()

        post = db_session.get(Post, post_id)

        if not user or not post:
            print(f"Error: User '{username}' or Post ID '{post_id}' not found.")
            return

        new_comment = Comment(content=content, user=user, post=post)
        
        db_session.add(new_comment)
        db_session.commit()
        
        print(f"Comment added to post '{post.title}' by '{username}'.")

        return new_comment

    except SQLAlchemyError as e:

        db_session.rollback()
        
        print(f"Database error: {e}")
        raise










## *********************************** READ POSTS BY CATEGORY ***********************************


def get_posts_by_category(db_session, category_name: str):

    stmt = select(Category).where(Category.name == category_name)
    category = db_session.scalars(stmt).first()

    if not category:
        print(f"Category '{category_name}' not found.")
        return []

    posts = category.posts
    
    return posts










## *********************************** READ POSTS OF A USER ***********************************


def get_all_posts_by_username(dbsession, username:str):

    user = session.scalars(select(User).where(User.username == username)).first()

    if not user.posts:
        print("  (No posts found)")
        return

    return user.posts









## ***************************** READ POSTS OF A USER WITH PAGINATION *****************************

def get_posts_by_username_paginated(db_session, username: str, page: int = 1, per_page: int = 5):

    current_offset = (page - 1) * per_page

    stmt = (
        select(Post)
        .join(Post.user)
        .where(User.username == username)
        .order_by(Post.id.desc())
        .limit(per_page)
        .offset(current_offset)
    )

    posts = db_session.scalars(stmt).all()

    if not posts:
        print(f"No posts found for {username} on page {page}.")
        return []
 
    return posts









## *********************************** READ TAGS ***********************************


def get_tags_by_names(db_session, tag_names: list[str]):

    stmt = select(Tag).where(Tag.name.in_(tag_names))
    
    tags = db_session.scalars(stmt).all()
    
    return tags










## *********************************** UPDATE POST ***********************************


def update_post(
    db_session,
    post_id: int,
    new_title: str = None,
    new_content: str = None,
    new_category_name: str = None,
    new_tag_names: list[str] = None,
):
    

    try:

        post = db_session.get(Post, post_id)
        
        if not post:
            print(f"Post with id '{post_id}' not found.")
            return

        if new_title is not None:
            post.title = new_title

        if new_content is not None:
            post.content = new_content

        if new_category_name:
            stmt = select(Category).where(Category.name == new_category_name)
            category = db_session.scalars(stmt).first()

            if category:
                post.category = category
            else:
                print(f"Category '{new_category_name}' not found. Skipping category update.")


        if new_tag_names is not None:
            post.tags.clear() 
            
            for name in new_tag_names:
                tag_stmt = select(Tag).where(Tag.name == name)
                tag = db_session.scalars(tag_stmt).first()

                if not tag:
                    tag = Tag(name=name)
                    db_session.add(tag)
                
                post.tags.append(tag)

        db_session.commit()

        print(f"Post with id '{post_id}' updated successfully.")
        return post

    except SQLAlchemyError as e:
        db_session.rollback()
        print(f"Error updating post: {e}")
        raise




 
 


## *********************************** UPDATE COMMENT ***********************************


def update_comment(db_session, comment_id: int, new_content: str):

    try:

        comment = db_session.get(Comment, comment_id)

        if not comment:
            print(f"Comment with ID '{comment_id}' not found.")
            return

        comment.content = new_content

        db_session.commit()
        print(f"Comment with ID '{comment_id}' updated successfully.")

        return comment

    except SQLAlchemyError as e:

        db_session.rollback()

        print(f"Error updating comment: {e}")
        raise








## *********************************** DELETE POST ***********************************


def delete_post(db_session, post_id: int):

    try:

        post = db_session.get(Post, post_id)

        if not post:
            print(f"Post with ID '{post_id}' not found.")
            return False

        
        db_session.delete(post)

        db_session.commit()

        print(f"Post with ID '{post_id}' and its related data have been deleted.")

        return True

    except SQLAlchemyError as e:

        db_session.rollback()

        print(f"Error deleting post: {e}")

        raise






## *********************************** DELETE COMMENT ***********************************


def delete_comment(db_session, comment_id: int):

    try:

        comment = db_session.get(Comment, comment_id)

        if not comment:
            print(f"Comment with ID '{comment_id}' not found.")
            return False
        
        db_session.delete(comment)

        db_session.commit()

        print(f"Comment with ID '{comment_id}' deleted successfully.")

        return True


    except SQLAlchemyError as e:

        db_session.rollback()

        print(f"Error deleting comment: {e}")
        raise
















## *********************************** ALL FUNCTIONS CALL ***********************************






## *********************************** CREATE OPERATIONS CALL ***********************************



username = "John Doe"
email="John@gmail.com"

add_user(session, username, email)





category_name="Educational"

add_category(session, category_name)




add_tag(session, "Python")




add_post(
    session,
    username="John Doe",
    title="Getting Started with SQLAlchemy 2.0",
    content="In this post, we explore the new features and functionality of SQLAlchemy 2.0",
    category_name="Educational",
    tag_names=["Python", "Database", "ORM"]
)




add_comment(session, "John Doe", 1, "This is a great post! Very helpful.")










## *********************************** READ OPERATIONS CALL ***********************************



posts = get_posts_by_category(session, "Educational")

post_count = len(posts)
print(f"Total Posts:- {post_count}") 

for post in posts:
    print(f"Category:- {post.category.name}\nPost:- {post.title}")





user_posts = get_all_posts_by_username(session,"John Doe")

for post in user_posts:
    print(post.title,"\n",post.content)




page_1_posts = get_posts_by_username_paginated(session, "John Doe", page=1, per_page=5)

for post in page_1_posts:
    print(post.title, "\n", post.content)







tags = get_tags_by_names(session, ["Python", "ORM"])

for tag in tags:
    print(f"{tag.name} ", end="")     









## *********************************** UPDATE OPERATIONS CALL ***********************************



update_post(
    session, 
    post_id=1, 
    new_title="My Updated Title", 
    new_tag_names=["Python", "SQLAlchemy", "Coding"]
)




update_comment(session, 1, "This is my updated comment text!")










## *********************************** DELETE OPERATIONS CALL ***********************************


delete_post(session, 1)


delete_comment(session, 1)