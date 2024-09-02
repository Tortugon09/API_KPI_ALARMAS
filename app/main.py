from fastapi import FastAPI
from routes import kpi_routes, alarm_routes, market_routes, region_routes

app = FastAPI()

app.include_router(kpi_routes.router, prefix="/api/kpis")
app.include_router(alarm_routes.router, prefix="/api/alarms")
app.include_router(market_routes.router, prefix="/api/markets")
app.include_router(region_routes.router, prefix="/api/regions")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
