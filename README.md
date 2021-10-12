Tool này giúp anh chị em lọc ra những giờ học của riêng mình trong thời khóa biểu chung của trường.

## Yêu cầu

- python > 3.6
- pip

## Cài đặt các thư viện

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

## Bật Google API

### Tạo một project trên Google Cloud Console

1.  Truy cập vào [Google Cloud Console](https://console.cloud.google.com) để tạo project.
2.  Bên cạnh logo Google Cloud Platform, bấm "Select a project", sau đấy bấm "New Project".
3.  Nhập tên project bất kỳ
4.  Xong, nhìn vào tab bên trái, chọn "API and Services"
5.  Bên cạnh logo "API and Services", chọn "Enable API and Services", ở ô tìm kiếm, nhập "Google Calendar" rồi bấm Enter, sau đó chọn mục "Google Calendar", sau đó bấm "Enable".
6.  Nhìn vào tab bên trái, chọn "Credentials".
7.  Bên cạnh logo Credentials, bấm "Configure Consent Screen", chọn "External" rồi bấm "Create"
8.  Nhập "App name" là "Filter Lich Hoc", nhập email của bạn phía dưới, nhập lại email đó vào mục "Developer contact information" phía dưới, rồi bấm "Save and Continue"
9.  Trong mục "Scope", bấm vào nút "Add or Remove Scopes"
10. Tích hết tất cả các mục trong bảng rồi bấm "Update" (Lưu ý có 4 trang nữa nên hãy kiểm tra đã tích hết).
11. Bấm Save and Continue.
12. Ở mục "Test Users", chọn "Add User", sau đó nhập email vừa nãy bạn nhập vào đây, rồi bấm "Add", sau đó bấm "Save and Continue", cuối cùng là nút "Back To Dashboard"

### Tải về Credentials để sử dụng API

1.  Ở tab bên trái, chọn "Credentials", sau đó chọn "Create Credentials", chọn OAuth client ID
2.  Mục Application type chọn "Desktop App", sau đó chọn "Create"
3.  Bấm "Download JSON" để tải về, lưu vào một thư mục mới, nhớ lưu tên file thành **client_secret.json**
4.  Lấy file **calendar_filter.py** này về, bỏ vào thư mục đó. Lưu ý **calendar_filter.py** và **client_secret.json** phải cùng trong 1 thư mục.

## Chạy code

1.  Chỉnh biến **CALENDER_NUM** ở dòng 29 thành **L1** hoặc **L2** tùy theo lịch bạn học
2.  Sửa biến **ENG_CLASS** theo như lớp học tương ứng của bạn
3.  Sửa các giá trị trong **SCI_CLASS** theo như các class và subclass của bạn
4.  Mở CMD trong thư mục hiện tại, sau đó chạy lệnh `python calendar_filter.py`
5.  Một cửa sổ đăng nhập sẽ hiện ra, và hãy chọn tài khoản gmail mà bạn đăng ký vừa lúc nãy.
6.  Bấm "Tiếp tục", rồi bấm "Tiếp tục" tiếp.
7.  Xong rồi, check trong Google Calendar là bạn đã có một thời khóa biểu riêng!