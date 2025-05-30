from datetime import datetime
from alunos.models import RegistroFrequencia
from django.core.mail import send_mail

def verificar_atrasos():
    agora = datetime.now()
    if agora.hour >= 19:  # Apenas verifica após as 19h
        atrasados = RegistroFrequencia.objects.filter(data__date=agora.date(), atrasado=True)

        if atrasados.exists():
            lista_alunos = "\n".join([f"{a.aluno.nome} - {a.aluno.matricula}" for a in atrasados])
            mensagem = f"Os seguintes alunos estão atrasados hoje:\n\n{lista_alunos}"

            # Enviar email para administrador
            send_mail(
                "Alunos Atrasados - Relatório Diário",
                mensagem,
                "sistema@exemplo.com",
                ["admin@escola.com"],
            )

            print("🔔 Alerta enviado!")
        else:
            print("✅ Nenhum aluno atrasado hoje.")
