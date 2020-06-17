from rest_framework.routers import DefaultRouter

from role.views import RoleViewSet

router = DefaultRouter()
router.register(r'', RoleViewSet)

urlpatterns = router.urls
