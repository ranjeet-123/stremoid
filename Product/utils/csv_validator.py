import pandas as pd
from io import StringIO

# Define required fields
REQUIRED_FIELDS = ['sku', 'name', 'brand', 'mrp', 'price']


def validate_and_parse_csv(uploaded_file) -> tuple:
    """
    Accepts Django UploadedFile (file-like) and returns (valid_rows, invalid_rows)
    Each row is a dict ready to be passed to Product.objects.update_or_create
    """
    # Try reading directly with pandas
    try:
        df = pd.read_csv(uploaded_file)
    except Exception:
        # If failed, re-read as UTF-8 string
        uploaded_file.seek(0)
        content = uploaded_file.read().decode('utf-8', errors='replace')
        df = pd.read_csv(StringIO(content))

    valid_rows = []
    invalid_rows = []

    for idx, row in df.iterrows():
        row_dict = {col: (None if pd.isna(row.get(col)) else row.get(col)) for col in df.columns}

        # Required fields check
        missing = [f for f in REQUIRED_FIELDS if not row_dict.get(f)]
        if missing:
            row_dict['_errors'] = f"Missing required fields: {missing}"
            invalid_rows.append(row_dict)
            continue

        # Numeric conversions & validations
        try:
            row_dict['mrp'] = float(row_dict['mrp'])
            row_dict['price'] = float(row_dict['price'])
        except Exception:
            row_dict['_errors'] = 'mrp/price must be numeric'
            invalid_rows.append(row_dict)
            continue

        # Quantity validation
        try:
            q = row_dict.get('quantity', 0)
            if q is None or (str(q).strip() == ''):
                q = 0
            row_dict['quantity'] = int(float(q))
        except Exception:
            row_dict['_errors'] = 'quantity must be an integer'
            invalid_rows.append(row_dict)
            continue

        # Business rules
        if row_dict['price'] > row_dict['mrp']:
            row_dict['_errors'] = 'price must be <= mrp'
            invalid_rows.append(row_dict)
            continue

        if row_dict['quantity'] < 0:
            row_dict['_errors'] = 'quantity must be >= 0'
            invalid_rows.append(row_dict)
            continue

        # Keep only known keys
        allowed_keys = ['sku', 'name', 'brand', 'color', 'size', 'mrp', 'price', 'quantity']
        clean = {k: row_dict.get(k) for k in allowed_keys}
        valid_rows.append(clean)

    return valid_rows, invalid_rows
