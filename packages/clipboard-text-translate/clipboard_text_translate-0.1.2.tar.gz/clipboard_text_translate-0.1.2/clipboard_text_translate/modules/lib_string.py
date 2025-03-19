def split_text(texto, max_size=10000, separators=["\n\n", ".", "!", "?"]):
    partes = []
    inicio = 0

    while inicio < len(texto):
        if len(texto) - inicio <= max_size:
            partes.append(texto[inicio:])
            break

        fim = inicio + max_size
        melhor_corte = -1
        melhor_sep = ""

        for sep in separators:
            pos = texto.rfind(sep, inicio, fim)
            if pos > melhor_corte:
                melhor_corte = pos
                melhor_sep = sep

        if melhor_corte == -1:
            fim = inicio + max_size  # Corta no limite se nenhum separador for encontrado
        else:
            fim = melhor_corte + len(melhor_sep)  # Inclui o separador no corte

        partes.append(texto[inicio:fim])
        inicio = fim

    return partes
