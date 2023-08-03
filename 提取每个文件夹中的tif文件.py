import os

# 1. 列出输入路径下的所有文件,包括子文件夹中的文件
def get_dir(input_path):
    for root, dirs, files in os.walk(input_path):
        for dir in dirs:
            son_folder = os.path.join(root, dir)
            for root2, dirs2, files2 in os.walk(son_folder):
                for file in files2:
                    if file.endswith('.tif'):
                        os.rename(os.path.join(root2, file), os.path.join(target_path, file))
                        print(os.path.join(root2, file) + '已移动到' + target_path)

if __name__ == '__main__':
    input_path = r'E:\Landsat_Modis_NDVI_trend\rgb对比'
    target_path = r'E:\Landsat_Modis_NDVI_trend\rgb对比合集'
    dirs = get_dir(input_path)


