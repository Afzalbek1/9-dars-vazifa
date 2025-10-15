from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram import Router, F
from aiogram.filters import Command, CommandStart

from buttons import REG_TEXT, GET_NAME, GET_PHONE,ERR_NAME, SUCCES_REG,ALREADY_IN,CAPTION_BOOK
from buttons import register_kb, phoneNumber_kb, menu_kb, after_menukb, send_toAdminkb, order_inline_kb, order_kb
from buttons import CONTACT_ADMIN


from aiogram.types import FSInputFile
from states import Register, Order, FSMContext
from filters import validate_name,validate_phone
from database import save_users, is_register_byChatId, add_order, get_user_by_chat_id, get_book_by_id
user_router = Router()

@user_router.message(CommandStart())
async def start(message: Message):
    if is_register_byChatId(message.from_user.id): 
        await message.answer(ALREADY_IN, reply_markup = menu_kb)
        
    else:
        await message.answer(REG_TEXT, reply_markup=register_kb)


@user_router.message(F.text == "Ro'yxatdan O'tish")
async def start(message: Message, state: FSMContext):
    await state.set_state(Register.name)
    await message.answer(GET_NAME, reply_markup=ReplyKeyboardRemove())
    

@user_router.message(Register.name)
async def get_name(message: Message, state: FSMContext):
    name = message.text.strip()  
    
    if validate_name(name):
        await state.update_data(name=name)
        await state.set_state(Register.phone)
        await message.answer(GET_PHONE, reply_markup=phoneNumber_kb)
    else:
        await message.answer(ERR_NAME)


@user_router.message(Register.phone) 
async def get_phone(message:Message, state: FSMContext):
    if message.contact: 
        phone = message.contact.phone_number
    else: 
        phone = message.text.split() 
        
    if validate_phone(phone): 
        await state.update_data(phone=phone)
        data =  await state.get_data()
        
        save_users(
            message.from_user.id,
           	data['name'], 
          	data['phone'], 
            message.from_user.username or None
                        )
        await message.answer(SUCCES_REG, reply_markup=menu_kb)
        await state.clear()
    else: 
        message.answer("❌ Telefon raqam noto‘g‘ri. Iltimos, +998901234567 formatida kiriting.")
        

        
@user_router.message(F.text=="📋 Menu")
async def menu_btn(message:Message, state:FSMContext): 
    await message.answer("📋 Asosiy menyu:",reply_markup=after_menukb)
    

@user_router.message(F.text=="⬅️ Back") 
async def back_menu(message:Message):
    await message.answer("📋 Main menu", reply_markup=menu_kb)
    

@user_router.message(F.text=="📞 Contact") 
async def contact_admin(message:Message): 
    await message.answer("""📩 Savollaringiz bormi?
  Biz har doim yordam berishga tayyormiz!
  Savvolarigizni yozing va Pastagi Yuborish tugmasini bosing""", reply_markup=send_toAdminkb)
  

@user_router.message(F.text=="Yuborish") 
async def send_admin(message:Message): 
    await message.answer(CONTACT_ADMIN)
    
    
@user_router.message(F.text=="⬅️ back") 
async def back_menu(message:Message):
    await message.answer("📋 Main menu", reply_markup=after_menukb)


@user_router.message(F.text == "🛒 Order")
async def order_handler(message:Message, state: FSMContext):
    await state.set_state(Order.quantity)
    await state.update_data(quantity=1, book_id=1)
    await message.answer("Your orders is loading..", reply_markup=order_kb)
    photo_path = FSInputFile("imgs/image.png")
    await message.answer_photo(photo=photo_path, caption=CAPTION_BOOK, reply_markup=order_inline_kb)

@user_router.callback_query(F.data == "add")
async def add_quantity(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quantity = data.get('quantity', 1) + 1
    await state.update_data(quantity=quantity)
    await callback.answer(f"Quantity: {quantity}")

@user_router.callback_query(F.data == "subtract")
async def subtract_quantity(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quantity = max(1, data.get('quantity', 1) - 1)
    await state.update_data(quantity=quantity)
    await callback.answer(f"Quantity: {quantity}")

@user_router.callback_query(F.data == "one")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    quantity = data.get('quantity', 1)
    book_id = data.get('book_id', 1)

    user = get_user_by_chat_id(callback.from_user.id)
    if not user:
        await callback.message.answer("User not found. Please register first.")
        await state.clear()
        return

    user_id = user[0]

    book = get_book_by_id(book_id)
    if not book:
        await callback.message.answer("Book not found.")
        await state.clear()
        return

    price = book[4] * quantity

    order_id = add_order(book_id, user_id, price, quantity)
    if order_id:
        await callback.message.answer(f"✅ Order confirmed!\nQuantity: {quantity}\nTotal Price: {price} so'm\nOrder ID: {order_id}")
    else:
        await callback.message.answer("❌ Failed to place order. Please try again.")

    await state.clear()
    