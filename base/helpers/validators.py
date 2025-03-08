import os  
from django.core.exceptions import ValidationError



def file_size_validator(value): # add this to some file where you can import it from
    limit = 3 * 1024 * 1024
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.pdf', '.png', '.jpeg']
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 5 MiB.')
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')