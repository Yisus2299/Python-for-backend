from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from routers import products, categories, auth, orders
from sqlalchemy.exc import IntegrityError #with this we'll create a handler global

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

@app.exception_handler(IntegrityError)
def integrity_exception_handler(request: Request, exc: IntegrityError):
    error_msg = str(exc.orig)

    if "UNIQUE constraint failed" in error_msg or "already exists" in error_msg:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "detail": "Duplicated Error: A form with this data already exists "
            }
        )
        
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail":"Invalid Operation: Invalid data Integrity"}
    )

        
    






    
    