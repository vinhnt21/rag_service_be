# Frequently Cmds

- List all installed packages to `requirements.txt`
    ```bash
    pip freeze > requirements.txt
    ```
- Install all packages from `requirements.txt`
    ```bash
    pip install -r requirements.txt
    ```
```bash
nodemon D:\Study\HANU\NCKH\rag_service_be\.venv\Scripts\python.exe -m flask run
```


# Bảng Giá Sử Dụng API

| Hạng mục                | Chi tiết                         | Số lượng token | Chi phí trên mỗi 1M tokens | Tổng chi phí (USD) |
|-------------------------|----------------------------------|----------------|----------------------------|--------------------|
| **Embedding**           | text-embedding-3-large           | 26,915,309     | $0.130                     | $3.50              |
| **Hỏi đáp input**       | 3,000 câu hỏi x 65 tokens       | 195,000        | $0.150                     | $0.03              |
| **Hỏi đáp output**      | 3,000 câu trả lời x 520 tokens  | 1,560,000      | $0.600                     | $0.94              |
|                         |                                  |                |                            |                    |
| **Tổng cộng**           |                                  |                |                            | **$4.46**          |
