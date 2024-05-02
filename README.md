# FastApi Skeleton
This application provides the basic structure for FastAPI development, implementing features such as logging, authentication, and containerization. 

While this skeleton is concentrated on the BrainyPedia project, it can be used in any other project.
## Features Implemented
- [x] Logging 
- ![](images/logging.png)

## Depends on?
- **JWT User & Scope Manager:** Check _APItokenmanager_ directory in [BrainyPedia](https://github.com/sensein/brainypedia/tree/ingestion-fapi-skeleton) repository.

## Features to be Implemented
- [x] Containerization of the application
- [x] JWT-based Authentication & Authorization


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