#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#ifdef _OPENMP
  #include <omp.h>
#else
  #define omp_get_thread_num() 0
  #define omp_get_num_threads() 1 
#endif

/* Como compilar

gcc -o 61_integralPar_Crit integralPar_Crit.c -Wall -lm -fopenmp -O2    // Para f(x) com 4096 trapézios
gcc -o 62_integralPar_Crit integralPar_Crit.c -Wall -lm -fopenmp -O2    // Para g(x) com 4096 trapézios
gcc -o 63_integralPar_Crit integralPar_Crit.c -Wall -lm -fopenmp -O2    // Para fg(x) com 4096 trapézios

gcc -o 71_integralPar_Crit integralPar_Crit.c -Wall -lm -fopenmp -O2    // Para f(x) com 40960 trapézios
gcc -o 72_integralPar_Crit integralPar_Crit.c -Wall -lm -fopenmp -O2    // Para g(x) com 40960 trapézios
gcc -o 73_integralPar_Crit integralPar_Crit.c -Wall -lm -fopenmp -O2    // Para fg(x) com 40960 trapézios

*/

double f (double x);
double g (double x);
double fg (double x);

int main(){

    double start = omp_get_wtime();
    double integral = 0.0, a= 0.0, b= 1.0, h;

    double expected = 1.33333333333333333333;    // Para f(x)
    // double expected = -0.9567460317460317;       // Para g(x)
    // double expected = -9042.912592905755;        // Para fg(x)

    int n = 4096;    // Para executáveis que começam com números pares
    // int n = 40960;   // Para executáveis que começam com números ímpares

    h = (b - a)/n;
    #pragma omp parallel
    {   
        double integral_loc = 0.0;
        #pragma omp for
        for(int i = 1; i < n ; i++){
            integral_loc += f(a + i*h);
        }
        #pragma omp atomic
        integral += integral_loc;
    } 
    integral += (f(a) + f(b))/2;
    integral *= h;

    printf("Estimativa com %d trapezios\n", n);
    printf("Integral = %.20lf\n", integral);
    printf("Diff = %.20lf\n", fabs(fabs(integral) - fabs(expected)));
    double stop = omp_get_wtime();
    printf("Tempo total: %.6lf\n", stop -start);
    return 0;
}

// Calcuradora de integrais: https://www.integral-calculator.com/

// Para o site: x^2 + 1
// a=0, b=1 -> integral = 1.3333333333333
double f(double x){
    return x*x + 1.0;
}

// Para o site: x^8 + x^7 - x^6 + x^5 + x^4 - x^3 + x^2 + x - 2
// a=0, b=1 -> integral = −0.9567460317460317
double g(double x){
    return pow(x,8) + pow(x,7) - pow(x,6) + pow(x,5) + pow(x,4) - pow(x,3) + pow(x,2) + x - 2;
}

// Para o site: 999*sin(9999*x)*x^8 + sqrt(999*x^7) - cos(9999*x)*999*x^6 + 999*x^5 + 999*x^4 - 999*x^3 + 999*x^2 + 999*x - 9999
// a=0, b=1 -> integral = -9042.912592905755
double fg(double x){
    return 999*sin(9999*x)*pow(x,8) + sqrt(999*pow(x,7)) - cos(9999*x)*999*pow(x,6) + 999*pow(x,5) + 999*pow(x,4) - 999*pow(x,3) + 999*pow(x,2) + 999*x - 9999;
}