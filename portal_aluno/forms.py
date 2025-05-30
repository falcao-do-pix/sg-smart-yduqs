from django import forms

class AlunoRegisterForm(forms.Form):
    nome = forms.CharField(
        label='Nome completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Seu nome completo'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'exemplo@email.com'
        })
    )
    matricula = forms.CharField(
        label='Matrícula',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Número da matrícula'
        })
    )
    senha = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': '********'
        })
    )
    curso = forms.CharField(
        label='Curso',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'Nome do curso'
        }),
        required=False
    )
