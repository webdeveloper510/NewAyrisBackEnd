from django.core.management.base import BaseCommand

import post.models as post_model


class Command(BaseCommand):
    help = "To remove all posts"

    def handle(self, *args, **kwargs):

        posts = post_model.Post.objects.all()
        if posts:
            count = posts.count()
            posts.delete()

            self.stdout.write(self.style.SUCCESS(f"{count} Post removed: "))
        else:
            self.stdout.write(self.style.ERROR(f"No Post to remove"))

