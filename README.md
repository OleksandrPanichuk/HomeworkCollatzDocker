Панічук Олександр, КІ-41

## Запуск через Docker

1. **Побудова образу**:
   Виконайте наступну команду в терміналі, перебуваючи в папці з проєктом:
   ```bash
   docker build -t collatz-project .
   ```

2. **Запуск контейнера**:
   ```bash
   docker run --rm collatz-project
   ```

   Також можна передати аргументи (кількість воркерів та N) для `main.py`:
   ```bash
   docker run --rm collatz-project python main.py 8 1000000
   ```
