from django.db import models
from django.urls import reverse # Usado para gerar URL buscando o padrão de URL.

import uuid # Obrigatório para instâncias de livro únicas.

class Genre(models.Model):
    """Modelo que representa o gênero de um livro."""
    name = models.CharField(max_length=200, 
        help_text="Informe um gênero de livro (exemplo: Ficção Científica).",
        verbose_name='Nome'
    )

    def __str__(self):
        """String para representação do objeto de Modelo. """
        return self.name

class Book(models.Model):
    """Modelo que representa um livro, mas não uma cópia específica do livro."""
    title = models.CharField(max_length=200, verbose_name='Título')

    # Chave estrangeira usada porque um livro pode ter apenas um autor, mas
    # um autor pode ter vários livros.
    # A classe Author está como string ao invés de objeto porque ela ainda 
    # não foi declarada no arquivo.
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, 
        help_text="Informe uma breve descrição do livro.",
    )
    isbn = models.CharField('ISBN', max_length=13, 
        help_text='13 caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'
    )
    # Usamos um campo ManyToMany porque um gênero pode conter muitos livros.
    # Livros podem conter vários gêneros.
    # A classe Genre já foi definida, então podemos especificar o objeto acima.
    genre = models.ManyToManyField(Genre, 
        help_text='Selecione um gênereo para este livro',
    )

    def __str__(self):
        """String para representar o objeto de Modelo."""
        return self.title

    def get_absolute_url(self):
        """Retorna a URL para acessar o registro dos detalhes para este livro"""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Modelo que representa uma cópia específica de um livro (por exemplo 
    que pode ser emprestado da biblioteca."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, 
        help_text='ID único para este livro particular na biblioteca.'
    )
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String para representar o objeto de Modelo."""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Modelo que representa um autor"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Retorna a URL que acessa a instância do autor."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String para representar o objeto de Modelo."""
        return f'{self.last_name}, {self.first_name}'
