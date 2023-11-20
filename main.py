import os
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def process_xml_file(xml_file_path):
    # Парсим xml файл
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Получаем все теги node с полем type
    nodes = root.findall('.//node[@type]')

    txt_content = []

    for node in nodes:
        # Проверяем значение поля type
        if node.attrib['type'] == 'RIL_TEXTLINE' or node.attrib['type'] == 'RIL_WORD':

            # Извлекаем текст из тега и удаляем знаки препинания и цифры
            text = node.text
            clean_text = re.sub('[^а-яА-Яa-zA-Z ]+', '', text)

            # Добавляем очищенный текст в список
            txt_content.append(clean_text)

    # Объединяем текстовые поля через пробел
    txt = ' '.join(txt_content)
    return txt

def process_directory(directory):
    # проверяем директорию на наличие .xml файлов
    for file in os.listdir(directory):
        if file.endswith('.xml'):
            xml_file_path = os.path.join(directory, file)
            txt_file_path = os.path.splitext(xml_file_path)[0] + '.txt'

            txt_content = process_xml_file(xml_file_path)

            # Записываем очищенный текст в файл
            with open(txt_file_path, 'w') as txt_file:
                txt_file.write(txt_content)

def process_directory_recursive(directory):
    # рекурсивно обходим директории
    for root, dirs, files in os.walk(directory):
        process_directory(root)


if __name__ == '__main__':
    # Получаем путь к директории, в которой находится main.py
    directory = os.path.dirname(os.path.abspath(__file__))
    process_directory_recursive(directory)
