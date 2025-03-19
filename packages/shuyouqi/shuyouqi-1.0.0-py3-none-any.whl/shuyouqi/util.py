def df_to_blob(df):
    import js, io
    
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    csv_str = csv_buffer.getvalue()
    csv_buffer.close()

    # 创建Blob对象
    blob = js.Blob.new([csv_str], {"type": "text/csv;charset=utf-8;"})

    # 创建Blob URL
    blob_url = js.URL.createObjectURL(blob)
    return blob_url
