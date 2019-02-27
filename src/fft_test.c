// Compilation: gcc-8 -fopenmp fft_test.c fft.c -o fft_test

#include "omp.h"
#include "stdio.h"
#include "stdlib.h"
#include "time.h"
#include "fft.h"

void random_data(struct Complex a[], int size) {
  srand(time(0));
  for (int i = 0; i<size; i++) {
    a[i].real = ((double)rand() / RAND_MAX) * 2000 - 1000;
    a[i].imaginary = ((double)rand() / RAND_MAX) * 2000 - 1000;
  }
}

void print_transforms(struct Complex transforms[], int size) {
  for (int i = 0; i<size; i++) {
    printf("%f+%fj\n", transforms[i].real, transforms[i].imaginary);
  }
}

void test_wikipedia_example() {
  // Algorithm Results
  printf("Test 1 - Wikipedia Example\n");
  printf("-------------------------------------\n");
  printf("Algorithm Results:\n");
  int size = 4;
  struct Complex a[] = {{1, 0}, {2, -1}, {0, -1}, {-1, 2}};

  fft(a, size);

  print_transforms(a, size);

  printf("-------------------------------------\n");
  printf("Actual Transform:\n");
  struct Complex actual_transforms[] = {{2,0}, {-2, -2}, {0, -2}, {4, 4}};

  print_transforms(actual_transforms, size);

  printf("-------------------------------------\n");
}

int main(int argc, char *argv[]) {
  test_wikipedia_example();

  for (int i = 2; i<=1048576; i*=2) {
    //printf("%d\n", i);
    struct Complex *a = malloc(sizeof(struct Complex)*i);

    random_data(a, i);
    double start = omp_get_wtime();
    fft(a, i);
    double end = omp_get_wtime();
    printf("%f\n", end-start);

    free(a);
  }

  return 0;
}
