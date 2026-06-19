from asset import Asset
from task import STATUS_ORDER

class Owner:
    def __init__(self, name):
        self.name = name
        self.assets = []

    def add_asset(self, asset):
        if not isinstance(asset, Asset):
            raise TypeError("asset must be a Asset instance")
        for existing in self.assets:
            if existing.name == asset.name:
                raise ValueError(f"a asset name '{asset.name}' already exists")
        self.assets.append(asset)

    def status(self):
        if not self.assets:
            return "ok"
        statuses = []
        for asset in self.assets:
            statuses.append(asset.status())
        return max(statuses, key=lambda s: STATUS_ORDER.index(s))

    def assets_by_status(self, target):
        if target not in STATUS_ORDER:
            raise ValueError(f"target must be one of {STATUS_ORDER}")
        result = {}
        for asset in self.assets:
            matching = asset.components_by_status(target)
            if matching:
                result[asset.name] = matching
        return result

    def delete_asset(self, name):
        for asset in self.assets:
            if asset.name == name:
                self.assets.remove(asset)
                return
        raise ValueError(f"no asset name '{name}' was found")

    def report(self):
        return {asset.name: asset.report() for asset in self.assets}
