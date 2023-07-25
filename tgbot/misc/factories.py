from aiogram.utils.callback_data import CallbackData

for_city = CallbackData("search", "city_id", "city_name")
for_photo = CallbackData("photos", "hotel_id")
for_hotels = CallbackData("hotels", "amount")
