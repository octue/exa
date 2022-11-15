# from django.db.models import FileField, Model, TextField
# from django_gcp.storage.fields import DirectUploadFileField


# class ExampleStorageModel(Model):
#     """
#     An example model containing direct and normal file uploads

#     """

#     direct_file = DirectUploadFileField(upload_to="direct_uploads_final_destination", blank=True, null=True)
#     normal_file = FileField(upload_to="normal_uploads", blank=True, null=True)

#     class Meta:
#         """Metaclass defining this model to reside in the example app"""

#         app_label = "example"
