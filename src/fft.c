#include <stdlib.h>
#include "fft.h"
#include "math.h"
#include "omp.h"

// max is non inclusive
int bit_reverse(int a, int max) {
  int reverse = 0;
  while (a > 0) {
    max = max >> 1;
    if (a % 2 == 1) {
      reverse+=max;
    }
    a = a >> 1;
  }
  return reverse;
}

int num_bits(int n) {
  int count = 0;
  while (n > 0) {
    n = n >> 1;
    count++;
  }
  return count;
}

void dft(struct Complex a[], int length) {
  struct Complex *transforms = malloc(sizeof(struct Complex)*length);

  for (int i = 0; i<length; i++) {
    double re = 0;
    double im = 0;
    for (int j = 0; j<length; j++) {
      double wn_r = cos(2*M_PI*i*j/length);
      double wn_i = -sin(2*M_PI*i*j/length);

      re += wn_r*a[j].real - wn_i*a[j].imaginary;
      im += wn_r*a[j].imaginary + wn_i*a[j].real;
    }
    struct Complex t = {re, im};
    transforms[i] = t;
  }

  for (int i = 0; i<length; i++) {
    a[i] = transforms[i];
  }

  free(transforms);
}

/*void transpose(int rows, int cols, struct Complex a[rows][cols]) {

}

void fft2(int rows, int cols, struct Complex a[rows][cols]) {

}*/

// Only works on powers of 2
void fft(struct Complex a[], int length) {
  // bit reverse
  #pragma omp parallel for
  for (int i = 0; i<length; i++) {
    int swap_index = bit_reverse(i, length);
    if (swap_index < i) {
      struct Complex temp = a[i];
      a[i] = a[swap_index];
      a[swap_index] = temp;
    }
  }

  // fft
  // Compute w_ns that will be used throughout
  struct Complex *w_ns = malloc(sizeof(struct Complex)*length);
  #pragma omp parallel for
  for (int k = 0; k<length; k++) {
    w_ns[k].real = cos(2*M_PI*k/length);
    w_ns[k].imaginary = -sin(2*M_PI*k/length);
  }

  // now do fft
  int num_iterations = num_bits(length-1);
  for (int i = 0; i<num_iterations; i++) {
    int outer = (int)round(pow(2, num_iterations-i-1));
    int inner = length/(2*outer);

    //printf("----------------------\n");
    #pragma omp parallel for collapse(2)
    for (int j = 0; j<outer; j++) {
      for (int k = 0; k<inner; k++) {
        int even_index = k+inner*2*j;
        int odd_index = k+inner*2*j+inner;
        int wn1 = outer*(even_index%(inner*2));
        int wn2 = outer*(odd_index%(inner*2));

        struct Complex new_even = {a[even_index].real + (w_ns[wn1].real * a[odd_index].real) - (w_ns[wn1].imaginary * a[odd_index].imaginary),
          a[even_index].imaginary + (w_ns[wn1].real * a[odd_index].imaginary) + (w_ns[wn1].imaginary * a[odd_index].real)};

        struct Complex new_odd = {a[even_index].real + (w_ns[wn2].real * a[odd_index].real) - (w_ns[wn2].imaginary * a[odd_index].imaginary),
          a[even_index].imaginary + (w_ns[wn2].real * a[odd_index].imaginary) + (w_ns[wn2].imaginary * a[odd_index].real)};

        a[even_index] = new_even;
        a[odd_index] = new_odd;
      }
    }
  }

  free(w_ns);
}
