# 获取目录信息：(文件的总大小,文件个数，子文件夹个数)
#  不存在的目录，返回None
#  存在的目录，返回3个元素的元组
import os
import shutil


def dir_info(root_dir: str):
    """
    获取目录信息元组：(文件的总大小,文件个数，子文件夹个数)
    :param root_dir: 根目录
    :return: 元组 或 None
    """
    while True:
        # 检查参数 路径是否存在
        if not os.path.exists(root_dir):
            return 0,0,0
        # 检查参数 路径是否为文件
        if os.path.isfile(root_dir):
            return os.path.getsize(root_dir),1,0

        size = 0
        file_count = 0
        subdir_count = 0
        for cur_dir,sub_dirs,files in os.walk(root_dir):
            file_count += len(files)
            subdir_count += len(sub_dirs)
            for name in files:
                size += os.path.getsize(os.path.join(cur_dir, name))
        return size,file_count,subdir_count
    pass

def insert_path(path,inst_dir):
    absPath = os.path.abspath(path)
    pathTup = os.path.split(absPath)
    return os.path.join(pathTup[0],inst_dir,pathTup[1])

def move_insert_path(path,inst_dir):
    newdir = insert_path(path,inst_dir)
    if os.path.exists(path):
        shutil.move(path,newdir)
        return (True,newdir)
    else:
        return (False,newdir)
def join(*paths):
    """与os.path.join 类似，担忧以下不同：
        1，遇到/或'\\\\'开头的路径段，会忽略前面参数的路径前缀
        2，遇到\和/混合使用时， 原始版本，原样处理， 本方法：会统一转为平台相关的分隔符
    """
    new_paths = []
    for path in paths:
        path = path.removeprefix("/")
        path = path.removeprefix("\\")
        new_paths.append(os.path.normpath(path))
    # print(new_paths,paths)
    return os.path.join(*new_paths)
def join_slash(*paths):
    return join(*paths).replace("\\","/")