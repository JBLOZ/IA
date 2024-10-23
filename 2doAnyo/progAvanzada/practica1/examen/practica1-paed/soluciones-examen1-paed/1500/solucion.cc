
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

/* Días laborables transcurridos desde el inicio de curso */
 int Fecha::diasLaborablesTranscurridos() const
 {
     int transcurridos=0;
  
     /* Cálculo de la fecha de inicio de curso */   
     Fecha inicioCurso;
     if(mes <=8)
         inicioCurso.setAnyo(anyo-1);
     else
         inicioCurso.setAnyo(anyo);
     inicioCurso.setDia(1);
     inicioCurso.setMes(9);
     
     /* Incremento, de un día en un día, la fecha de inicio de curso
     hasta llegar a la fecha actual
      */
     while( !( inicioCurso == (*this) ) ){
         if(!inicioCurso.esFestivo() && inicioCurso.obtenerDiaSemana()>=0 && inicioCurso.obtenerDiaSemana()<=4)
             transcurridos++;
         inicioCurso.incrementaDias(1);
     }
     return transcurridos;
 }
