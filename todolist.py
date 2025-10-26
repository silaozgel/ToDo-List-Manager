import datetime  #Required for date and time operations.

#Task Class: Represents each task
class Task:
    def __init__(self, text):
        self.text = text
        self.status = "Tamamlanmadı"
        self.start_time = None
        self.end_time = None

    def __str__(self):
        #Defines symbols according to situations.
        status_symbols = {
            "Tamamlandı": "( + )",
            "Ertelendi": "( - )",
            "Tamamlanmadı": "( x )"
        }

        #Creates time information in appropriate format.
        time_info = ""
        if self.start_time and self.end_time:
            time_info = f" ({self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%Y-%m-%d %H:%M')})"
        elif self.start_time:
            time_info = f" (Başlangıç: {self.start_time.strftime('%Y-%m-%d %H:%M')})"
        elif self.end_time:
            time_info = f" (Bitiş: {self.end_time.strftime('%Y-%m-%d %H:%M')})"

        #The text, status, and timestamp of the task are returned concatenated.
        return f"{status_symbols[self.status]} {self.text}{time_info}"

#Task Manager Class: Performs operations such as adding, deleting, and editing tasks.
class TaskManager:
    def __init__(self):
        self.tasks = [] #The list where all tasks are kept.

    #Checks if the task text is valid.
    def is_valid_task(self, task):
        task = task.strip()
        if not task: #No empty tasks should be entered.
            return False
        if task.isdigit(): #It shouldn't just be a number.
            return False
        if len(task) < 4: #Very short texts are not accepted.
            return False
        if len(task.split()) == 1 and len(task) <= 3 and task.islower():
            return False
        return True

    #Lists all tasks.
    def list_tasks(self):
        if not self.tasks:
            print("\n Görev Listesi Boş.\n")
        else:
            print("\n Görev Listesi:")
            for i, task in enumerate(self.tasks, start=1):
                print(f"{i}. {task}")
            print()

    #Adds new task.
    def add_task(self):
        task_text = input("Görevi girin: ").strip()
        if self.is_valid_task(task_text):
            self.tasks.append(Task(task_text))
            print("Görev Eklendi.\n")
        else:
            print("Lütfen geçerli görev giriniz.\n")

    #Deletes the task with the specified number.
    def delete_task(self):
        self.list_tasks()
        try:
            index = int(input("Silinecek görevin numarası: "))
            if 1 <= index <= len(self.tasks):
                removed = self.tasks.pop(index - 1)
                print(f"'{removed.text}' silindi.\n")
            else:
                print("Geçersiz numara.\n")
        except ValueError:
            print("Lütfen geçerli numara giriniz.\n")

    #Updates the status of the task.
    def update_status(self):
        self.list_tasks()
        try:
            index = int(input("Durumunu değiştirmek istediğiniz görev numarası: "))
            if 1 <= index <= len(self.tasks):
                print("Durumu seçiniz:")
                print("1. Tamamlandı ( + )")
                print("2. Ertelendi ( - )")
                print("3. Tamamlanmadı ( x )")
                choice = input("Seçiminiz (1-3): ")

                if choice == "1":
                    self.tasks[index - 1].status = "Tamamlandı"
                elif choice == "2":
                    self.tasks[index - 1].status = "Ertelendi"
                elif choice == "3":
                    self.tasks[index - 1].status = "Tamamlanmadı"
                else:
                    print("Geçersiz seçim.\n")
                    return

                print("Görev durumu güncellendi.\n")
            else:
                print("Geçersiz görev numarası.\n")
        except ValueError:
            print("Lütfen geçerli bir sayı giriniz.\n")

    #Determines the start and end dates of the task.
    def set_task_time(self, index):
        task = self.tasks[index]
        try:
            start_input = input("Başlangıç zamanı (yyyy-mm-dd HH:MM) [boş bırakmak için Enter]: ").strip()
            end_input = input("Bitiş zamanı (yyyy-mm-dd HH:MM) [boş bırakmak için Enter]: ").strip()

            if start_input:
                task.start_time = datetime.datetime.strptime(start_input, "%Y-%m-%d %H:%M")
            else:
                task.start_time = None

            if end_input:
                task.end_time = datetime.datetime.strptime(end_input, "%Y-%m-%d %H:%M")
            else:
                task.end_time = None

            print("Tarih/saat bilgisi güncellendi.\n")
        except ValueError:
            print("Hatalı format. Lütfen 'yyyy-mm-dd HH:MM' şeklinde giriniz.\n")

    #Organizes the task: text, sequence or timestamp.
    def edit_task(self):
        self.list_tasks()
        try:
            index = int(input("Düzenlenecek görevin numarası: "))
            if 1 <= index <= len(self.tasks):
                print("1. Görev metnini değiştir")
                print("2. Görevin sırasını değiştir")
                print("3. Görev tarih/saat bilgisi ekle veya değiştir")
                choice = input("Seçiminiz (1-3): ").strip()

                if choice == "1":
                    new_text = input("Yeni görev metnini girin: ").strip()
                    if self.is_valid_task(new_text):
                        old_text = self.tasks[index - 1].text
                        self.tasks[index - 1].text = new_text
                        print(f"'{old_text}' → '{new_text}' olarak değiştirildi.\n")
                    else:
                        print("Geçersiz görev metni.\n")

                elif choice == "2":
                    new_position = int(input("Yeni sırasını girin: "))
                    if 1 <= new_position <= len(self.tasks):
                        task = self.tasks.pop(index - 1)
                        self.tasks.insert(new_position - 1, task)
                        print("Görev sırası güncellendi.\n")
                    else:
                        print("Geçersiz sıra numarası.\n")

                elif choice == "3":
                    self.set_task_time(index - 1)

                else:
                    print("Geçersiz seçim.\n")
            else:
                print("Bu numarada görev yok.\n")
        except ValueError:
            print("Lütfen geçerli numara giriniz.\n")

    #The main work cycle of the application.
    def run(self):
        while True:
            print("\n----- To-Do List Uygulamasına Hoş Geldiniz -----\n")
            print("1. Görevleri Listele")
            print("2. Görev Ekle")
            print("3. Görev Sil")
            print("4. Görev Durumu Güncelle")
            print("5. Görevi Düzenle")
            print("6. Çıkış\n")

            choice = input("Seçiminiz (1-6): ").strip()

            if choice == "1":
                self.list_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.delete_task()
            elif choice == "4":
                self.update_status()
            elif choice == "5":
                self.edit_task()
            elif choice == "6":
                print("\n----- Uygulamadan çıkılıyor. Kendize iyi bakın! -----")
                break
            else:
                print("Lütfen geçerli seçim yapınız.\n")

#The TaskManager is started when the application is run directly.
if __name__ == "__main__":
    TaskManager().run()