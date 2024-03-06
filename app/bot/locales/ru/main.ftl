# DIALOGS
common-btn-back = Назад
common-btn-cancel = Отмена
common-btn-close = Закрыть

common-title = Название
common-category = Категория

file-type-category =
{
    $file_type ->
        [photo] Фото
        [video] Видео
        [document] Документ
        [audio] Аудио
        [gif] Гиф
        *[unknown] Неизвестно
}

file-sub-type = 
{
    $sub_type -> 
        [text] текст
        [image] изображение
        [video] видео
        [audio] аудио
        *[document] документ 
}
file-title = Файл № { $file_id }

files-not-found-details = По такому запросу файлов не найдено
files-not-found-hint = Ничего не найден

missed-file-id-hint = Отправьте ид файла аргументом
missed-category-id-hint = Отправьте ид категории аргументом

invalid-file-id-hint = Некорректный ид файла
invalid-category-id-hint = Некорректный ид категории

users-locale-select = Выберите язык. Текущий язык отмечен галочкой.
users-locale-chosen = Выбран русский язык

help-text =
    Для загрузки файла достаточно просто отправить его в чат.

    Так же вы можете использовать инлайн режим для отправки файла по названию.

    Команды:
    /list - Поиск файла
    /file - Открыть файл по его ИД

    /category - Редактирование категории
    /create_category - Создание категории

    /locale - Изменить язык бота

inline-mode-btn = Попробуйте встроенный режим в другом чате
