from django.db import models

class Post(models.Model):
    post = models.CharField("Должность", max_length=50)
    price = models.DecimalField("Зарплата", max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ["price"]
        indexes = [
            models.Index(fields=["post"]),
            models.Index(fields=["price"]),
        ]
        
    def __str__(self):
        return f"{self.post}"

class Category(models.Model):
    name = models.CharField("Название", max_length=50)
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        indexes = [
            models.Index(fields=["name"])
        ]
    
    def __str__(self):
        return f"{self.name}"

class Staff(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    father_name = models.CharField("Отчество", max_length=50)
    phone_number = models.CharField("Номер телефона", max_length=11)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Должность")

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name", "father_name"]
        indexes = [
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["phone_number"])
        ]
    
    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Concert(models.Model):
    start_time = models.DateTimeField("Начало")
    end_time = models.DateTimeField("Конец")
   
    class Meta:
        verbose_name = "Концерт"
        verbose_name_plural = "Концерты"
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["start_time"]),
            models.Index(fields=["end_time"])
        ]
    
    def __str__(self):
        return f"Концерт {self.start_time} - {self.end_time}"

class Shift(models.Model):
    hours = models.TimeField('Часы')
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="Сотрудник")
    concert_id = models.ForeignKey(Concert, on_delete=models.CASCADE, verbose_name="Концерт")
    
    class Meta:
        indexes = [
            models.Index(fields=["hours"])
        ]
    
    def __str__(self):
        return f"{self.hours}"

class Ticket(models.Model):
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)
    date = models.DateField("Дата")
    quantity = models.IntegerField("Количество")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        ordering = ["price"]
        indexes = [
            models.Index(fields=["price"]),
            models.Index(fields=["date"])
        ]
        
    def __str__(self):
        return f"Билет {self.category_id} - {self.price}"