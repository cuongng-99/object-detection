# Intro

- Danh sách sản phẩm Abby: Download và Crop vào 1 folder
- Các sản phẩm của đối thủ: khi có sản phẩm mới hoặc sản phẩm đổi giá thì chạy model => detect => nếu phát hiện
có sản phẩm abby tương tự thì cần thêm thông tin vào trường `competitorProducts`:

- Tạo thêm trường `competitorProducts` trong `products`:
  ```json
  {
    "_id": ,
    "competitor": ,
    "link": ,
    "price: "
  }
  ```

- Noti vào channel `#competition`
