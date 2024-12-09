import pandas as pd

class CBR():
    def __init__(self):
        self._load_data()
        self._generate_case_library()

    def _load_data(self):
        foods = pd.read_excel('alimentos.xlsx')
        groups = pd.read_excel('grupos.xlsx')
        nutrients = pd.read_excel('alimento_nut_all.xlsx')

        foods['cod_alimento'] = foods['cod_alimento'].str.replace('BR', '')

        foods = foods.merge(groups, left_on='grupo_id', right_on='id').drop('id', axis='columns')
        foods = foods.merge(nutrients, on='cod_alimento')

        self.foods = foods

    def _generate_case_library(self):
        def _generate_case(foods: pd.DataFrame):
            protein = foods[foods["nm_grupo_br"].isin(['Carnes e derivados', 'Pescados e frutos do mar', 'Ovos e derivados'])].sample(1)
            vegetables = foods[foods["nm_grupo_br"].isin(['Vegetais e derivados', 'Leguminosas e derivados'])].sample(2)
            carb  = foods[foods["nm_grupo_br"].isin(['Cereais e derivados'])].sample(1)
            drink = foods[foods["nm_grupo_br"] == 'Bebidas '].sample(1)

            return pd.concat([protein, vegetables, carb, drink])
        
        self.case_library = [_generate_case(self.foods) for _ in range(10)]


if __name__ == '__main__':
    cbr = CBR()