def load_gamedata(gamedata_dir=None):
    import json
    from os.path import join, dirname, basename, splitext
    from os import listdir

    # default to local gamedata
    if gamedata_dir == None:
        gamedata_dir = join(dirname( __file__ ), '..', 'gamedata')

    # laad all the gamedata files into a single dictionary
    gamedata = {}
    for path in listdir(gamedata_dir):
        (name, ext) = splitext(basename(path))
        if ext != '.json':
            continue
        with open(join(gamedata_dir,path)) as f:
            gamedata[name] = json.load(f)

    return gamedata
    
if __name__ == '__main__':
    gamedata = load_gamedata()
    print gamedata['gametext'][u'text_help']
