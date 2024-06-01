from setting import *
import sys
from setting import *
from tkinter import filedialog
from PIL import Image
from PIL.ExifTags import TAGS
from tkinter.messagebox import showerror, showwarning, showinfo
from colorama import init, Fore
from openai import *
from speech_recognition import *
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import telebot
import os

init() #инициализация colorama
client = OpenAI(api_key=(API_KEY)) #инициализация GPT
# sr.pause_treshold = 1
bot = telebot.TeleBot(token)

def handle_permission_denied_error(e):
    print('OpenAi не поддерживается в вашей стране или регионе')


def shut_down():
    os.system("shutdown /p")

def listen_command():
    # query = input('-> ').lower()
    """The function will return the recognized command"""

    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic,duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

        return query
    except speech_recognition.UnknownValueError:
        print('Незвестная камманда, попробуйте еще-раз')


def create_task():
    """Create todo task"""

    print('Что-бы вы хотели добавить в неё?')
    query = listen_command()

    # with open('task.txt','a', encoding='utf-8') as file:
    #     file.write(f'\n{query}')
    bot.send_message(chat_id=ID, text=f'Новая заметка: {query}')


    print(f'Задача "{query}" успешно создана!')


"""Функция шифровки"""

def encode_zip():
    try:
        path_img = filedialog.askopenfilename(title="Выбор файла (*.png, *.jpg, *.jpeg, *.mp3)", filetypes=[("Image files", "*.jpg; *.jpeg"),("Image files", "*.png"),("Sound file","*.mp3")])
        print("opened image: " + path_img)
        path_zip = filedialog.askopenfilename(title="Выбор архива", filetypes=[("Zip files", "*.zip")])
        print("opened archive: " + path_zip)
        with open(path_img, "ab") as image, open(path_zip, "rb") as archive:
            image.write(archive.read())
        print("Шифрование прошло успешно!")
        showinfo(title="Успех", message="Шифрование прошло успешно!")
    except Exception as Error:
        print("Возникла ошибка!: " + str(Error))
        showerror(title="Ошибка", message=f"Возникла ошибка!: " + str(Error))

def decode_zip():
    try:
        path_img = filedialog.askopenfilename(title="Выбор файла (*.png, *.jpg, *.jpeg, *.mp3)", filetypes=[("Image files", "*.jpg; *.jpeg"),("Image files", "*.png"),("Sound file","*.mp3")])
        with open(path_img, "rb") as image:
            data = image.read()
            offset = data.index(b"\xFF\xD9")
            image.seek(offset + 2)
            lst_path_image = path_img.split("/")
            name_archive = lst_path_image[-1] + " archive" + ".zip"
            dir_archive = filedialog.askdirectory(title="Путь сохранения архива")
            full_archive_dir = dir_archive + name_archive
            with open(full_archive_dir, "wb") as archive:
                archive.write(image.read())
            print("Разшифровка прошла успешно!")
            showinfo(title="Успех", message="Раcшифровка прошла успешно!")
    except Exception as Error:
        print("Возникла ошибка!: " + str(Error))
        showerror(title="Ошибка", message=f"Возникла ошибка!: " + str(Error))

"""Функция вывода мета данных"""

def print_meta():
    try:
        path_img = filedialog.askopenfilename(title="Выбор изображения", filetypes=[("Image files", "*.jpg; *.jpeg"),("Image files", "*.png")])
        lst_path_image = path_img.split("/")
        name_image = lst_path_image[-1]
        image = Image.open(path_img)
        info_dict = {
            "Имя файла": image.filename,
            "Размер изображения": name_image,
            "Высота изображения": image.height,
            "Ширина изображения": image.width,
            "Формат изображения": image.format,
            "Режим изображения": image.mode,
            "Анимированное изображение": getattr(image, "is_animated", False),
            "Количество кадров": getattr(image, "n_frames", 1)
        }

        for label, value in info_dict.items():
            data_image = label + ": " + str(value)
            print(data_image)
            exif_data = image.getexif()
            showinfo(title="Информация", message=data_image)
        for tag_id in exif_data:
            tag = TAGS.get(tag_id, tag_id)
            data = exif_data.get(tag_id)
            if isinstance(data, bytes):
                data = data.decode()
            print(f"{tag:25}: {data}")
            showinfo(title="Информация", message=f"{tag:25}: {data}")

    except Exception as Error:
        print("Возникла ошибка!: " + str(Error))
        showerror(title="Ошибка", message=f"Возникла ошибка!: {str(Error)}")

"""Функция удаления мета данных"""

def del_meta():
    try:
        path_img = filedialog.askopenfilename(title="Выбор изображения", filetypes=[("Image files", "*.jpg; *.jpeg"),("Image files", "*.png")])
        img = Image.open(path_img)
        data = list(img.getdata())
        img_without_metadata = Image.new(img.mode, img.size)
        img_without_metadata.putdata(data)
        img_without_metadata.save(path_img)

        print("Удаление успешно")
        showinfo(title="Успех!", message="Удаление успешно")
    except Exception as Error:
        print("Возникла ошибка!: " + str(Error))
        showerror(title="Ошибка", message=f"Возникла ошибка!: {str(Error)}")

def gpt(prompt):
        
        try:
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{'role':'user','content':prompt}]
            )
            print('Вы бы хотели сохранить ответ в телеграмм боте?')
            ans = listen_command()
            if ans in ['да', 'ye', 'yes', 'yep']:
                bot.send_message(chat_id=ID,text=f'GPT-save: {response.choices[0].message.content.strip()}')
                return response.choices[0].message.content.strip()
            elif ans != ['да', 'ye', 'yes', 'yep']:
                print(")=")
                return response.choices[0].message.content.strip()
        except PermissionDeniedError as e:
            handle_permission_denied_error(e)


def set_volume(volume_level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    
    # Установить громкость (значение от 0.0 до 1.0)
    volume.SetMasterVolumeLevelScalar(volume_level, None)

def volume_get():
    print('На сколько процентов изменить громкость звука?')
    volume = listen_command()
    for element in volume:
        try:
            if isinstance(int(element), int):
                volume = element
                volume = int(volume)
                if volume != 0:
                    set_volume(volume/10)# -> Говорить значения от 0 до 9
                else:
                    set_volume(0)
                print(f'Уровень громкости успешно изменён на {volume}%')
        except ValueError:
            pass

def main():

    # for i in tqdm(range(10)):
    #     time.sleep(0.1)


    # Вывод завершения загрузки и приветствия
    query = listen_command()
        
    if query in ['quit','exit','bye','пока']:
        print('Пятница: Досвидания, до новых встреч!')
        time.sleep(2)
        os.system('cls')
        sys.exit()
    
    elif query in ['кто твой создатель','кто тебя создал']:
        print('Пятница: мой создатель человек под псевдонимом: "Crazy_tosser3"')

    elif query in ['заметка', 'создать задачу', 'создать заметку', 'задача']:
        create_task()
    elif query in ['зашифруй файл']:
        encode_zip()
    elif query in ['расшифруй файл']:
        decode_zip()
    elif query in ['выведи мета данные', 'вывод метаданных', 'мета данные']:
        print_meta()
    elif query in ['удалить мета данные', 'удали мета данные']:
        del_meta()
    elif query in ['пока', 'goodbye', 'досвидания', 'bye', 'все goodbye']:
        print('Пятница: Досвидания! До новых встреч')

    elif query in ['изменить громкость', 'громкость']:
        volume_get()
    elif query in ['выключи пк', 'выключи', 'выключи мой пк']:
        shut_down()

    else:
        response = gpt(query)
        print(f'Пятница: {response}')
