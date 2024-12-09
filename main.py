import pandas as pd

class CBR():
    class _Menu():
        def __init__(self, menu: pd.DataFrame):
            energy, carb, protein, fat, fiber, vitC, vitD, vitE = 0, 0, 0, 0, 0, 0, 0, 0
            for _, value in menu.iterrows():
                energy += value['energia2_media']
                carb += value['carboidrato_disponivel_media']
                protein += value['proteina_media']
                fat += value['lipidios_media']
                fiber += value['fibra_alimentar_media']
                vitC += value['vitamina_C_media']
                vitD += value['vitamina_D_media']
                vitE += value['vitamina_E_media']

            self.menu = menu
            self.energy = energy
            self.nutrient_table = {'carb': carb, 'protein': protein, 'fat': fat, 'fiber': fiber, 'vitC': vitC, 'vitD': vitD, 'vitE': vitE}

        def __repr__(self):
            nutrient_table = f'''
Tabela Nutricional:\n---------------------------
Energia: {self.energy} kcal
Carboidratos: {self.nutrient_table['carb']} g
Proteinas: {self.nutrient_table['protein']} g
Lipidios: {self.nutrient_table['fat']} g
Fibras: {self.nutrient_table['fiber']} g
Vitamina C: {self.nutrient_table['vitC']} g
Vitamina D: {self.nutrient_table['vitD']} g
Vitamina E: {self.nutrient_table['vitE']} g\n
Alimentos:\n---------------------------
'''
            foods = ''
            index = 0
            for _, value in self.menu.iterrows():
                if index < 5:
                    foods += f'Alimento {index + 1}: {self.menu.iloc[index]["nome_pt_br"]}\n'
                else:
                    foods += f'Alimento Adicionado {index + 1}: {self.menu.iloc[index]["nome_pt_br"]}\n'
                index += 1
            return nutrient_table + foods

    def __init__(self):
        self.foods = self._load_data()
        self.case_library = [self._generate_case(self.foods) for _ in range(10)]
        print(self.case_library[0])

    def _load_data(self):
        foods = pd.read_excel('alimentos.xlsx')
        groups = pd.read_excel('grupos.xlsx')
        nutrients = pd.read_excel('alimento_nut_all.xlsx')

        foods['cod_alimento'] = foods['cod_alimento'].str.replace('BR', '')

        foods = foods.merge(groups, left_on='grupo_id', right_on='id').drop('id', axis='columns')
        foods = foods.merge(nutrients, on='cod_alimento')

        return foods

    def _generate_case(self, foods: pd.DataFrame):
        protein = foods[foods["nm_grupo_br"].isin(['Carnes e derivados', 'Pescados e frutos do mar', 'Ovos e derivados'])].sample(1)
        vegetables = foods[foods["nm_grupo_br"].isin(['Vegetais e derivados', 'Leguminosas e derivados'])].sample(2)
        carb  = foods[foods["nm_grupo_br"].isin(['Cereais e derivados'])].sample(1)
        drink = foods[foods["nm_grupo_br"] == 'Bebidas '].sample(1)

        menu = pd.concat([protein, vegetables, carb, drink])
        
        return self._Menu(menu)
         

if __name__ == '__main__':
    cbr = CBR()