def recolocarTexto(referencia, textoOriginal, substituicao):
  texto = textoOriginal
  if referencia in textoOriginal:
    texto = textoOriginal.replace(referencia, substituicao)
  return texto