class MaterialList:
    def __init__(self):
        self.materials = {}

    def add_material(self, name, price_per_unit, unit):
        self.materials[name] = {'price_per_unit': price_per_unit, 'unit': unit}

    def edit_material(self, old_name, new_name, new_price_per_unit, new_unit):
        if old_name in self.materials:
            del self.materials[old_name]
            self.materials[new_name] = {'price_per_unit': new_price_per_unit, 'unit': new_unit}

    def delete_material(self, name):
        if name in self.materials:
            del self.materials[name]

    def get_materials(self):
        return self.materials

    def get_material_price(self, name):
        if name in self.materials:
            return self.materials[name]['price_per_unit']
        return 0

    def get_material_unit(self, name):
        if name in self.materials:
            return self.materials[name]['unit']
        return ''