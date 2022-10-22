from pathlib import Path
from wordcloud import WordCloud

# Читать текстовое содержимое
current_directory = Path.cwd()
text = Path.open(current_directory/"file.txt").read() #нужно вставить название текстового файла для чтения на аглийском

# Создать объект экземпляра облака слов
wordcloud = WordCloud()

# Загрузить текстовое содержимое в объект облака слов.
wordcloud.generate(text)

# Вывести изображение с заданным именем файла изображения.
wordcloud.to_file('WordCloud_pic.png')