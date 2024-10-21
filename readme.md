```
.........................................
.............N....N...CCC...L.....I......
.............NN...N..C...C..L.....I......
.............N.N..N..C......L.....I......
.............N..N.N..C......L.....I......
.............N...NN..C...C..L.....I......
.............N....N...CCC...LLL...I......
.........................................
```

# NodeJs microservices routes & test generation cli
Version: 1.0-beta

## Install

### Install in linux
copy the files anywhere\
write this line to your .bashrc:
```
alias ncli="python3 (the ncli.py location)"
```
(e.g. alias ncli="python3 /home/user/ncli/ncli.py")\

start new terminal

### Install in windows
copy the files anywhere\
add this path to the PATH enviroment variable\
use 'python ncli.py' to run.

I haven't tested in windows yet. I think it should work.

## Usage examples:

###  Create server:
```
    ncli create server
```

###  Create new router:
```
       with an empty route
    ncli add router user "group=/user"

       with a specified route
    ncli add router user "group=/user" "-api=GET /get"

       or router with rest apis
    ncli add router user -rest

       (without group option the route group will be '/<route name>')
```

###    Create or change the router file & add an api:
```
    ncli add route user -api="PUT /add"

  Add param declarations:

    ncli add route user "-api=PUT /add/:id/:name" "-params=id|name"

  Remove the router (& all its apis) (NOT WORKING YET!):

    ncli remove router user -all

  Remove specific api in the router (NOT WORKING YET!):

    ncli remove route user "-api=PUT /form"
```
###    List all routes:
```
    ncli list
```
###    Generate api tester:
```
    ncli test

        use special comment (before const declaration) to fill
        api test with default json body value
          /*<request-template>
            {
               "myparam1": "my default value1",
               "myparam1": "my default value2",
            }
          </request-template>*/
```
### Look into settings.json before run the cli.

### Examples
```
(server.ts creation)
ncli create server

(add a router file with CRUD)
ncli add router user -rest

(add a route to existing router)
ncli add route user "-api=POST /login"

(list all routes)
ncli list

(create tester file)
ncli test

```

### Settings variables (in settings.json)
"typescript": using typescipt or not\
"empty-exports": prevent the nodejs typescipt import problem\
"beautify": beauty the code or not\
"structure": the source file paths and main file location\
"server-options": server options in main file (e.g. host,port,cors options)\
"file-options": you can append the file names (e.g. %.router ==> user.router.ts )\
"var-options": you can append the var names (e.g. %Router ===> userRouter )\
"router-imports": optional array, if its [], it will be empty, other cases it will be added to the files\
"rest-options": if you use '-rest' option, add the specified CRUD service\
"route-params": use async/await in function? request/response var names or types, etc...\
"route-body": extra lines to add the function body (after the start and before the end)\
"test-option": options using for test generation\
"input-comments": you can specify the default request json data (e.g. {"name":"","pass":""} ), if is is true, write over these block with your json data

### Tester
After generate the tester the html will be in the specified path.
![image](https://github.com/user-attachments/assets/c9613fca-ae0f-4b03-a559-6d6634403e45)


### Important
Use file backups before you use cli. There isn't rollback function.



