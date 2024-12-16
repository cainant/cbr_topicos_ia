import pandas as pd
import random as rnd

class Menu:
    def __init__(self, menu: pd.DataFrame):
        self.menu = menu
        self.generate_nutrient_table()

    def __repr__(self):
        nutrient_table = (
            f"Tabela Nutricional:\n"
            f"---------------------------\n"
            f"Energia: {self.energy} kcal\n"
            f"Carboidratos: {self.nutrient_table['carb']} g\n"
            f"Proteínas: {self.nutrient_table['protein']} g\n"
            f"Lipídios: {self.nutrient_table['fat']} g\n"
            f"Fibras: {self.nutrient_table['fiber']} g\n"
            f"Vitamina C: {self.nutrient_table['vitC']} g\n"
            f"Vitamina D: {self.nutrient_table['vitD']} g\n"
            f"Vitamina E: {self.nutrient_table['vitE']} g\n\n"
            f"Alimentos:\n"
            f"---------------------------\n"
        )
        foods = ''
        for index, _ in enumerate(self.menu.iterrows()):
            foods += f'Alimento {index + 1}: {self.menu.iloc[index]["nome_pt_br"]} | {self.menu.iloc[index]["nm_grupo_br"]}\n'
        return nutrient_table + foods

    def generate_nutrient_table(self):
        menu = self.menu
        self.energy = menu['energia2_media'].sum()
        self.nutrient_table = {
            'carb': menu['carboidrato_disponivel_media'].sum(),
            'protein': menu['proteina_media'].sum(),
            'fat': menu['lipidios_media'].sum(),
            'fiber': menu['fibra_alimentar_media'].sum(),
            'vitC': menu['vitamina_C_media'].sum(),
            'vitD': menu['vitamina_D_media'].sum(),
            'vitE': menu['vitamina_E_media'].sum()
        }

class CBR():
    def __init__(self):
        self.foods = self._load_data()
        self.case_library = [self._generate_case(self.foods) for _ in range(10)]

    def _load_data(self):
        foods = pd.read_excel('alimentos.xlsx')
        groups = pd.read_excel('grupos.xlsx')
        nutrients = pd.read_excel('alimento_nut_all.xlsx')

        foods['cod_alimento'] = foods['cod_alimento'].str.replace('BR', '')

        foods = foods.merge(groups, left_on='grupo_id', right_on='id').drop('id', axis='columns')
        foods = foods.merge(nutrients, on='cod_alimento')

        return foods

    def _generate_case(self, foods: pd.DataFrame):
        protein = foods[foods["nm_grupo_br"].isin(['Carnes e derivados', 'Pescados e frutos do mar', 'Ovos e derivados'])].sample(rnd.randint(2, 3))
        vegetables = foods[foods["nm_grupo_br"].isin(['Vegetais e derivados', 'Leguminosas e derivados'])].sample(rnd.randint(2, 4))
        carb  = foods[foods["nm_grupo_br"].isin(['Cereais e derivados'])].sample(rnd.randint(2, 4))
        drink = foods[foods["nm_grupo_br"] == 'Bebidas '].sample(1)

        menu = pd.concat([protein, vegetables, carb, drink])
        return Menu(menu)

    def retrieve(self, energy, threshold):
        filtered_menus = [m for m in self.case_library if energy - threshold <= m.energy <= energy + threshold]

        if len(filtered_menus) == 0:
            print('Nenhum menu encontrado nesta faixa de energia')
            return None
        menu = sorted(filtered_menus, key=lambda m: abs(m.energy - energy))[0]

        print(f'MENU ORIGINAL\n{menu}')
        menu = Menu(menu.menu)
        return self.reuse(menu, energy, threshold)
    
    def reuse(self, menu: Menu, energy, threshold):
        to_change = menu.menu.sample(1).iloc[0]
        to_change_group = to_change['grupo_id']

        new_food = self.foods[(self.foods['grupo_id'] == to_change_group) & (~self.foods['cod_alimento'].isin(menu.menu['cod_alimento']))].sample(1)

        if not new_food.empty:
            print(f"Substituindo: {to_change['nome_pt_br']} ({to_change['nm_grupo_br']}) por {new_food.iloc[0]['nome_pt_br']} ({new_food.iloc[0]['nm_grupo_br']})")
            menu.menu = menu.menu[menu.menu['cod_alimento'] != to_change['cod_alimento']]
            menu.menu = pd.concat([menu.menu, new_food])

        if self.revise(menu, energy, threshold) == None:
            self.reuse(menu, energy, threshold)

        return menu

    def revise(self, menu: Menu, energy, threshold):
        menu.generate_nutrient_table()

        if (energy - threshold <= menu.energy <= energy + threshold):
            print(f'NOVO MENU\n{menu}')
            self.retain(menu)
            return menu
        else:
            return None

    def retain(self, menu):
        self.case_library.append(menu)

if __name__ == '__main__':
    cbr = CBR()
    energia1_med = int(input("Digite a energia média: "))
    limiar = int(input("Digite o limiar de energia: "))
    menu = cbr.retrieve(energia1_med, limiar)
    
