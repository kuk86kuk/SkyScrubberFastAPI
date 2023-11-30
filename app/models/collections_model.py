import datetime



def logs(docs, tag_id):
    json = {
        "id": docs,
        "task": tag_id,
        'register_datatime': datetime.datetime.now()
    }
    return json



def tags(tag, name, process):
    json = {
        "tag": tag,
        "name": name,
        "process": process,
        'time': datetime.datetime.now()
    }
    return json



def tasks(path, args):
    json = {
        "path": path,
        "args": args
    }
    return json

