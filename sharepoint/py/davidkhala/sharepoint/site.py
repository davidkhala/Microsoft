from office365.onedrive.sites.site import Site as RawSite


class Site:
    def __init__(self, site: RawSite):
        self._ = site
        self._.get().execute_query()

    @property
    def drives(self):
        return self._.drives.get().execute_query()

    def drive_id(self, name: str):
        return next((d.id for d in self.drives if d.name == name), None)
