
/* Método auxiliar que comprueba si el año pasado como parámetro
es bisiesto
 */
bool Fecha::esBisiesto(int a) const{
   return (a%4 ==0) && (a%100!=0 || (a%100==0 && a%400==0));
}

/* Método auxiliar que devuelve el día de la semana de la fecha actual
0=lunes, 6=domingo
 */
int Fecha::obtenerDiaSemana() const{
   int diasT=0;
   for(int a=1900; a < anyo; a++)
       if(esBisiesto(a))
           diasT+=366;
       else
           diasT+=365;
   for(int m=1; m< mes; m++)
       diasT+=calculaDiasMes(m,anyo);
   
   diasT+=(dia-1);
   
   return diasT % 7;
}


/* Método auxiliar que comprueba si la fecha actual es un día festivo */
bool Fecha::esFestivo() const{
    if((dia == 1 && mes==1) || (dia == 6 && mes==1) || (dia==1 && mes==5) || (dia==15 && mes==8) || (dia==12 && mes==10) || (dia==1 && mes==11) || (dia==6 && mes==12) || (dia==25 && mes==12) )
        return true;
    else
        return false;
 }

/* Cuántos días faltan hasta el principio del siguiente puente */
   int Fecha::diasHastaSiguientePuente() const{
      int transcurridos=0;
      Fecha f(*this);
      
      /* Si estamos en fin de semana, hay qu comprobar 
      si el viernes es festivo.
      En caso afirmativo, estaremos en un puente y habrá que devolver 0*/
      if( f.obtenerDiaSemana() >=5 )
      {
           //Comprobar si el viernes es festivo
           if(f.obtenerDiaSemana() ==5){
              Fecha f2(f);
              f2.incrementaDias(-1);
              if(f2.esFestivo())
                  return 0;
           }else{
              Fecha f2(f);
              f2.incrementaDias(-2);
              if(f2.esFestivo())
                  return 0;
           }
      }
      
      /* Incrementamos la fecha f hasta llegar a un día festivo que es lunes o viernes
         Contamos el número de incrementos realizados
       */
      while( !( f.esFestivo() && (f.obtenerDiaSemana()==0 || f.obtenerDiaSemana()==4) ) ){
          transcurridos++;
          f.incrementaDias(1);
      }
      
      /*
      Si el festivo es lunes, el comienzo del puente será dos días antes (sábado)
      */
      if( f.obtenerDiaSemana()==0)
          transcurridos-=2;
      
      /* Podemos obtener un número menor que 0 si, por ejemplo, estamos en
      domingo, y el día siguiente (lunes) es festivo. En ese caso, devolvemos 0 
      porque ya estamos dentro del puente
       */
      if(transcurridos <0)
          transcurridos=0;
     
     return transcurridos;
  
  }
