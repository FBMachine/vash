import requests
import json

from util import splitpath, Color, BrightColor

class ExecutableType:
    UNKNOWN = 0
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4

def exec_type_str(exec_type):
    if exec_type == ExecutableType.GET:
        return "get"
    elif exec_type == ExecutableType.POST:
        return "post"
    elif exec_type == ExecutableType.PUT:
        return "put"
    elif exec_type == ExecutableType.DELETE:
        return "delete"

    return "unknown"

class Resource(object):
    def __init__(self, name):
        self.name = name

        self.children = []
        self.parent = None

    def add_child(self, resource):
        resource.parent = self
        self.children.append(resource)

    def ls(self):
        return self.children

class Executable(Resource):
    def __init__(self, name, exec_type, url):
        super(Executable, self).__init__(name)
        self.exec_type = exec_type
        self.url = url

    def get_child(self, resource_name, resource_type=Resource):
        return None

    def run(self):
        if self.exec_type != ExecutableType.GET:
            raise Exception("Unsupported executable type: " + exec_type_str(self.exec_type))
        return requests.get(self.url).json()

class Directory(Resource):
    def get_child(self, resource_name, resource_type=Resource):
        for child in self.children:
            if child.name == resource_name and isinstance(child, resource_type):
                return child
        return None

def load_package(name):
    """ Take path to swagger json (without extension).
        Import all endpoints as executables, and preceding paths as directories.
    """

    # assume swagger
    swagger = json.load(open(name+'.json', 'r'))
    # strip leading path
    name = splitpath(name)[-1]

    protocol = 'https://' if 'https' in swagger['schemes'] else 'http://'
    host = swagger['host']
    api_base = swagger['basePath']

    url = protocol + host + api_base

    package_root = Directory(name)

    for path, desc in swagger['paths'].iteritems():
        res_list = [res for res in splitpath(path) if res]
        executable = res_list[-1]
        exec_type = ExecutableType.UNKNOWN
        if 'get' in desc:
            exec_type = ExecutableType.GET
        elif 'post' in desc:
            exec_type = ExecutableType.POST
        elif 'put' in desc:
            exec_type = ExecutableType.PUT
        elif 'delete' in desc:
            exec_type = ExecutableType.DELETE

        if exec_type == ExecutableType.UNKNOWN:
            print "Unhandled executable type for: " + executable
            continue

        tail = package_root

        # treat all but leaf as a directory
        for res in res_list[:-1]:
            child = tail.get_child(res)
            if child != None:
                tail = child
            else:
                resource = Directory(res)
                tail.add_child(resource)
                tail = resource

        # final part of path is treated as the "executable"
        exec_res = Executable(executable, exec_type, url + path)
        tail.add_child(exec_res)

    return package_root

def find_resource(current_directory, path_delta, resource_type=Resource):
    """ Find resource from current directory. e.g. if current path is '~/blah',
        and path_delta is '../foo', return '~/foo' if it exists.
        Return resource if found, None otherwise.
        If resource_type is set, found resource must match this type.
    """
    deltas = splitpath(path_delta)

    new_directory = current_directory

    # save final delta since we will be checking its type
    for delta in deltas[:-1]:
        # go up a directory?
        if delta == '..':
            # was at root, invalid delta
            if new_directory.parent == None:
                return None
            new_directory = new_directory.parent
        else:
            # attempt to find subdirectory
            child = new_directory.get_child(delta)
            if not child:
                # directory not found
                return None
            new_directory = child

    # final part of path
    delta = deltas[-1]
    # go up a directory?
    if delta == '..':
        # only if not at root
        if new_directory.parent == None:
            return None
        new_directory = new_directory.parent
    else:
        # attempt to get resource, with matching type
        child = new_directory.get_child(delta, resource_type)
        if not child:
            return None
        new_directory = child

    return new_directory

def print_resource(resource):
    if type(resource) == Directory:
        print Color.BOLD + Color.BLUE + resource.name + Color.RESET
    else:
        print resource.name
