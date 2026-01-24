# The Complete Backend Flow: From Request to Data
# Toàn Tập Luồng Backend: Từ Request đến Dữ Liệu

## [EN] English Version

---

### 1. The Entry Point: The Web Server (The "Very First A")
When you type a URL or make a `fetch()` call, the request hits a Web Server (like Nginx) or a WSGI/ASGI server (like Gunicorn or the Django dev server).
- **Why?** Python code cannot talk to the internet directly. We need a "bridge" that understands HTTP and translates it into something Python can process.

### 2. Middleware: The Gatekeepers
Before reaching your logic, the request passes through **Middleware**.
- **What happens?** It checks things like: "Is this request secure (HTTPS)?", "Is it coming from an allowed frontend (CORS)?", "Is the user logged in?".
- **Why?** It prevents repetitive code. You don't want to check for login in every single function.

### 3. URL Dispatcher (The Navigator)
Django looks at your `urls.py`. It's like the Router in Next.js.
- **How it works:** It matches the URL (e.g., `/api/locations/`) to a specific **View**.
- **The "Why":** Without this, the server wouldn't know which piece of logic to run for which link.

### 4. Views: The Brain (Business Logic)
This is where the real work happens. In our project, we use `ListAPIView`.
- **Queryset:** The view reaches out to the Database. But it doesn't use SQL; it uses the **ORM**.
- **Backend Flow:** View -> Model -> Database.
- **The "Why":** Views decide *what* data should be fetched and *who* is allowed to see it.

### 5. Models & ORM (Object-Relational Mapping)
This is the most powerful part of Django.
- **How it works:** You define a Python `class Location`. Django translates this into a SQL table.
- **Magic:** When you call `Location.objects.all()`, Django writes the SQL `SELECT * FROM tours_location;` for you.
- **The "Why":** It lets you handle data as Python objects, making the code much cleaner and less error-prone than writing raw SQL.

### 6. The Storage Layer (Where MinIO lives)
When a Model has an `ImageField`, it doesn't store the actual image in the Database (DBs are bad at storing large files).
- **The mechanism:** The DB stores a string (the path). The **Storage Backend** (configured in `settings.py`) handles the actual file upload.
- **MinIO integration:** When you call `obj.image.url`, Django asks the S3 Storage backend to generate the full link (including endpoint and bucket).

### 7. Serializers: The Bridge to Frontend
Models are Python Objects. Frontend wants JSON. The **Serializer** is the translator.
- **Transformation:** It takes the Model Object and turns it into a Dictionary/JSON.
- **Custom Logic (`SerializerMethodField`):** As we discussed, you can add custom logic here. `get_full_image_url` is called for every object to "manually" refine the data before it leaves the server.

### 8. The Response: The Journey's End
The Serializer's output is wrapped in a `Response` object, passed back through the Middlewares (which might compress it), and sent over the wire as JSON to your Frontend.

---
---

## [VI] Bản Tiếng Việt

---

### 1. Điểm Đầu Vào: Web Server (Cái "A" đầu tiên)
Khi bạn nhập một URL hoặc gọi `fetch()`, request sẽ chạm vào Web Server (Nginx) hoặc WSGI/ASGI server (Gunicorn hoặc Django dev server).
- **Tại sao?** Code Python không thể trực tiếp "nói chuyện" với internet. Chúng ta cần một "cây cầu" hiểu HTTP và dịch nó thành thứ mà Python có thể xử lý.

### 2. Middleware: Những Người Gác Cổng
Trước khi đến được logic của bạn, request đi qua **Middleware**.
- **Điều gì xảy ra?** Nó kiểm tra các thứ như: "Request này có an toàn (HTTPS) không?", "Có đến từ Frontend được cho phép (CORS) không?", "User đã đăng nhập chưa?".
- **Tại sao?** Nó giúp code không bị lặp lại. Bạn không muốn phải kiểm tra đăng nhập ở trong từng hàm một.

### 3. URL Dispatcher (Người Điều Hướng)
Django nhìn vào file `urls.py`. Nó giống như Router trong Next.js.
- **Cách hoạt động:** Nó khớp URL (VD: `/api/locations/`) với một **View** cụ thể.
- **Tại sao:** Nếu không có cái này, server sẽ không biết phải chạy đoạn logic nào cho cái link nào.

### 4. Views: Bộ Não (Logic nghiệp vụ)
Đây là nơi công việc thực sự diễn ra. Trong project của mình, chúng ta dùng `ListAPIView`.
- **Queryset:** View kết nối tới Database. Nhưng nó không dùng SQL; nó dùng **ORM**.
- **Luồng:** View -> Model -> Database.
- **Tại sao:** Views quyết định dữ liệu *nào* cần lấy và *ai* được phép xem nó.

### 5. Models & ORM (Ánh xạ Đối tượng - Quan hệ)
Đây là phần mạnh mẽ nhất của Django.
- **Cách hoạt động:** Bạn định nghĩa một `class Location` bằng Python. Django tự dịch nó thành một bảng dữ liệu (Table) trong SQL.
- **Ảo thuật:** Khi bạn gọi `Location.objects.all()`, Django tự viết câu lệnh SQL `SELECT * FROM tours_location;` cho bạn.
- **Tại sao:** Nó giúp bạn xử lý dữ liệu dưới dạng đối tượng Python, giúp code sạch hơn và ít lỗi hơn việc viết SQL thuần.

### 6. Lớp Lưu Trữ - Storage Layer (Nơi MinIO sống)
Khi một Model có trường `ImageField`, nó không lưu trực tiếp cái ảnh vào Database (DB rất tệ trong việc lưu file lớn).
- **Cơ chế:** DB chỉ lưu một chuỗi văn bản (đường dẫn). **Storage Backend** (cấu hình trong `settings.py`) sẽ xử lý việc upload file thực tế.
- **Tích hợp MinIO:** Khi bạn gọi `obj.image.url`, Django sẽ hỏi S3 Storage backend để sinh ra một cái link đầy đủ (bao gồm cả endpoint và bucket).

### 7. Serializers: Cây Cầu Nối Đến Frontend
Models là các Đối tượng Python. Frontend thì muốn JSON. **Serializer** chính là người thông dịch.
- **Chuyển đổi:** Nó lấy đối tượng Model và biến thành Dictionary/JSON.
- **Logic tùy chỉnh (`SerializerMethodField`):** Như đã thảo luận, bạn có thể thêm logic ở đây. Hàm `get_full_image_url` được gọi cho từng object để "tinh chỉnh" dữ liệu thủ công trước khi nó rời khỏi server.

### 8. Response: Kết Thúc Hành Trình
Đầu ra của Serializer được đóng gói vào một đối tượng `Response`, đi ngược lại qua các Middleware (có thể được nén lại), và gửi qua mạng dưới dạng JSON đến Frontend của bạn.
