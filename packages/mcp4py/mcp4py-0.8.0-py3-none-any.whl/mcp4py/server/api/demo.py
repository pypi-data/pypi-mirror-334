from fastapi import FastAPI,APIRouter


class Tools(FastAPI):
    def init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup_routes()

    def setup_routes(self):
        router = APIRouter(prefix="/items",tags=["items"],responses={404: {"description": "Not found"}})
        @router.post("/")
        async def test_1():
            return {"test": "test1"}
        self.include_router(router) # 将路由添加到 FastAPI 实例