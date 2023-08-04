from PIL import Image
import os
import fire
from tqdm import tqdm



def expandIMG(**kwargs):

    folder_path = kwargs.get('path')

    folders_to_process = [folder_path]

        # 循环处理文件夹和文件
    while folders_to_process:
        current_folder = folders_to_process.pop()

        print((current_folder))

        for filename in tqdm(os.listdir(current_folder),desc='expand'):

            file_path = os.path.join(current_folder, filename)

            if file_path.endswith(('.jpg', '.jpeg', '.png', '.bmp')):

                # 打开原始图片
                original_image = Image.open(file_path)

                original_width, original_height = original_image.size

                size=max(original_width,original_height)

                # 创建一个新的正方形空白图像
                new_image = Image.new("RGB", (size, size))

                try:

                    if(size==original_width):


                        center_size=(size-original_height)//2

                        # 将原始图像放置在新图像的中间部分
                        new_image.paste(original_image, (0, center_size))

                        # 进行上下插值
                        for x in range(0, size):
                            for y in range(center_size-1,-1,-1):
                                # 使用最近邻插值 
                                interpolated_pixel = original_image.getpixel((x, 0))
                                new_image.putpixel((x, y), interpolated_pixel)

                            for y in range(center_size+original_height,size):
                                # 使用最近邻插值
                                interpolated_pixel = original_image.getpixel((x, original_height-1))
                                new_image.putpixel((x, y), interpolated_pixel)

                    if(size==original_height):

                        center_size=(size-original_width)//2


                        new_image.paste(original_image, (center_size, 0))

                        # 进行左右插值
                        for y in range(0, size):
                            for x in range(center_size-1, -1,-1):
                                # 使用最近邻插值
                                interpolated_pixel = original_image.getpixel((0, y))
                                new_image.putpixel((x, y), interpolated_pixel)

                            for x in range(center_size+original_width,size):
                                # 使用最近邻插值
                                interpolated_pixel = original_image.getpixel((original_width-1, y))
                                new_image.putpixel((x, y), interpolated_pixel)

                    # 保存新图片
                    new_image.save(file_path)
                    # new_image.save(os.path.join("C:\\Users\\songyu\\Desktop\\dfg",os.path.basename(file_path)[:-4]+'.jpg'))

                except Exception as e:
                    # 获取文件名字并打印
                    filename = file_path
                    print(f"处理文件 {filename} 时发生错误: {e}")

            elif os.path.isdir(file_path):
                # 如果是子文件夹，则将其添加到待处理的文件夹栈中
                folders_to_process.append(file_path)


if __name__=='__main__':
    import fire
    fire.Fire(expandIMG)


        
    