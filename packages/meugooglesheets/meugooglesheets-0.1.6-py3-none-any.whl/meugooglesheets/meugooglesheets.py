from gspread import authorize
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep
import logging
logging.basicConfig(level=logging.WARNING)
class GoogleSheet:
    def __init__(self,  CREDENCIAL, KEY, PAGINA ):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict = CREDENCIAL, scopes = scope)
        client = authorize(creds)
        sheet = client.open_by_key(KEY)
        self.worksheet = sheet.worksheet(PAGINA)

    def Ler_celulas_listas(self, intervalo = "A1:z"):
        return self.worksheet.get(intervalo)

    def Inserir_listas(self, valor:list[list], intervalo = "A1:z"):
        self.worksheet.update(valor, intervalo)

    def Inserir_valor(self, linha = 1, coluna = 1,valor:str |int = 1):
        self.worksheet.update_cell(linha, coluna, f'{valor}')  

    def LocalizarCelulas(self, palavra):
        return self.worksheet.findall(palavra)

    def Inserir_na_planilha(self, valor:list[list], cell_init = None):
        def generate_interval_string(start_cell, num_cols, num_rows):
            def increment_column(col):
                # Incrementar a string da coluna (por exemplo, 'A' -> 'B', 'Z' -> 'AA')
                if col[-1] != 'Z':
                    return col[:-1] + chr(ord(col[-1]) + 1)
                else:
                    if len(col) == 1:
                        return 'AA'
                    else:
                        return increment_column(col[:-1]) + 'A'    
            # Extrair a parte da coluna e a parte da linha da célula inicial
            start_col = ''.join(filter(str.isalpha, start_cell))
            start_row = int(''.join(filter(str.isdigit, start_cell)))
            
            # Calcular a coluna final
            end_col = start_col
            for _ in range(num_cols - 1):
                end_col = increment_column(end_col)
            
            # Calcular a linha final
            end_row = start_row + num_rows -1
            
            # Formar a string do intervalo
            return f"{start_col}{start_row}:{end_col}{end_row}"
        
        
        if not cell_init:
            linha_inicial = None
            linha_inicial = len(self.worksheet.get("A1:Z"))
            while linha_inicial is None:
                sleep(0.5)
            cell_init = f'A{linha_inicial+1}'
        logging.warning(f'linha inicial: {linha_inicial}')
        v = valor.copy()
        num_rows = len(v)
        num_cols = max(list(map(lambda x: len(x), v))) 
        intervalo = generate_interval_string(cell_init,num_cols,num_rows)
        self.worksheet.update(v, intervalo)
        return 'dados inseridos!'
