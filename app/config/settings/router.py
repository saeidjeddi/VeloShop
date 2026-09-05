class DatabaseRouter:

    primary_apps = {
        "accounts",
        "auth",
        "contenttypes",
        "admin",
        "sessions",
    }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.primary_apps:
            return "default"

        return "replica"

    def db_for_write(self, model, **hints):
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"