from django.db import models

import post.models as post_model


class PostManager(models.Manager):

    def create(self, **kwargs):
        print("self : ", self)
        print("kwargs : ", kwargs)


        raise Exception("create")
        return super().create(**kwargs)




class PostQuerySet(models.QuerySet):
    def create(self, **kwargs):
        print("self : ", self)
        print("kwargs : ", kwargs)


        raise Exception("create")
        return super().create(**kwargs)
