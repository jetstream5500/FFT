#include "stdio.h"
#include "math.h"

struct Complex {
  double real;
  double imaginary;
};

void print_array(int a[], int length) {
  for (int i = 0; i<length; i++) {
    if (i == 0) {
      printf("[%d, ", a[i]);
    } else if (i == length-1) {
      printf("%d]\n", a[i]);
    } else {
      printf("%d, ", a[i]);
    }
  }
}

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

void print_complex(struct Complex c) {
  printf("%f+%fj\n", c.real, c.imaginary);
}

void test(int a) {
  int a = 5;
}

// Only works on powers of 2
void fft(struct Complex a[], int length, struct Complex transforms[]) {
  // bit reverse
  for (int i = 0; i<length; i++) {
    transforms[i] = a[bit_reverse(i, length)];
  }

  // fft
  // Compute w_ns that will be used throughout
  struct Complex w_ns[length];
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
    for (int j = 0; j<outer; j++) {
      for (int k = 0; k<inner; k++) {
        int even_index = k+inner*2*j;
        int odd_index = k+inner*2*j+inner;
        int wn1 = outer*(even_index%(inner*2));
        int wn2 = outer*(odd_index%(inner*2));
        //printf("----------------------\n");
        //printf("even: %d\n", even_index);
        //printf("odd: %d\n", odd_index);
        //printf("wn1: %d\n", wn1);
        //printf("wn2: %d\n", wn2);

        struct Complex new_even = {transforms[even_index].real + (w_ns[wn1].real * transforms[odd_index].real) - (w_ns[wn1].imaginary * transforms[odd_index].imaginary),
          transforms[even_index].imaginary + (w_ns[wn1].real * transforms[odd_index].imaginary) + (w_ns[wn1].imaginary * transforms[odd_index].real)};

        struct Complex new_odd = {transforms[even_index].real + (w_ns[wn2].real * transforms[odd_index].real) - (w_ns[wn2].imaginary * transforms[odd_index].imaginary),
          transforms[even_index].imaginary + (w_ns[wn2].real * transforms[odd_index].imaginary) + (w_ns[wn2].imaginary * transforms[odd_index].real)};

        transforms[even_index] = new_even;
        transforms[odd_index] = new_odd;
      }
    }
  }
}

int main(int argc, char *argv[]) {
  // with struct
  struct Complex a[8];
  a[0].real = 1;
  a[0].imaginary = 0;
  a[1].real = 2;
  a[1].imaginary = 0;
  a[2].real = 3;
  a[2].imaginary = 1;
  a[3].real = 1;
  a[3].imaginary = 1;
  a[4].real = 2;
  a[4].imaginary = 2;
  a[5].real = 5;
  a[5].imaginary = 2;
  a[6].real = 6;
  a[6].imaginary = 1;
  a[7].real = 0;
  a[7].imaginary = -1;
  int length = 8;

  struct Complex transforms[length];
  fft(a, length, transforms);
  printf("--------------\n");
  for (int k = 0; k<length; k++) {
    printf("%f+%fj\n", transforms[k].real, transforms[k].imaginary);
  }

  return 0;
}
