from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import products, categories, auth, orders

#  CREATE TABLES INTO THE DATABASE
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",      # The standar Port
    "http://localhost:5173"     # Vite standar Port
]


# we add the Middleware to the app (a middleware is like a door API watcher who checks every single petition before it gets to Routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # it allows petitions from the URLs (the origin list)
    allow_credentials=True,      # it allows the cookies and authentication credentials
    allow_methods=["*"],         # it allows all HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],         # it allows all HTTP headers (incluing the Authorization Token)
)


# we connect the teo routers to the main server
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(auth.router)
app.include_router(orders.router)


# we just let the route HOME just for testing
@app.get("/")
def home():
    return{"message": "Welcome to the Store API Test"}





#BEFORE CREATING ROUTER'S FOLDER WE HAD THIS:


# let's add a test endpoint: we'll need to use this command to start the server:
# uvicorn main:app --reload
# just in case if you want to see in real time what's going on with de API go here: http://127.0.0.1:8000/docs

# ENDPOINTS
# @app.get("/")
# def home():
#     return {"message": "Hey! go to the Docs section and try all out (there isn't that much in here to be honest) If you can imagine it, you can program it!"}

# @app.get("/products")
# def get_all_products(db: Session = Depends(get_db)):
#     products = db.query(models.ProductModel).all()
#     return products

# @app.get("/products/{product_id}") #product_id = 1
# def get_product(product_id: int, db: Session = Depends(get_db)):
#     product = db.query(models.ProductModel).filter(models.ProductModel.id == product_id).first()
#     if not product:
#         raise HTTPException(status_code=404, detail="Product not Found")
#     return product
        
# # from here we will create a product with the POST method. in order to do this, we'll need what we created into schemas, plus a couple things

# @app.post("/products") # product_in = is to incluide the data 
# def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
#     new_product = models.ProductModel(
#         name=product_in.name,
#         price=product_in.price,
#         is_offer=product_in.is_offer
#     )

# # with this we save it
#     db.add(new_product)
# # with this we push what we previously saved
#     db.commit()
# # and we finally have it into our database with the automatic ID
#     db.refresh(new_product)
# # we return the real product is already in the database
#     return new_product

# # now the PUT method:
# @app.put("/products/{product_id}")
# def update_product(product_id: int, product_in: ProductCreate, db: Session = Depends(get_db)):
#     # we will look for the original product in the databse:
#     db_product = db.query(models.ProductModel).filter(models.ProductModel.id == product_id).first()
    
#     if not db_product:
#         raise HTTPException(status_code=404, detail="Product not Found")
#     else:
#         db_product.name = product_in.name
#         db_product.price = product_in.price
#         db_product.is_offer = product_in.is_offer
        
#         #we dont use db.add due to we're not creating anythig just updating
#         db.commit()
#         db.refresh(db_product)
#         return db_product
        
# # now let's create the DELETE method:
# @app.delete("/products/{product_id}")
# def delete_product(product_id: int,db: Session = Depends(get_db)):
#     deleted = db.query(models.ProductModel).filter(models.ProductModel.id == product_id).first()
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Product not Found to Delete")
#     #here we use the db.delete and commit only:
#     db.delete(deleted)
#     db.commit()
#     return{"message": f"Product with ID {product_id} was deleted"}

        
    






    
    