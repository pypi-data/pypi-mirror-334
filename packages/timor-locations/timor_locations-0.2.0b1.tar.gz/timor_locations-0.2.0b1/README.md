# Timor GIS

Timor Leste GIS data as Django models

This initial release uses administrative boundariew from Estrada, tweaked to include Atauro as a separate entity, with pcodes which are intended to match existing data from PNDS.

Data inputs are stored as `gpkg` files in Git LFS.

You may need to run something like

`apt install git-lfs` and `git lfs install`

(or equivalent for your OS)

## Environment

This is intended to be compatible with:

- Django 4.1+
- Python 3.10+

```sh
gh repo clone catalpainternational/timor_locations
cd timor_locations
uv sync
```

## Manually Uploading a new version to PyPi

Bump `pyproject.toml`
Then run `uv build` and `uv publish`

```bash
uv build
uv publish
```

There is a token which may or may not work
(scoped only to TimorGIS:)

pypi-AgEIcHlwaS5vcmcCJGJlMjJlMTU1LTM3YWMtNDljYy04ZGUyLWQ3ZjdlYWRiYjRiMwACF1sxLFsidGltb3ItbG9jYXRpb25zIl1dAAIsWzIsWyI0NmVmYjY0Mi04YzQ5LTQ2ZjYtYThmZi02NjdmYzNkOWNiMWEiXV0AAAYgbhoTrQvgdpiYpZ0pOvEcYYihiXkBEPc3yefm2Fv34uU
