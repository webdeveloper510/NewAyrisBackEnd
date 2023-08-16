from rest_framework.routers import DefaultRouter

from machine.views import (
MachineViewSet,
MyMachineViewSet,
MyObjectsNameViewSet
)
from accounts.views import (
UserViewSet,
ProfileViewSet,
MyUserProfileViewSet
)
from buildx.views import BuildViewSet
from category.views import (
CategoryViewSet,
MenuCategoryViewSet
)
from post.views import PostViewSet

from prefered.views import (
UserPreferenceViewSet
)

from artworks.views import (
ArtsWorksViewSet
)

router = DefaultRouter()
router.register('machines', MachineViewSet, basename='machines')
router.register('machine', MyMachineViewSet, basename='machine')

router.register('categories', CategoryViewSet, basename='categories')
router.register('menu', MenuCategoryViewSet, basename='menu')


router.register('arts_works', ArtsWorksViewSet, basename='arts_works')

router.register('users', UserViewSet, basename='users')

router.register('profile', MyUserProfileViewSet, basename='profile')
router.register('profiles', ProfileViewSet, basename='profiles')

router.register('user_pref', UserPreferenceViewSet, basename='user_pref')
#
router.register('builds', BuildViewSet, basename='builds')
router.register('objects_name', MyObjectsNameViewSet, basename='objects_name')

router.register('posts', PostViewSet, basename='posts')

urlpatterns = router.urls
