from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.modules.vaccines.router import router as vaccines_router
from app.modules.locations.router import router as locations_router
from app.modules.appointments.router import router as appointments_router
from app.modules.inventory.router import router as inventory_router
from app.modules.schedules.router import router as schedules_router
from app.modules.records.router import router as records_router
from app.modules.auth.register_router import router as register_router
from app.modules.auth.login_router import router as login_router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VaxCenter API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(register_router, prefix="/api/register", tags=["Registration"])
app.include_router(login_router, prefix="/api/login", tags=["Login"])
app.include_router(vaccines_router, prefix="/api/vaccines", tags=["Vaccines"])
app.include_router(locations_router, prefix="/api/locations", tags=["Locations"])
app.include_router(appointments_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(inventory_router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(schedules_router, prefix="/api/schedules", tags=["Schedules"])
app.include_router(records_router, prefix="/api/records", tags=["Vaccination Records"])

@app.get("/")
def read_root():
    return {"message": "Welcome to VaxCenter API"}
