from rest_framework.routers import DefaultRouter

from api.views import experiment_1, experiment_2, experiment_3

router = DefaultRouter()
router.register("experiments/1/items", experiment_1.DemoApiViewSet, "demo-1")
router.register("experiments/2/items", experiment_2.DemoApiViewSet, "demo-2")
router.register("experiments/3/items", experiment_3.DemoApiViewSet, "demo-3")

urlpatterns = router.urls
