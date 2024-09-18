#include <iostream>
using namespace std;
<<<<<<< HEAD

int calculadora(int a, int b) {
    char oper;
    std::cin >> oper;
    if (oper=='+')
    {
        return (a+b);
    }
    if (oper=='-')
    {
        return (a-b);
    }
    if (oper=='*')
    {
        return (a*b);
    }
    if (oper=='/')
    {
        return (a/b);
    }
    return 0;
}

int menor(int a, int b)
{
    if (a>b)
    {
        return b;
    }
    else
    {
        return a;
    }
}

void FlizzBuzz()
{
    for (int i=1;i <= 100; i++)
    {

        if (i % 3 == 0)
        {
            if (i % 5 ==0)
            {
                std::cout << "FlizzBuzz" << std::endl;
            }
            else
            {
                std::cout << "Flizz" << std::endl;
            }
        }
        else
        {
            if(i % 5 == 0)
            {
                std::cout << "Buzz" << std::endl;
            }
            else
            {
                std::cout << i << std::endl;
            }
        }
    }
}
void triangulo(int num)
{
    for (int i=0;i<=num;i++,cout << endl)
    {
        for (int j=0;j<i;j++)
        {
            cout << '*';
        }
    }
}
void trianguloReves(int num)
{
    for (int i=0;i<=num;i++,cout << endl)
    {
        for (int j=0;j<num-i;j++)
        {
            cout << ' ';
        }
        for (int j=0;j<i;j++)
        {
            cout << '*';
        }

    }
}
void trianguloVerdad(int num)
{
    for (int i=0;i<=num;i++,cout << endl)
    {
        for (int j=0;j<num-i;j++)
        {
            cout << ' ';
        }
        for (int j=0;j<i;j++)
        {
            cout << '*';
        }
        for (int j=0;j<i;j++)
        {
            cout << '*';
        }


    }
}
int main(){

    trianguloVerdad(4);

    return 0;
}



=======

void Hola()
{
  cout << "hola" << endl;
}

int main()
{
    Hola();
    return 0;
}

>>>>>>> d4dfd3dff1f4ab9994aae7f7117bff207e3949ef
