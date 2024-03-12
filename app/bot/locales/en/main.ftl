# DIALOGS
common-btn-back = Back
common-btn-cancel = Cancel
common-btn-close = Close

common-title = Title
common-category = Category

file-type-category =
{
    $file_type ->
        [photo] Photo
        [video] Video
        [document] Document
        [audio] Audio
        [gif] Gif
        *[unknown] Unknown
}

file-sub-type = 
{
    $sub_type -> 
        [text] text
        [image] image
        [video] video
        [audio] audio
        *[document] document
}

file-title = File № { $file_id }


files-not-found-details = No files found for this request
files-not-found-hint = Not found
file-not-found = File not found

missed-file-id-hint = Send file id as argument
missed-category-id-hint = Send category id as argument

file-already-exists = This file has already been uploaded
invalid-file-id-hint = Invalid file id
invalid-category-id-hint = Invalid category id


users-locale-select = Choose language. The current language is marked with a check mark.
users-locale-chosen = English language chosen

help-text =
    To download a file, simply send it to the chat.
    You can also use the inline mode to send a file by name.

    Commands:
    /list - Search files
    /file - Open a file by its ID

    /category - Editing a category
    /create_category - Create a category

    /locale - Change the bot language

inline-mode-btn = Try inline mode in other chat

file-access-denied = You do not have access to this file
category-access-denied = You do not have access to this category

file-upload-add-category = Add category
file-upload-send = Send a file