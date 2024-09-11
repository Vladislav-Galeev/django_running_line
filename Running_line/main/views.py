from django.http import FileResponse, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Note

import cv2
import numpy as np


def download_file(request, running_line):
    
    note = Note(text=running_line)
    note.save()

    width, height = 100, 100

    # Задаем параметры для видео
    out = cv2.VideoWriter("video.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (width, height))

    # Создаем кадр
    frame = np.zeros((height, width, 3), dtype=np.uint8)

    # Начальные координаты для бегущей строки
    x, y = width, height // 2

    # Установим параметры шрифта
    font = cv2.FONT_HERSHEY_COMPLEX # Поддержка кириллицы
    font_scale = 0.5
    font_thickness = 1
    font_color = (255, 255, 255)  # Белый цвет текста

    # Найдем размеры бегущей строки
    message_size = cv2.getTextSize(running_line, font, font_scale, font_thickness)

    # Вычислим скорость, с которой необходимо двигать строку
    v = round((width+message_size[0][0]) / 90)

    # Двигаем строку каждый кадр (3 секунды * 30 кадров = 90)
    for i in range(90):

        # Очистка кадра
        frame.fill(0)

        # Двигаем строку с найденной скоростью
        x -= v

        # Добавляем текст
        cv2.putText(frame, running_line, (x, y), font, font_scale, font_color, font_thickness)

        # Записываем кадр
        out.write(frame)

    # Закрываем видеопоток
    out.release()

    video = open("video.mp4", 'rb')
    response = HttpResponse(video, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename=my_video.mp4'
    
    return response


def get_notes(request):

    notes = Note.objects.all().values()
    return JsonResponse(list(notes), safe=False)