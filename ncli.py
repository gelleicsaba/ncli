version="1.1"
import json
import sys
import os
from pathlib import Path
from inspect import getsourcefile
from os.path import abspath
exepath = abspath(getsourcefile(lambda:0)).replace("/ncli.py","")
# print(exepath)
# dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.getcwd()
settingsPath = exepath
srcPath =dir_path
routesPath =dir_path
servicesPath =dir_path
mainFile = dir_path

settings=None
add=False
remove=False
router=False
route=False
routerName=None
serviceName=None
api=None
params=None
_list=False
_test=False
service=False
rest=False
ext=""
routerFile=None
warnings=0
errors=0
routerVar=None
serviceVar=None
endmark=None
asyncret=None
extraopt=None
quotes=None
routeGroup=None
create=False
server=False
addSpace=""
outputContent=None

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def main():
    global settingsPath
    global dir_path
    global settings
    # global version
    global srcPath
    global routesPath
    global servicesPath
    global mainFile
    global add
    global remove
    global router
    global route
    global routerName
    global serviceName
    global api
    global params
    global _list
    global _test
    global service
    global rest
    global ext
    global routerFile
    global warnings
    global errors
    global routerVar
    global serviceVar
    global endmark
    global asyncret
    global extraopt
    global quotes
    global routeGroup
    global create
    global server
    global addSpace
    global outputContent


    with open(f"{settingsPath}/settings.json", 'r') as file:
        settings = json.load(file)

    # Print the options & version
    if (len(sys.argv) == 1):
        print(f"{bcolors.BOLD}")
        print(".........................................")
        print(".............N....N...CCC...L.....I......")
        print(".............NN...N..C...C..L.....I......")
        print(".............N.N..N..C......L.....I......")
        print(".............N..N.N..C......L.....I......")
        print(".............N...NN..C...C..L.....I......")
        print(".............N....N...CCC...LLL...I......")
        print(".........................................")
        print("")
        print("NodeJs microservices routes & test generation cli")
        print("Version: " + str(version))
        print(f"{bcolors.ENDC}")
        print("Usage examples:")
        print("")
        print("  Create server:")
        print("    ncli create server")
        print("")
        print("  Create new router:")
        print("  ")
        print("       with an empty route")
        print("    ncli add router user \"group=/user\"")
        print("       with a specified route")
        print("    ncli add router user \"group=/user\" \"-api=GET /get\"")
        print("       or router with rest apis")
        print("    ncli add router user -rest")
        print("       (without group option the route group will be '/<route name>')")
        print("")
        print("  Create or change the router file & add an api:")
        print("")
        print("    ncli add route user -api=\"PUT /add\"")
        print("")
        print("  Add param declarations:")
        print("")
        print("    ncli add route user \"-api=PUT /add/:id/:name\" \"-params=id|name\"")
        print("")
        print("  Remove the router (& all its apis):")
        print("")
        print("    ncli remove router user -all")
        print("")
        print("  Remove specific api in the router:")
        print("")
        print("    ncli remove route user \"-api=PUT /form\"")
        print("")
        print("  List all routes:")
        print("")
        print("    ncli list")
        print("")
        print("  Generate api tester:")
        print("")
        print("    ncli test")
        print("")
        print("        use special comment (before const declaration) to fill")
        print("        api test with default json body value")
        print("          /*<request-template>")
        print("            {")
        print("               \"myparam1\": \"my default value1\",")
        print("               \"myparam1\": \"my default value2\",")
        print("            }")
        print("          </request-template>*/")
        print("")
        print("  Create service:")
        print("")
        print("    ncli add service UserService")
        print(f"    {bcolors.WARNING}(Not supported yet in this version){bcolors.ENDC}")
        print("")
        print("Look into settings.json before run the cli.")
        return

    s = settings

    # Initialize the base values
    if s["structure"]["src"] != "." and s["structure"]["src"] != "":
        srcPath += "/"
        srcPath += s["structure"]["src"]
    if s["structure"]["routes"] != "." and s["structure"]["routes"] != "":
        routesPath += "/"
        routesPath += s["structure"]["routes"]
    if s["structure"]["services"] != "." and s["structure"]["services"] != "":
        servicesPath += "/"
        servicesPath += s["structure"]["services"]
    mainFile += f"/{s["structure"]["server"]}"
    if (s["typescript"]):
        ext = ".ts"
    else:
        ext = ".js"
    if not s["beautify"]:
        endmark = ";"
        quotes = "\""
    else:
        endmark = ""
        quotes = "'"
        addSpace = " "
    if s["route-params"]["async-return"]:
        asyncret="async"
    else:
        asyncret=""
    if s["route-params"]["extra-option"] != "":
        extraopt = f"{s["route-params"]["extra-option"]}, "
    else:
        extraopt = ""

    # If src or router path not exists, create them
    if not os.path.exists(srcPath):
        os.makedirs(srcPath)
    if not os.path.exists(routesPath):
        os.makedirs(routesPath)

    # Check what params is specified
    for arg in enumerate(sys.argv):
        arg=arg[1]
        if arg == "add":
            add = True
        elif arg == "remove":
            remove = True
        elif arg == "router":
            router = True
        elif arg == "route":
            route = True
        elif arg.__contains__("api="):
            api = arg.split("=")[1]
        elif arg.__contains__("group="):
            routeGroup = arg.split("=")[1]
        elif arg.__contains__("params="):
            params = arg.split("=")[1]
        elif arg == "-rest":
            rest = True
        elif arg == "service":
            service = True
        elif arg == "test":
            _test = True
        elif arg == "list":
            _list = True
        elif arg == "create":
            create = True
        elif arg == "server":
            server = True

    if add and routeGroup == None:
        routeGroup = f"/{sys.argv[3]}"

    # Set router name/var OR service name/var
    if (router or route) and (add or remove):
        routerName = s["file-options"]["router"].replace("%", sys.argv[3])
        routerVar = s["var-options"]["router"].replace("%", sys.argv[3])
    elif service and add:
        serviceName = s["file-options"]["service"].replace("%", sys.argv[3])
        serviceVar = s["var-options"]["service"].replace("%", sys.argv[3])

    # When add a router
    if add and router and routerName != None:
        routerFile=routesPath+"/"+routerName+ext

        if not Path(mainFile).is_file():
            print(f"{bcolors.BOLD}{bcolors.FAIL}Error: The server file does not exist!{bcolors.ENDC}")
            print(f"{bcolors.BOLD}{bcolors.WARNING}       Tip: You can create the main file with 'create server' option.{bcolors.ENDC}")
            return

        # If router file doesnt exists, create it
        if not Path(routerFile).is_file():
            f = open(routerFile, "w")
            if s["empty-exports"]:
                f.write("export {}\n")
            elif s["typescript"]:
                print(f"{bcolors.BOLD}{bcolors.WARNING}Warning: It's strongly recommended to set 'exmpty-export' in case of using typescript.")
                warnings = warnings + 1
            for imp in s["router-imports"]:
                if not s["beautify"]:
                    f.write(f"{imp.replace("'","\"")}\n")
                else:
                    f.write(f"{imp.replace("\"","'").replace(";","")}\n")
            f.write("\n")
            f.write(f"const {routerVar} = express.Router(){endmark}\n")
            f.write("\n")

            # if no option defined, create a GET / by default
            if not rest and api == None:
                if s["typescript"]:
                    f.write(f"{routerVar}.get{addSpace}(\"/\", {extraopt}{asyncret} ({s["route-params"]["request"]}: {s["route-params"]["typescript-options"]["request-type"]}, {s["route-params"]["response"]}: {s["route-params"]["typescript-options"]["response-type"]}) => "+"{\n")
                else:
                    f.write(f"{routerVar}.get{addSpace}(\"/\", {extraopt}{asyncret} ({s["route-params"]["request"]}, {s["route-params"]["response"]}) => "+"{\n")
                for dcl in s["route-body"]["start"]:
                    if s["beautify"]:
                        f.write(f"\t{dcl.replace(";","")}\n")
                    else:
                        f.write(f"\t{dcl}{endmark}\n")

                f.write("\n")
                for dcl in s["route-body"]["end"]:
                    if s["beautify"]:
                        f.write(f"\t{dcl.replace(";","")}\n")
                    else:
                        f.write(f"\t{dcl}{endmark}\n")
                f.write("})\n\n")

            # if -rest or/and -api= defined
            else:
                # if -rest defined, create a GET,POST,PUT etc. routes
                if rest:
                    apis=[]
                    if s["rest-options"]["GET"]:
                        apis.append("get")
                    if s["rest-options"]["POST"]:
                        apis.append("post")
                    if s["rest-options"]["PUT"]:
                        apis.append("put")
                    if s["rest-options"]["DELETE"]:
                        apis.append("delete")
                    if s["rest-options"]["PATCH"]:
                        apis.append("path")

                    for an in apis:
                        if s["typescript"]:
                            f.write(f"{routerVar}.{an}{addSpace}(\"/\", {extraopt}{asyncret} ({s["route-params"]["request"]}: {s["route-params"]["typescript-options"]["request-type"]}, {s["route-params"]["response"]}: {s["route-params"]["typescript-options"]["response-type"]}) => "+"{\n")
                        else:
                            f.write(f"{routerVar}.{an}{addSpace}(\"/\", {extraopt}{asyncret} ({s["route-params"]["request"]}, {s["route-params"]["response"]}) => "+"{\n")
                        if an != "get" and s["test-options"]["input-comments"]:
                            f.write("\t/*<request-template>\n")
                            f.write("\t\t{\n")
                            f.write("\t\t\t\"key\":\"value\"\n")
                            f.write("\t\t}\n")
                            f.write("\t</request-template>*/\n\n")
                        for dcl in s["route-body"]["start"]:
                            if s["beautify"]:
                                f.write(f"\t{dcl.replace(";","")}\n")
                            else:
                                f.write(f"\t{dcl}{endmark}\n")

                        f.write("\n")
                        for dcl in s["route-body"]["end"]:
                            if s["beautify"]:
                                f.write(f"\t{dcl.replace(";","")}\n")
                            else:
                                f.write(f"\t{dcl}{endmark}\n")
                        f.write("})\n\n")
                # if -api= defined, create a GET,POST,PUT etc. routes
                if api != None:
                    apityp = api.split(" ")[0]
                    apiroute = api.split(" ")[1]
                    an = apityp.lower()
                    if s["typescript"]:
                        f.write(f"{routerVar}.{an}{addSpace}(\"{apiroute}\", {extraopt}{asyncret} ({s["route-params"]["request"]}: {s["route-params"]["typescript-options"]["request-type"]}, {s["route-params"]["response"]}: {s["route-params"]["typescript-options"]["response-type"]}) => "+"{\n")
                    else:
                        f.write(f"{routerVar}.{an}{addSpace}(\"{apiroute}\", {extraopt}{asyncret} ({s["route-params"]["request"]}, {s["route-params"]["response"]}) => "+"{\n")
                    if an != "get" and s["test-options"]["input-comments"]:
                        f.write("\t/*<request-template>\n")
                        f.write("\t\t{\n")
                        f.write("\t\t\t\"key\":\"value\"\n")
                        f.write("\t\t}\n")
                        f.write("\t</request-template>*/\n\n")
                    for dcl in s["route-body"]["start"]:
                        if s["beautify"]:
                            f.write(f"\t{dcl.replace(";","")}\n")
                        else:
                            f.write(f"\t{dcl}{endmark}\n")

                    f.write("\n")
                    for dcl in s["route-body"]["end"]:
                        if s["beautify"]:
                            f.write(f"\t{dcl.replace(";","")}\n")
                        else:
                            f.write(f"\t{dcl}{endmark}\n")
                    f.write("})\n\n")

            f.write(f"module.exports = {routerVar}{endmark}\n")
            f.close()

            # Read the main file (e.g.: server.js)
            content=[]
            with open(mainFile, 'r') as f2:
                for line in f2:
                    content.append(line)
            idx = len(content)-1
            # insert the route addition after last .use line
            while idx > 0 and not content[idx].__contains__(f"{s["appname"]}.use"):
                idx = idx - 1
            content.insert(idx+1, f"{s["appname"]}.use(\"{routeGroup}\", {routerVar}){endmark}\n")

            # export the route after last require
            idx = len(content)-1
            while idx > 0 and not content[idx].__contains__("require"):
                idx = idx - 1
            content.insert(idx+1, f"const {routerVar} = require({quotes}{s["import-relative-paths"]["import-router"]}/{routerName}{quotes})\n")

            # Write the main file (e.g.: server.js)
            with open(mainFile, 'w') as f3:
                for txt in content:
                    f3.write(txt)

            print(f"{bcolors.OKBLUE}{bcolors.BOLD}{routerName} has been created{bcolors.ENDC}")
        else:
            print(f"{bcolors.BOLD}{bcolors.FAIL}Error: {routerName} is exist!{bcolors.ENDC}")

        return
    elif add and route and routerName != None:
        routerFile=routesPath+"/"+routerName+ext
        if not Path(routerFile).is_file():
            print(f"{bcolors.BOLD}{bcolors.FAIL}Error: Router is not exists!{bcolors.ENDC}")
            return

        if api != None:
            content = []
            with open(routerFile, 'r') as f:
                for line in f:
                    content.append(line)

            idx = len(content)-1
            # insert the route before last module.exports line
            while idx > 0 and not content[idx].__contains__("module.exports"):
                idx = idx - 1

            apityp = api.split(" ")[0]
            apiroute = api.split(" ")[1]
            an = apityp.lower()
            if s["typescript"]:
                content.insert(idx, f"{routerVar}.{an}{addSpace}(\"{apiroute}\", {extraopt}{asyncret} ({s["route-params"]["request"]}: {s["route-params"]["typescript-options"]["request-type"]}, {s["route-params"]["response"]}: {s["route-params"]["typescript-options"]["response-type"]}) => "+"{\n")
                idx += 1
            else:
                content.insert(idx, f"{routerVar}.{an}{addSpace}(\"{apiroute}\", {extraopt}{asyncret} ({s["route-params"]["request"]}, {s["route-params"]["response"]}) => "+"{\n")
                idx += 1
            if s["test-options"]["input-comments"]:
                content.insert(idx, "\t/*<request-template>\n")
                idx += 1
                content.insert(idx, "\t\t{\n")
                idx += 1
                content.insert(idx, "\t\t\t\"key\":\"value\"\n")
                idx += 1
                content.insert(idx, "\t\t}\n")
                idx += 1
                content.insert(idx, "\t</request-template>*/\n\n")
                idx += 1
            for dcl in s["route-body"]["start"]:
                if s["beautify"]:
                    content.insert(idx, f"\t{dcl.replace(";","")}\n")
                    idx += 1
                else:
                    content.insert(idx, f"\t{dcl}{endmark}\n")
                    idx += 1

            if params != None:
                params = params.split("|")
                for par in params:
                    if settings["typescript"]:
                        parName = par.split(":")[0].strip()
                        parTyp = par.split(":")[1].strip()
                        content.insert(idx, f"\tconst {parName} :{parTyp} = {s["route-params"]["request"]}.body.{parName.replace("?","")}{endmark}\n")
                        idx += 1
                    else:
                        content.insert(idx, f"\tconst {par} = {s["route-params"]["request"]}.body.{par}{endmark}\n")
                        idx += 1

            content.insert(idx, "\n")
            idx += 1
            for dcl in s["route-body"]["end"]:
                if s["beautify"]:
                    content.insert(idx, f"\t{dcl.replace(";","")}\n")
                    idx += 1
                else:
                    content.insert(idx, f"\t{dcl}{endmark}\n")
                    idx += 1
            content.insert(idx, "})\n\n")
            idx += 1

            with open(routerFile, 'w') as f3:
                for txt in content:
                    f3.write(txt)

            print(f"{bcolors.OKBLUE}{bcolors.BOLD}'{api}' has been added to {routerName}{bcolors.ENDC}")
            return

    elif create and server:
        appname = s["appname"]
        if not Path(mainFile).is_file():
            with open(mainFile, 'w') as f:
                if s["empty-exports"]:
                    f.write("export {}\n")
                f.write(f"const express = require({quotes}express{quotes}){endmark}\n")
                f.write(f"const bodyParser = require({quotes}body-parser{quotes}){endmark}\n")
                f.write("\n")
                f.write(f"const PORT = {s["server-options"]["port"]}{endmark}\n")
                f.write(f"const HOST_NAME = {quotes}{s["server-options"]["host"]}{quotes}{endmark}\n")
                f.write("\n")
                f.write(f"const {appname} = express(){endmark}\n")
                f.write(f"{appname}.use(express.static({quotes}client{quotes})){endmark}\n")
                f.write(f"{appname}.use(bodyParser.urlencoded({{extended: true}})){endmark}\n")

                if s["server-options"]["enable-cors"]:

                    if s["typescript"]:
                        f.write(f"{appname}.use( ({s["route-params"]["request"]}: any, {s["route-params"]["response"]}: any, next: any) => {{\n")
                    else:
                        f.write(f"{appname}.use( ({s["route-params"]["request"]}, {s["route-params"]["response"]}, next) => {{\n")

                    f.write(f"\t{s["route-params"]["response"]}.header(\"Access-Control-Allow-Origin\", \"{s["server-options"]["allow-sources"]}\"){endmark}\n")
                    f.write(f"\t{s["route-params"]["response"]}.header(\"Access-Control-Allow-Methods\", \"{s["server-options"]["allow-methods"]}\"){endmark}\n")
                    f.write(f"\t{s["route-params"]["response"]}.header(\"Access-Control-Allow-Headers\", \"{s["server-options"]["allow-headers"]}\"){endmark}\n")
                    f.write(f"\t{endmark}next(){endmark}\n")
                    f.write(f"}})\n")

                # app.use ("/user", userRouter)
                f.write("\n")
                f.write(f"{appname}.listen(PORT, HOST_NAME, () => {{\n")
                f.write(f"\tconsole.log(`Server running at ${{HOST_NAME}}:${{PORT}}`){endmark}\n")
                f.write(f"}})")
            print(f"{bcolors.OKBLUE}{bcolors.BOLD}'{s["structure"]["server"]}' has been created.{bcolors.ENDC}")
        else:
            print(f"{bcolors.BOLD}{bcolors.FAIL}Error: The server file has already exists!{bcolors.ENDC}")
        return

    elif _list:

        if not Path(mainFile).is_file():
            print(f"{bcolors.FAIL}{bcolors.FAIL}Error: '{s["structure"]["server"]}' not found!{bcolors.ENDC}")
            return

        extr = s["var-options"]["router"].replace("%","")
        rgroups = []
        mainContent = []
        with open(mainFile, 'r') as f:
            for line in f:
                mainContent.append(line)
        for line in mainContent:
            if line.__contains__(f"use{addSpace}(") or line.__contains__(f"use("):
                tmp = line.split(",")
                if len(tmp) == 2:
                    rName = tmp[1].strip().replace(f"{extr}","").replace(")","")
                    if line.strip().replace("'","\"").__contains__("\""):
                        rPath = line.strip().replace("'","\"").split("\"")[1]
                        rgroups.append([rName, rPath])

        if len(rgroups) == 0:
            print(f"{bcolors.BOLD}{bcolors.OKBLUE}There aren't routes.{bcolors.ENDC}")
            return

        print(rgroups)

        for gr in rgroups:
            print(f"{gr[0]} group:\n")
            tmp = f"{routesPath}/{gr[0]}{ext}"

            rd = []
            with open(tmp, 'r') as f:
                for line in f:
                    rd.append(line)

            row = 0
            for line in rd:
                if line.__contains__(f"{extr}.get{addSpace}(") or line.__contains__(f"{extr}.get("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""
                    rt = f"\t{bcolors.OKGREEN}GET " + (gr[1] + rt).replace("//","/")
                    print(rt)
                elif line.__contains__(f"{extr}.post{addSpace}(") or line.__contains__(f"{extr}.post("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""
                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1
                    rt = f"\t{bcolors.OKBLUE}POST " + (gr[1] + rt).replace("//","/")
                    print(rt)
                    if template != "":
                        print(template)
                elif line.__contains__(f"{extr}.put{addSpace}(") or line.__contains__(f"{extr}.put("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""
                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1
                    rt = f"\t{bcolors.OKCYAN}PUT " + (gr[1] + rt).replace("//","/")
                    print(rt)
                    if template != "":
                        print(template)
                elif line.__contains__(f"{extr}.delete{addSpace}(") or line.__contains__(f"{extr}.delete("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""
                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1
                    rt = f"\t{bcolors.FAIL}DELETE " + (gr[1] + rt).replace("//","/")
                    print(rt)
                    if template != "":
                        print(template)
                elif line.__contains__(f"{extr}.patch{addSpace}(") or line.__contains__(f"{extr}.patch("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""
                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1
                    rt = f"\t{bcolors.WARNING}PATCH " + (gr[1] + rt).replace("//","/")
                    print(rt)
                    if template != "":
                        print(template)
                row += 1
            print("\n")

        return

    elif _test:

        if not Path(mainFile).is_file():
            print(f"{bcolors.FAIL}{bcolors.FAIL}Error: '{s["structure"]["server"]}' not found!{bcolors.ENDC}")
            return

        extr = s["var-options"]["router"].replace("%","")
        rgroups = []
        mainContent = []
        outputContent = []
        outputContent.append("<!-- This is NodeJs microservice api tester.")
        outputContent.append("   - Generated by njcli python cli application.")
        outputContent.append("   - http://github.com/gelleicsaba/njcli.")
        outputContent.append("   -->")
        outputContent.append("<!DOCTYPE html>")
        outputContent.append("<html>")
        outputContent.append("\t<head>")
        outputContent.append("\t\t<meta charset=\"utf-8\" />")
        outputContent.append("\t\t<meta name=\"description\" content=\"NodeJs microservice project tester\">")
        outputContent.append("\t\t<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">")
        outputContent.append("\t\t<meta http-equiv=\"Content-Security-Policy\"/>")
        outputContent.append(f"\t\t<title>{s["test-options"]["title"]}</title>")
        outputContent.append("\t\t<link rel=\"stylesheet\" href=\"./assets/style.css\" type=\"text/css\">")
        outputContent.append("\t\t<link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH\" crossorigin=\"anonymous\">")
        outputContent.append("\t\t<script src=\"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js\"></script>")
        outputContent.append("\t</head>")
        outputContent.append("\t<body>")
        outputContent.append("\t\t<div id=\"root\">")

        with open(mainFile, 'r') as f:
            for line in f:
                mainContent.append(line)
        for line in mainContent:
            if line.__contains__(f"use{addSpace}(") or line.__contains__(f"use("):
                tmp = line.split(",")
                if len(tmp) == 2:
                    rName = tmp[1].strip().replace(f"{extr}","").replace(")","")
                    if line.strip().replace("'","\"").__contains__("\""):
                        rPath = line.strip().replace("'","\"").split("\"")[1]
                        rgroups.append([rName, rPath])

        if len(rgroups) == 0:
            print(f"{bcolors.BOLD}{bcolors.OKBLUE}There aren't routes.{bcolors.ENDC}")
            return

        routerList = []
        id=100000
        for gr in rgroups:
            # print(f"{gr[0]} group:\n")
            tmp = f"{routesPath}/{gr[0]}{ext}"

            rd = []
            with open(tmp, 'r') as f:
                for line in f:
                    rd.append(line)

            row = 0
            for line in rd:
                if line.__contains__(f"{extr}.get{addSpace}(") or line.__contains__(f"{extr}.get("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""
                    template=""
                    createForm(gr[1]+rt,"get",id,template)
                    id += 1

                elif line.__contains__(f"{extr}.post{addSpace}(") or line.__contains__(f"{extr}.post("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""

                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1

                    createForm(gr[1]+rt,"post",id,template)
                    id += 1

                elif line.__contains__(f"{extr}.put{addSpace}(") or line.__contains__(f"{extr}.put("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""

                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1

                    createForm(gr[1]+rt,"put",id, template)
                    id += 1

                elif line.__contains__(f"{extr}.delete{addSpace}(") or line.__contains__(f"{extr}.delete("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""

                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1

                    createForm(gr[1]+rt,"delete",id, template)
                    id += 1

                elif line.__contains__(f"{extr}.patch{addSpace}(") or line.__contains__(f"{extr}.patch("):
                    rt = line.strip().replace("'","\"").split("\"")[1]
                    if rt == "/":
                        rt = ""

                    template=""
                    if s["test-options"]["input-comments"] and rd[row+1].__contains__("/*<request-template>"):
                        tt = row + 2
                        while not rd[tt].__contains__("</request-template>*/") and tt < len(rd):
                            template += rd[tt]
                            tt += 1

                    createForm(gr[1]+rt,"patch",id, template)
                    id += 1

                row += 1

        outputContent.append("\t\t</div>")
        outputContent.append("\t</body>")
        outputContent.append("</html>")

        outputPath = f"{dir_path}/{s["test-options"]["output-dir"]}"
        if not os.path.exists(outputPath):
            os.makedirs(outputPath)
        tmp = f"{dir_path}/{s["test-options"]["output-dir"]}/assets"
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        outputFile = f"{outputPath}/index.html"

        with open(outputFile, 'w') as f3:
            for txt in outputContent:
                f3.write(f"{txt}\n")

        cssFile=f"{outputPath}/assets/style.css"
        with open(cssFile, 'w') as f3:
            f3.write(".get { margin: 30px 0px 0px 30px; color: DarkGreen; background-color: AliceBlue; width: 850px; padding: 30px 30px 30px 30px; border-radius: 15px; }\n")
            f3.write(".post { margin: 30px 0px 0px 30px; color: DarkBlue; background-color: AliceBlue; width: 850px; padding: 30px 30px 30px 30px; border-radius: 15px; }\n")
            f3.write(".put { margin: 30px 0px 0px 30px; color: DarkCyan; background-color: AliceBlue; width: 850px; padding: 30px 30px 30px 30px; border-radius: 15px; }\n")
            f3.write(".delete { margin: 30px 0px 0px 30px; color: DarkRed; background-color: AliceBlue; width: 850px; padding: 30px 30px 30px 30px; border-radius: 15px; }\n")
            f3.write(".patch { margin: 30px 0px 0px 30px; color: Brown; background-color: AliceBlue; width: 850px; padding: 30px 30px 30px 30px; border-radius: 15px; }\n")
            f3.write(".text { width: 780px; margin-left:20px; }\n")

        print(f"{bcolors.BOLD}{bcolors.OKBLUE}The tester has been created.\nSee './{s["test-options"]["output-dir"]}'.{bcolors.ENDC}")
        return

    print(f"{bcolors.BOLD}{bcolors.FAIL}Error: Something wrong with parameters \n       Or the given function is not supported yet!{bcolors.ENDC}")


def createForm(rt, typ, id, template):
    global outputContent
    global settings
    s = settings
    btnstyle = None
    if typ == "get":
        btnstyle = "btn-success"
    elif typ == "post":
        btnstyle = "btn-primary"
    elif typ == "put":
        btnstyle = "btn-info"
    elif typ == "delete":
        btnstyle = "btn-danger"
    elif typ == "patch":
        btnstyle = "btn-warning"
    root = s["test-options"]["url"]
    pretty = None
    if s["test-options"]["pretty-json"]:
        pretty = ", null, 4"
    else:
        pretty = ""

    outputContent.append(f"\t\t\t<div class=\"{typ} form-group\">")
    outputContent.append(f"\t\t\t\t{typ.upper()}&nbsp;{rt}<br>")
    outputContent.append("\t\t\t\t<form>")
    outputContent.append(f"\t\t\t\t\t<label for=\"route{id}\">Route url</label><br>")

    outputContent.append(f"\t\t\t\t\t<input type=\"text\" id=\"route{id}\" name=\"route{id}\" value=\"{rt}\" class=\"text form-control\"><br>")
    if typ != "get":
        outputContent.append(f"\t\t\t\t\t<label for=\"input{id}\">JSON input</label><br>")
        outputContent.append(f"\t\t\t\t\t<textarea id=\"input{id}\" name=\"input{id}\" value=\"\" rows=\"5\" class=\"text form-control\">{template}</textarea><br>")

    outputContent.append(f"\t\t\t\t\t<input type=\"button\" value=\"{typ.upper()}\" onclick=\"{typ}{id}(0)\" class=\"btn {btnstyle}\">&nbsp;&nbsp;<input type=\"button\" value=\"Clear\" onclick=\"{typ}{id}(1)\" class=\"btn btn-secondary\"><br>")
    outputContent.append(f"\t\t\t\t\t<label for=\"output{id}\">Output</label><br>")
    outputContent.append(f"\t\t\t\t\t<textarea id=\"output{id}\" name=\"output{id}\" value=\"\" rows=\"5\" class=\"text form-control\"></textarea><br>")
    outputContent.append("\t\t\t\t</form>")
    outputContent.append("\t\t\t</div>")
    outputContent.append("\t\t\t<script>")
    outputContent.append(f"\t\t\t{typ}{id} = (c) => {{")

    if typ == "get":
        outputContent.append(f"\t\t\t\t\tconst rt = $('#route{id}')")
        outputContent.append(f"\t\t\t\t\tconst o = $('#output{id}')")
        outputContent.append(f"\t\t\t\t\tif(c==1){{o.val('');return}}")
        outputContent.append(f"\t\t\t\t\t$.ajax({{")
        outputContent.append(f"\t\t\t\t\t\turl: '{root}'+rt.val(),")
        outputContent.append(f"\t\t\t\t\t\ttype: 'GET',")
        outputContent.append(f"\t\t\t\t\t\tsuccess: (res) => {{")
        outputContent.append(f"\t\t\t\t\t\t\tconsole.log(res)")
        outputContent.append(f"\t\t\t\t\t\t\to.val(JSON.stringify(res{pretty}))")
        outputContent.append(f"\t\t\t\t\t\t}}")
        outputContent.append(f"\t\t\t\t\t}})")
    elif typ == "post":
        outputContent.append(f"\t\t\t\t\tconst rt = $('#route{id}')")
        outputContent.append(f"\t\t\t\t\tconst i = $('#input{id}')")
        outputContent.append(f"\t\t\t\t\tconst o = $('#output{id}')")
        outputContent.append(f"\t\t\t\t\tif(c==1){{o.val('');return}}")
        outputContent.append(f"\t\t\t\t\t$.ajax({{")
        outputContent.append(f"\t\t\t\t\t\turl: '{root}'+rt.val(),")
        outputContent.append(f"\t\t\t\t\t\ttype: 'POST',")
        outputContent.append(f"\t\t\t\t\t\tdata: JSON.parse(i.val()),")
        outputContent.append(f"\t\t\t\t\t\tsuccess: (res) => {{")
        outputContent.append(f"\t\t\t\t\t\t\tconsole.log(res)")
        outputContent.append(f"\t\t\t\t\t\t\to.val(JSON.stringify(res{pretty}))")
        outputContent.append(f"\t\t\t\t\t\t}}")
        outputContent.append(f"\t\t\t\t\t}})")
    elif typ == "put":
        outputContent.append(f"\t\t\t\t\tconst rt = $('#route{id}')")
        outputContent.append(f"\t\t\t\t\tconst i = $('#input{id}')")
        outputContent.append(f"\t\t\t\t\tconst o = $('#output{id}')")
        outputContent.append(f"\t\t\t\t\tif(c==1){{o.val('');return}}")
        outputContent.append(f"\t\t\t\t\t$.ajax({{")
        outputContent.append(f"\t\t\t\t\t\turl: '{root}'+rt.val(),")
        outputContent.append(f"\t\t\t\t\t\ttype: 'PUT',")
        outputContent.append(f"\t\t\t\t\t\tdata: JSON.parse(i.val()),")
        outputContent.append(f"\t\t\t\t\t\tsuccess: (res) => {{")
        outputContent.append(f"\t\t\t\t\t\t\tconsole.log(res)")
        outputContent.append(f"\t\t\t\t\t\t\to.val(JSON.stringify(res{pretty}))")
        outputContent.append(f"\t\t\t\t\t\t}}")
        outputContent.append(f"\t\t\t\t\t}})")
    elif typ == "delete":
        outputContent.append(f"\t\t\t\t\tconst rt = $('#route{id}')")
        outputContent.append(f"\t\t\t\t\tconst i = $('#input{id}')")
        outputContent.append(f"\t\t\t\t\tconst o = $('#output{id}')")
        outputContent.append(f"\t\t\t\t\tif(c==1){{o.val('');return}}")
        outputContent.append(f"\t\t\t\t\t$.ajax({{")
        outputContent.append(f"\t\t\t\t\t\turl: '{root}'+rt.val(),")
        outputContent.append(f"\t\t\t\t\t\ttype: 'DELETE',")
        outputContent.append(f"\t\t\t\t\t\tdata: JSON.parse(i.val()),")
        outputContent.append(f"\t\t\t\t\t\tsuccess: (res) => {{")
        outputContent.append(f"\t\t\t\t\t\t\tconsole.log(res)")
        outputContent.append(f"\t\t\t\t\t\t\to.val(JSON.stringify(res{pretty}))")
        outputContent.append(f"\t\t\t\t\t\t}}")
        outputContent.append(f"\t\t\t\t\t}})")
    elif typ == "patch":
        outputContent.append(f"\t\t\t\t\tconst rt = $('#route{id}')")
        outputContent.append(f"\t\t\t\t\tconst i = $('#input{id}')")
        outputContent.append(f"\t\t\t\t\tconst o = $('#output{id}')")
        outputContent.append(f"\t\t\t\t\tif(c==1){{o.val('');return}}")
        outputContent.append(f"\t\t\t\t\t$.ajax({{")
        outputContent.append(f"\t\t\t\t\t\turl: '{root}'+rt.val(),")
        outputContent.append(f"\t\t\t\t\t\ttype: 'PATCH',")
        outputContent.append(f"\t\t\t\t\t\tdata: JSON.parse(i.val()),")
        outputContent.append(f"\t\t\t\t\t\tsuccess: (res) => {{")
        outputContent.append(f"\t\t\t\t\t\t\tconsole.log(res)")
        outputContent.append(f"\t\t\t\t\t\t\to.val(JSON.stringify(res{pretty}))")
        outputContent.append(f"\t\t\t\t\t\t}}")
        outputContent.append(f"\t\t\t\t\t}})")
    else:
        outputContent.append("\t\t\t\t\talert('yo')")

    outputContent.append("\t\t\t\t\t}")
    outputContent.append("\t\t\t</script>")

if __name__ == "__main__":
    main()

