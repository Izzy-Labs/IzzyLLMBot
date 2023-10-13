def get_wallet_by_user_id(user_id: int, data: dict) -> str:
    conn = data.get('conn')

    if conn:
        cursor = conn.cursor()
        request = "SELECT address FROM users WHERE id = %s"
        cursor.execute(request, (user_id,))
        address = cursor.fetchone()
        cursor.close()
        return address[0] if address else None
    return None
