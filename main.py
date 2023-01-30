 ########################################################################################################
########################################################################################################
########################################################################################################
#######Rotina desenvolvida conforme o protocolo harmonizado, disponível em português no link: #######
####https://www.gov.br/inmetro/pt-br/centrais-de-conteudo/publicacoes/protocolo-harmonizado-ct5.pdf####
########################################################################################################
########################################################################################################
########################################################################################################

import pandas as pd
from statsmodels.stats.contingency_tables import cochrans_q
from scipy.stats import chi2, f
import numpy as np

R1 = np.array([10.5000,9.6000,10.4000,9.5000,10.0000,9.6000,9.8000,9.8000,10.8000,10.2000,9.8000,10.2000])
R2 = np.array([10.4000,9.5000,9.9000,9.9000,9.7000,10.1000,10.4000,10.2000,10.7000,10.0000,9.5000,10.0000])
sigmap=1.140

###
###
###Teste de Cochran, para outliers nas duplicatas
###(deve ser realizado)
###
###

dic = {1:R1, 2:R2}
df = pd.DataFrame(dic)
m = (len(R1)+len(R2))/2

df['Di2'] = (df[1] - df[2])**2
sum_Di2 = df['Di2'].sum()
max_Di2 = df['Di2'].max()
coch_cal = max_Di2/sum_Di2

# Encontrando Cochran tabelado (não tem função no Python para calcular o C de Cochran. Não confundir com Q de Cochran!!!)
tabela = [0.967,0.906,0.841,0.781,0.727,0.68,0.638,0.602,0.57,0.541,0.515,0.492,0.471,0.452,0.434,0.418,0.403,0.389]
index = int(m) - 3
coch_tab = tabela[index]

if coch_cal <= coch_tab:
    print("Não deve ser removida nenhuma duplicata")
    ###
    ###Teste de homogeneidade, conforme o Protocolo Harmonizado (se Cochran validar, então deve ser realizado como abaixo)
    ###
    ##
    
    # Cálculo da Variação Analítica
    s2an = sum_Di2 / (2*m)

    ###Cálculo da Variação Amostral
    si = R1+R2
    Vs = np.var(si, ddof=1)
    s2sam =((Vs/2)-s2an)/2

    ###Cálculo do Valor Crítico
    F1 = chi2.ppf(0.95, m-1) / (m-1)
    F2 = (f.isf(0.05, m-1, m)-1) / 2
    C = (F1*(0.3*sigmap)**2)+(F2*s2an)

    ###Decisão Final
    dec = "aprovada" if s2sam<=C else "reprovada"
    print(f'''
A variância amostral foi de {round(s2sam,4)}
A variância do EP foi de {round((sigmap**2),4)}
O valor crítico foi de {round(C,4)}
Homogeneidade foi {dec} segundo o protocolo harmonizado
    ''')

else:
    print("A duplicata de maior diferença deve ser removida")

