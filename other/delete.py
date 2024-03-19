import os


def delete_files(folder_path):
    # 获取文件夹中所有文件
    files = os.listdir(folder_path)
    # 按文件修改时间排序
    files.sort(key=lambda x: os.path.getmtime(os.path.join(folder_path, x)))

    # 每读到8个文件就删除前7个
    for i in range(len(files) // 8):
        files_to_delete = files[i * 8: i * 8 + 7]
        for file_to_delete in files_to_delete:
            os.remove(os.path.join(folder_path, file_to_delete))

    print("Files processed.")


# 要处理的文件夹路径
folder_path = ("F:\PR\\133")
delete_files(folder_path)
