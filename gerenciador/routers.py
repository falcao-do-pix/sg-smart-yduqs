class PresencaRouter:
    """
    Roteador para direcionar o modelo Presenca para o banco 'postgres'.
    """

    route_app_labels = {'gerenciador'}  # Substitua pelo nome do seu app se diferente

    def db_for_read(self, model, **hints):
        if model.__name__ == "Presenca":
            return 'presenca_postgres'
        return None

    def db_for_write(self, model, **hints):
        if model.__name__ == "Presenca":
            return 'presenca_postgres'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.model_name == "presenca" or obj2._meta.model_name == "presenca":
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name == "presenca":
            return db == 'presenca_postgres'
        elif db == 'presenca_postgres':
            return False
        return None
