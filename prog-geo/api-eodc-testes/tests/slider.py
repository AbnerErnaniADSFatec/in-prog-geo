from ipywidgets import interact

n = eocube_service.getDataCube().time.values
lista =[eocube_service.calculateColorComposition(n[i])[0].values for i in range(1,len(n))]

@interact (date=(1, len(n)-1))
def sliderplot(date):
    plt.figure(figsize=(25, 8))
    plt.imshow((lista[date-1] * 255).astype(np.uint8))
    plt.title('Composição colorida verdadeira');
    print('' \t',datetime.utcfromtimestamp(n[date].tolist()/1e9))
