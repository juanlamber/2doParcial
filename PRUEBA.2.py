
import sympy as sp
#NOTA importar el modulo sympy como:  pip3 install sympy (MAC)

#PUNTO 1: Constante de red K

D= sp.Symbol('x')
y= sp.Symbol('y')
z= sp.Symbol('z')
k= (1/(6.328e-5))*(y/((y**2+D**2)**(1/2)))
kfinal= k.subs([(D,182),(y,74.75)])

ksegx=sp.diff(k,D)
ksegy=sp.diff(k,y)

errork = sp.sqrt(((ksegx.subs([(D,182), (y,74.75)]))*0.1)**2+((ksegy.subs([(D,182), (y,74.75)]))*0.435)**2)

print('\n------------')

print('K = (',kfinal, '±', errork, ') 1/cm')

print('------------ \n')


#PUNTO 2: Calculo de longitud de onda del espectro de emitido por luz proveniente de una lámpara de mercurio

lamgral= (1/(z))*(y/((y**2+D**2)**(1/2)))
lazul= lamgral.subs([(y, 3.1), (D, 11.5), (z, 6009)])
lverde= lamgral.subs([(y, 3.9), (D, 11.5), (z, 6009)])
lnar= lamgral.subs([(y, 4.2), (D, 11.5), (z, 6009)])

lazul*=1e+7
lverde*=1e+7
lnar*=1e+7

lamsegx=sp.diff(lamgral,D)
lamsegy=sp.diff(lamgral,y)
lamsegz=sp.diff(lamgral,z)


errorazul = ((lamsegz.subs([(D,11.5), (y,3.1), (z, 6009)])* (20))**2 +(lamsegx.subs([(D,11.5), (y,3.1), (z, 6009)])*0.1)**2+(lamsegy.subs([(D,11.5), (y,3.1), (z, 6009)])*0.1)**2)**(1/2)
errorverde = ((lamsegz.subs([(D,11.5), (y,3.9), (z, 6009)])* (20))**2 +(lamsegx.subs([(D,11.5), (y,3.9), (z, 6009)])*0.1)**2+(lamsegy.subs([(D,11.5), (y,3.9), (z, 6009)])*0.1)**2)**(1/2)
errornaranja = ((lamsegz.subs([(D,11.5), (y,4.2), (z, 6009)])* (20))**2 +(lamsegx.subs([(D,11.5), (y,4.2), (z, 6009)])*0.1)**2+(lamsegy.subs([(D,11.5), (y,4.2), (z, 6009)])*0.1)**2)**(1/2)

errorazul*=1e+7
errorverde*=1e+7
errornaranja*=1e+7

print(('lambda azul= ({} ± {})nm,\n\n-----------------------------\n\nlambda verde = ({} ± {})nm,\n\n-----------------------------\n\nlambda naranja = ({} ± {})nm,\n\n-----------------------------\n\n').format(lazul, errorazul, lverde, errorverde, lnar, errornaranja))