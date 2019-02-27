#ifndef FFT_H
#define FFT_H

struct Complex {
  double real;
  double imaginary;
};

int bit_reverse(int a, int max);
int num_bits(int n);
void dft(struct Complex a[], int length);
void fft(struct Complex a[], int length);

#endif
