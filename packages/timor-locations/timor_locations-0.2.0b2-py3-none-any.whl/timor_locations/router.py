from geojson_pydantic import FeatureCollection
from ninja import Router

from timor_locations import models, schemas

router = Router(tags=["Timor GIS"])


@router.get("/area/list.json", response=list[schemas.AreaOut])
def area_list(request):
    """
    Returns a list of area information: type, name, id, parent id
    """
    return [
        *(
            dict(name=instance.name, type="Municipality", pcode=instance.pcode)
            for instance in models.Municipality.objects.all()
        ),
        *(
            dict(name=instance.name, type="Administrative Post", pcode=instance.pcode, parent=instance.municipality_id)
            for instance in models.AdministrativePost.objects.all()
        ),
        *(
            dict(name=instance.name, type="Suco", pcode=instance.pcode, parent=instance.adminpost_id)
            for instance in models.Suco.objects.all()
        ),
    ]


@router.get("/sucos.json", response=FeatureCollection)
def sucos(request):
    return models.Suco.objects.as_feature_collection()


@router.get("/admin_posts.json", response=FeatureCollection)
def admin_posts(request):
    return models.AdministrativePost.objects.as_feature_collection()


@router.get("/municipalities.json", response=FeatureCollection)
def municipalities(request):
    return models.Municipality.objects.as_feature_collection()


# The following endpoints require appropriate data in the database
# See the `create_topology` command


@router.get("/{slug}.topojson", response=schemas.Topology)
def original_topojson(request, slug: str):
    return models.TopoJson.objects.get(pk=slug).topology
