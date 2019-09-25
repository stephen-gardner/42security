import hashlib
import os

BUFF_SIZE = 4096


def hash_file(path):
    hasher = hashlib.sha1()
    with open(path, "rb") as file:
        buffer = file.read(BUFF_SIZE)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(BUFF_SIZE)
    return hasher.hexdigest()


def hash_rename(photos, photo_name):
    old_path = photos.path(photo_name)
    photo_name = hash_file(old_path) + os.path.splitext(photo_name)[1]
    new_path = photos.path(photo_name)
    os.rename(old_path, new_path)
    return photo_name
