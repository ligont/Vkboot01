import vk_api

class VKinderBot:

    def __init__(self, token):
        self.vk = vk_api.VK(token=token, v="5.131")

    def search(self, user_id, age, gender, city, family_status):
        try:
            users = self.vk.users.search(
                user_id=user_id,
                age_from=age,
                age_to=age,
                gender=gender,
                city=city,
                family_status=family_status,
            )
        except vk_api.exceptions.ApiError as e:
            print(f"Ошибка при поиске пользователей: {e}")
            return []

        photos = []
        for user in users:
            photo_ids = user["photos_list"]
            try:
                photos.append(self.vk.photos.get(photos_list=photo_ids))
            except vk_api.exceptions.ApiError as e:
                print(f"Ошибка при получении фотографий: {e}")
                continue

        if photos:
            top_3_photos = sorted(photos, key=lambda photo: photo["likes"], reverse=True)[:3]
        else:
            top_3_photos = []

        return top_3_photos

    def send_results(self, user_id, top_3_photos):
        for photo in top_3_photos:
            try:
                self.vk.messages.send(
                    user_id=user_id,
                    message=f"{photo['text']} ({photo['likes']} likes)",
                    attachment=photo["photo_200"],
                )
            except vk_api.exceptions.ApiError as e:
                print(f"Ошибка при отправке сообщения: {e}")
                continue


def main():
    token = input("Enter your VK token: ")

    vkinder_bot = VKinderBot(token)

    user_id = input("Enter the user ID or username: ")
    age = input("Enter the user's age: ")
    gender = input("Enter the user's gender: ")
    city = input("Enter the user's city: ")
    family_status = input("Enter the user's family status: ")

    top_3_photos = vkinder_bot.search(user_id, age, gender, city, family_status)

    vkinder_bot.send_results(user_id, top_3_photos)


if __name__ == "__main__":
    main()