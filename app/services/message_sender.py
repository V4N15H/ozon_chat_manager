from app.services.promo_checker import check_promo_conditions
import httpx


async def send_promo_messages(db, client_id: str, api_key: str):
    # Отправляет сообщения в соответствии с проверкой условий промокода
    url = "https://api-seller.ozon.ru/v1/chat/send/message"
    headers = {
        "Client-Id": client_id,
        "Api-Key": api_key,
        "Content-Type": "application/json",
    }
    messages = await check_promo_conditions(db)

    if not messages:
        return
    async with httpx.AsyncClient() as client:
        for ozon_chat_id, text in messages:
            payload = {
                "chat_id": str(ozon_chat_id),
                "text": text,
            }
            post = await client.post(url, headers=headers, json=payload, timeout=30)
            post.raise_for_status()
