# FastApi Skeleton
This application provides the basic structure for FastAPI development, implementing features such as logging, authentication, and containerization. 

While this skeleton is concentrated on the BrainyPedia project, it can be used in any other project.
## Features Implemented
- [x] Logging 
- ![](images/logging.png)

## Depends on?
- **JWT User & Scope Manager:** Check _APItokenmanager_ directory in [BrainyPedia](https://github.com/sensein/brainypedia/tree/ingestion-fapi-skeleton) repository. It allows the management of the permissions (or scopes). The scopes can be added as follows.
    ````python
  @router.get("/endpoint-name", dependencies=[Depends(require_scopes(["read"]))]) #1 check if the authenticated user has read permission
  async def token_check(user: Annotated[LoginUserIn, Depends(get_current_user)]): #2 check if the user (or bearer token) is a valid one 
        #your logic 
    
    ````
- Required imports
    ```python
    from fastapi import APIRouter, Depends
    
    from core.models.user import LoginUserIn
    from core.security import get_current_user, require_scopes
    
    router = APIRouter()
    ```
- Complete code would be as follows.
    ```python
    from fastapi import APIRouter, Depends
    
    from core.models.user import LoginUserIn
    from core.security import get_current_user, require_scopes
    
    router = APIRouter()
    
    
    @router.get("/endpoint-name", dependencies=[Depends(require_scopes(["read"]))])
    async def token_check(user: Annotated[LoginUserIn, Depends(get_current_user)]):
        #your logic 
        return {"message": "your message/response"}
    ```

## Features 
- [x] Containerization of the application
- [x] JWT-based Authentication & Authorization
- [x] Permission (or role or scope) management
- [x] Role based REST endpoint access

### Environment variables
```bash
ENV_STATE=dev 
DATABASE_URL= 
DB_FORCE_ROLL_BACK=False
LOGTAIL_API_KEY= 
JWT_POSTGRES_DATABASE_PORT= 
JWT_POSTGRES_DATABASE_USER= 
JWT_POSTGRES_DATABASE_PASSWORD= 
JWT_POSTGRES_TABLE_USER_SCOPE_REL= 
JWT_POSTGRES_DATABASE_NAME= 
JWT_POSTGRES_TABLE= 
JWT_POSTGRES_DATABASE_HOST_URL= 
JWT_POSTGRES_TABLE_USER= 
JWT_POSTGRES_TABLE_SCOPE= 
JWT_ALGORITHM= 
JWT_SECRET_KEY= 
```


### Acknowledgements
Special thanks to the authors of the resources below who helped with some best practices.
- Building Python Microservices with FastAPI
- Mastering-REST-APIs-with-FastAPI
- FastAPI official documentation

### License
[MIT](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt)