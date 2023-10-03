import os
import sys
import webbrowser

base_path = os.path.dirname(os.path.abspath(__file__))

# 清空并新建build文件夹
os.system(f"rmdir /s /q {base_path}\\build")
os.system(f"mkdir {base_path}\\build")

# 复制文件夹内的内容到build
os.system(f"xcopy {base_path}\\config {base_path}\\build /e /i /h")
os.system(f"xcopy {base_path}\\data {base_path}\\build /e /i /h")
os.system(f"xcopy {base_path}\\themes {base_path}\\build\\themes /e /i /h")
os.system(f"xcopy {base_path}\\hugo {base_path}\\build /e /i /h")
os.system(f"xcopy {base_path}\\publish {base_path}\\build /e /i /h")

# 切换目录
os.chdir(f"{base_path}\\build")

# 运行hugo
os.system(f"hugo --buildExpired  --buildFuture --config hugo.yaml")

# 将更改发布到服务器
print("Uploading publish file to server...")
#os.system(f"rclone delete qcloud:/opt/blog/public --config .config --rmdirs")
os.system(f"rclone sync public qcloud:/opt/blog/public --config .config")
webbrowser.open_new("https://blog.steven53.top")