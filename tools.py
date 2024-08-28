def import_data_db():
    import pandas as pd
    from sqlalchemy import create_engine, Table, MetaData, Column, Integer, String, Float
    from sqlalchemy.dialects.mysql import BIGINT, FLOAT, VARCHAR

    # Đọc file CSV
    file_path = 'mro_sanpham_full_202408170925.csv'  # Thay 'mro_sanpham_full_202408170925.csv' bằng đường dẫn thực tế đến file CSV của bạn
    data = pd.read_csv(file_path)

    # Thông tin kết nối MySQL
    user = 'root'
    password = 'admin'
    host = 'localhost'
    port = '3306'
    database = 'product_db'

    # Chuỗi kết nối đến MySQL
    connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'

    # Tạo engine kết nối
    engine = create_engine(connection_string)

    # Tạo bảng với cấu trúc phù hợp từ dữ liệu CSV nếu chưa tồn tại
    metadata = MetaData()

    products_table = Table(
        'products', metadata,
        Column('id', BIGINT, primary_key=True),
        Column('category_id', BIGINT),
        Column('sku', VARCHAR(255)),
        Column('name', VARCHAR(255)),
        Column('slug', VARCHAR(255)),
        Column('image', VARCHAR(255)),
        Column('slide', VARCHAR(255)),
        Column('price', FLOAT),
        Column('price_old', FLOAT),
        Column('detail', VARCHAR(255)),
        Column('related_products', VARCHAR(255)),
        Column('related_posts', VARCHAR(255)),
        Column('bundled_products', VARCHAR(255)),
        Column('brand_id', BIGINT),
        Column('model_producer', VARCHAR(255)),
        Column('page_catalog', VARCHAR(255)),
        Column('product_group_id', BIGINT),
        Column('ship_number', BIGINT),
        Column('sell_number', BIGINT),
        Column('ship_weight', VARCHAR(255)),
        Column('origin', VARCHAR(255)),
        Column('packing_number', BIGINT),
        Column('instock', BIGINT),
        Column('status', BIGINT),
        Column('created_at', VARCHAR(255)),
        Column('updated_at', VARCHAR(255)),
        Column('keyword', VARCHAR(255)),
        Column('description', VARCHAR(255)),
        Column('order', BIGINT),
        Column('unit', VARCHAR(255)),
        Column('warranty', VARCHAR(255)),
        Column('is_stop_sell', BIGINT),
        Column('size', VARCHAR(255)),
        Column('id_producer', VARCHAR(255)),
        Column('percent_vat', BIGINT),
        Column('price_vat', BIGINT),
        Column('is_fast_shipping', BIGINT),
        Column('related_accessories', VARCHAR(255))
    )

    # Tạo bảng trong MySQL
    metadata.create_all(engine)

    # Import dữ liệu vào bảng MySQL
    table_name = 'products'

    try:
        data.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print("Dữ liệu đã được nhập thành công vào bảng MySQL.")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")


def get_cols_datatype():
    import pandas as pd

    # Đọc file CSV
    file_path = 'mro_sanpham_full_202408170925.csv'  # Thay 'mro_sanpham_full_202408170925.csv' bằng đường dẫn thực tế đến file CSV của bạn
    data = pd.read_csv(file_path)
    print(data.dtypes)


def clean_data():
    import pandas as pd
    from sqlalchemy import create_engine

    # Thông tin kết nối MySQL
    user = 'root'
    password = 'admin'
    host = 'localhost'
    port = '3306'
    database = 'product_db'

    # Chuỗi kết nối đến MySQL
    connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'

    # Tạo engine kết nối
    engine = create_engine(connection_string)

    # Đọc dữ liệu từ bảng products
    query = "SELECT * FROM products;"
    df = pd.read_sql(query, con=engine)

    # Hàm chuyển đổi thông tin sản phẩm thành đoạn văn
    def generate_product_description(row):
        name = row['name']
        price = row['price']
        price_old = row['price_old']
        detail = row['detail']
        origin = row['origin']
        size = row['size']
        warranty = row['warranty']
        related_products = row['related_products']

        # Tạo danh sách tên và liên kết sản phẩm liên quan
        related_products_links = ""
        if pd.notna(related_products):
            try:
                related_products_ids = [int(id.strip()) for id in str(related_products).split(',') if
                                        id.strip().isdigit()]

                for related_id in related_products_ids:
                    related_product = df[df['id'] == related_id]
                    if not related_product.empty:
                        related_name = related_product.iloc[0]['name']
                        related_slug = related_product.iloc[0]['slug']
                        link = f"https://example.com/products/{related_slug}"
                        related_products_links += f"{related_name}: {link}\n"
            except (SyntaxError, TypeError) as e:
                related_products_links += "No related products available.\n"

        # Tạo đoạn văn mô tả sản phẩm
        description = (
            f"Product Name: {name}\n"
            f"Price: {price} (Old Price: {price_old})\n"
            f"Details: {detail}\n"
            f"Origin: {origin}\n"
            f"Size: {size}\n"
            f"Warranty: {warranty}\n"
            f"Related Products:\n{related_products_links}\n"
        )
        return description

    # Tạo file văn bản
    with open('products_descriptions.txt', 'w', encoding='utf-8') as file:
        for index, row in df.iterrows():
            description = generate_product_description(row)
            file.write(description + "\n---\n")

    print("Data has been successfully written to products_descriptions.txt")

    # Gọi hàm để thực hiện công việc


import tiktoken

# Định nghĩa mã hóa cho mô hình GPT-4
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# Đọc nội dung file
with open('products_descriptions.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Mã hóa nội dung và đếm token
tokens = encoding.encode(content)
num_tokens = len(tokens)

print(f"Số lượng token trong file là: {num_tokens}")
