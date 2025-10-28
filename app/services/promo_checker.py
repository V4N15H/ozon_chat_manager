from datetime import datetime, timezone
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.message import Message
from app.crud.message import list_messages
from app.crud.order import get_order
from app.crud.promo import list_promos, delete_promo
from app.crud.chat import list_chats
from app.services.status_updater import update_chat_status
from app.schemas.chat import ChatStatusEnum
from app.schemas.message import SenderEnum


async def check_promo_conditions(db: AsyncSession):
    # Проверяет условия выдачи промокода и формирует кортеж из ozon_chat_id и promo_text для последующей отправки
    messages_to_send = []
    all_chats = await list_chats(db)
    chats = [c for c in all_chats if c.status != ChatStatusEnum.DONE]
    for chat in chats:
        await update_chat_status(db, chat.id, ChatStatusEnum.IN_PROGRESS)

        # Получаем последнее сообщение
        messages = await list_messages(db, chat.id)
        last_message = next(
            (m for m in messages if m.sender == SenderEnum.USER),
            None  # значение по умолчанию, если ничего не найдено
        )

        # Проверка на сообщение от покупателя
        if not last_message or last_message.sender != SenderEnum.USER:
            await update_chat_status(db, chat.id, ChatStatusEnum.DECLINED)
            continue


        # Проверяем наличие заказа
        order = await get_order(db, chat_id=chat.id)
        if not order:
            messages_to_send.append((
                chat.ozon_chat_id,
                "У вас не прикреплён заказ.\nПожалуйста, прикрепите заказ к чату."
            ))
            await update_chat_status(db, chat.id, ChatStatusEnum.DECLINED)
            continue

        # Проверяем статус заказа
        if order.status != "received":
            messages_to_send.append((
                chat.ozon_chat_id,
                "Ваш заказ ещё не получен.\nПодтвердите получение, чтобы получить промокод."
            ))
            await update_chat_status(db, chat.id, ChatStatusEnum.DECLINED)
            continue

        # Ищем действующий промокод
        now = datetime.now(timezone.utc).date()
        promos = await list_promos(db)
        valid_promos = [p for p in promos if p.valid_until >= now]
        promo = valid_promos[0]
        # Формируем сообщение
        promo_text = (
            "🌸 Спасибо, что доверяете нам!\n"
            "Мы рады, что вы с нами 💕\n"
            f"Дарим вам промокод: {promo.code}\n"
            "Он действует месяц и суммируется с другими акциями.\n"
            "Пусть ваши покупки будут ещё приятнее!"
        )


        await update_chat_status(db, chat.id, ChatStatusEnum.DONE)
        messages_to_send.append((chat.ozon_chat_id, promo_text))

    return messages_to_send
