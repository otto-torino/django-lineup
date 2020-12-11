from mptt.managers import TreeManager


class MenuItemManager(TreeManager):

    def enabled(self, *args, **kwargs):
        return self.filter(*args, enabled=True, **kwargs)
