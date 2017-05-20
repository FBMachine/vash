from resource import Directory, find_resource, print_resource, load_package

def validate_directory(command_name, directory):
    """ Ensure resource exists, and is a directory.
        True if is existing directory, False otherwise.
    """
    if directory == None:
        print command_name + ': "' + directory + '": No such directory'
        return False
    elif type(directory) != Directory:
        print command_name + ': "' + directory + '": Not a directory'
        return False

    return True

def ls(state, path_delta):
    """ Print out list of resources at current directory
    """
    if path_delta:
        target_directory = find_resource(state.current_directory, path_delta)
    else:
        target_directory = state.current_directory

    if validate_directory('ls', target_directory):
        resources = target_directory.ls()
        for resource in resources:
            print_resource(resource)

def install(state, package_name):
    """ Import a package describing api.
    """
    state.current_directory.add_child(load_package(package_name))
    state.local_autocomplete = []
    for resource in state.current_directory.ls():
        state.local_autocomplete.append(resource.name)

def cd(state, path_delta):
    """ Change directory given a path delta.
        Also updates auto-complete choices.
    """
    new_directory = find_resource(state.current_directory, path_delta)
    if validate_directory('cd', new_directory):
        state.current_directory = new_directory
    state.local_autocomplete = []
    for resource in state.current_directory.ls():
        state.local_autocomplete.append(resource.name)

if __name__ == '__main__':
    print "test"
