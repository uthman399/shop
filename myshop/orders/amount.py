
class Amount:
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
