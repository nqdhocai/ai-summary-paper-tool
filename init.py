import os
import getpass

if __name__ == '__main__':
    # Nhập mật khẩu từ người dùng mà không hiển thị
    GG_API_KEY = getpass.getpass("YOUR GOOGLE API KEY: ")

    # Tạo biến môi trường
    os.environ['GG_API_KEY'] = GG_API_KEY

    # Kiểm tra xem biến môi trường đã tồn tại chưa
    if 'GG_API_KEY' in os.environ:
        print("Biến môi trường GG_API_KEY đã được tạo thành công.")
    else:
        print("Biến môi trường GG_API_KEY chưa tồn tại.")
