from django.db import models

def event_image_file_path(instance, filename):
    """Generates a unique file path for event images by appending a timestamp."""
    ext = filename.split('.')[-1]
    filename = f'{instance.name}_{datetime.now().strftime("%Y%m%d%H%M%S")}.{ext}'
    return os.path.join('events/', filename)

class UploadedFile(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    file = models.FileField(upload_to='uploads/', verbose_name="Documento")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Configuracion"
        verbose_name_plural = "Configuraciones"
        db_table = 'sumate_configuracion'