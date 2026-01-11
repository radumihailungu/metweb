from django.db import models

class ArtObject(models.Model):
    data = models.JSONField()

    #accesam tabel deja existent in mysql
    class Meta:
        db_table = "data"

    #creeam functii ca sa le apelam usor pt datele din db
    @property
    def title(self):
        return self.data.get("title", "")

    @property
    def artist(self):
        return self.data.get("artistDisplayName", "")

    @property
    def department(self):
        return self.data.get("department", "")

    @property
    def image_data_uri(self):
        return self.data.get("image", "")
