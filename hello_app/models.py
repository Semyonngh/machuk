from django.db import models
from django.utils import timezone

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
        verbose_name = "Категория билета"
        verbose_name_plural = "Категории билетов"
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

class Artist(models.Model):
    name = models.CharField("Имя артиста", max_length=100)
    description = models.TextField("Описание артиста")
    image = models.URLField("Фото артиста")
    genre = models.CharField("Жанр", max_length=50, blank=True)
    
    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"
        indexes = [
            models.Index(fields=["name"])
        ]
    
    def __str__(self):
        return f"{self.name}"

class Venue(models.Model):
    name = models.CharField("Название площадки", max_length=100)
    city = models.CharField("Город", max_length=50)
    address = models.CharField("Адрес", max_length=200)
    capacity = models.IntegerField("Вместимость")
    
    class Meta:
        verbose_name = "Площадка"
        verbose_name_plural = "Площадки"
        indexes = [
            models.Index(fields=["city"]),
            models.Index(fields=["name"])
        ]
    
    def __str__(self):
        return f"{self.city}, {self.name}"

class Concert(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name="Артист")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name="Площадка")
    start_time = models.DateTimeField("Начало")
    end_time = models.DateTimeField("Конец")
    description = models.TextField("Описание концерта", blank=True)
   
    class Meta:
        verbose_name = "Концерт"
        verbose_name_plural = "Концерты"
        ordering = ["start_time"]
        indexes = [
            models.Index(fields=["start_time"]),
            models.Index(fields=["end_time"])
        ]
    
    def __str__(self):
        return f"{self.artist.name} - {self.venue.city} ({self.start_time.strftime('%d.%m.%Y')})"
    
    def get_ticket_categories(self):
        """Получить все категории билетов для этого концерта"""
        return self.ticket_set.all()
    
    def get_min_price(self):
        """Минимальная цена билета на концерт"""
        tickets = self.ticket_set.all()
        return min(ticket.price for ticket in tickets) if tickets else 0

class Shift(models.Model):
    hours = models.TimeField('Часы работы')
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, verbose_name="Сотрудник")
    concert_id = models.ForeignKey(Concert, on_delete=models.CASCADE, verbose_name="Концерт")
    
    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"
        indexes = [
            models.Index(fields=["hours"])
        ]
    
    def __str__(self):
        return f"{self.staff_id} - {self.concert_id}"

class Ticket(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, verbose_name="Концерт")
    price = models.DecimalField("Стоимость", max_digits=10, decimal_places=2)
    date = models.DateField("Дата продажи", auto_now_add=True)
    quantity = models.IntegerField("Количество доступных")
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
        return f"Билет {self.concert.artist.name} - {self.category_id} - {self.price}₽"

class TicketOrder(models.Model):
    TICKET_TYPES = [
        ('dancefloor', 'Танцпол'),
        ('fan-zone', 'Фан-зона'),
        ('vip', 'VIP'),
    ]
    
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, verbose_name="Концерт")
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, verbose_name="Выбранный билет")
    customer_name = models.CharField("Имя покупателя", max_length=100)
    email = models.EmailField("Email")
    phone = models.CharField("Телефон", max_length=20)
    ticket_type = models.CharField("Тип билета", max_length=20, choices=TICKET_TYPES)
    quantity = models.IntegerField("Количество билетов")
    total_price = models.DecimalField("Общая стоимость", max_digits=10, decimal_places=2)
    order_date = models.DateTimeField("Дата заказа", default=timezone.now)
    order_number = models.CharField("Номер заказа", max_length=20, unique=True)
    
    class Meta:
        verbose_name = "Заказ билета"
        verbose_name_plural = "Заказы билетов"
        ordering = ["-order_date"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["customer_name"]),
            models.Index(fields=["order_date"])
        ]
    
    def __str__(self):
        return f"Заказ #{self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = TicketOrder.objects.order_by('-id').first()
            last_id = last_order.id if last_order else 0
            self.order_number = f"T{last_id + 1:06d}"
        
        if self.ticket and not self.total_price:
            self.total_price = self.ticket.price * self.quantity
            
        super().save(*args, **kwargs)